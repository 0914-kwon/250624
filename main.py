import streamlit as st
import pandas as pd

# CSV 파일 경로 (파일명에 맞게 변경)
CSV_PATH = "202505_202505_연령별인구현황_월간 (2).csv"

@st.cache_data
def load_and_process_data():
    df = pd.read_csv(CSV_PATH, encoding="euc-kr")

    # 총인구수 숫자 컬럼으로 분리
    df["총인구수"] = df["2025년05월_계_총인구수"].str.replace(",", "").astype(int)

    # 연령별 열 필터링 및 이름 정제
    age_cols = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
    rename_map = {col: col.replace("2025년05월_계_", "").replace("세", "").strip() for col in age_cols}
    df_age = df[["행정구역"] + age_cols].rename(columns=rename_map)

    # 쉼표 제거 후 숫자형 변환
    for col in df_age.columns[1:]:
        if df_age[col].dtype == object:
            df_age[col] = df_age[col].str.replace(",", "").astype(int)

    # 병합
    df_all = pd.merge(df[["행정구역", "총인구수"]], df_age, on="행정구역")
    return df_all

# 앱 UI 구성
st.title("2025년 5월 기준 연령별 인구 현황 분석")
st.markdown("총인구수가 많은 상위 5개 행정구역의 연령별 인구 분포를 선 그래프로 시각화합니다.")

# 데이터 불러오기
df_all = load_and_process_data()

# 총인구수 기준 상위 5개 지역 추출
top5_df = df_all.sort_values(by="총인구수", ascending=False).head(5)

# 원본 데이터 표시
st.subheader("📋 상위 5개 행정구역 원본 데이터")
st.dataframe(top5_df)

# 연령별 인구 그래프 준비
st.subheader("📈 연령별 인구 선 그래프")

age_columns = [col for col in top5_df.columns if col not in ["행정구역", "총인구수"]]
age_sorted = sorted(age_columns, key=lambda x: int(x.replace("이상", "1000")))

chart_data = top5_df.set_index("행정구역")[age_sorted].T
chart_data.index.name = "연령"

# Streamlit 기본 line_chart 사용
st.line_chart(chart_data)

# 설명
st.markdown("""
- 데이터 출처: 통계청  
- 단위: 명  
- 연령은 0세부터 100세 이상까지 포함됩니다.  
""")
