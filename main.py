import streamlit as st
import pandas as pd

CSV_FILE = "202505_202505_연령별인구현황_월간 (1).csv"

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_FILE, encoding="euc-kr")

    # 총인구수 숫자 처리
    df["총인구수"] = df["2025년05월_계_총인구수"].str.replace(",", "").astype(int)

    # 연령별 열 추출 및 이름 정제
    age_cols = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
    rename_map = {
        col: col.replace("2025년05월_계_", "").replace("세", "").replace(" ", "")
        for col in age_cols
    }
    df_age = df[["행정구역"] + age_cols].rename(columns=rename_map)

    # 쉼표 제거 후 숫자로 변환
    for col in df_age.columns[1:]:
        if df_age[col].dtype == object:
            df_age[col] = df_age[col].str.replace(",", "").astype(int)

    # 최종 병합
    df_result = pd.merge(df[["행정구역", "총인구수"]], df_age, on="행정구역")
    return df_result

# 앱 제목
st.title("2025년 5월 연령별 인구 현황 분석")

# 데이터 불러오기
df_all = load_data()

# 총인구수 기준 상위 5개 지역
top5_df = df_all.sort_values(by="총인구수", ascending=False).head(5)

# 원본 데이터 표시
st.subheader("📋 총인구수 기준 상위 5개 행정구역 데이터")
st.dataframe(top5_df)

# 연령별 선그래프 시각화
st.subheader("📈 연령별 인구 선 그래프")

# 연령 순서 정렬
age_cols = [col for col in top5_df.columns if col not in ["행정구역", "총인구수"]]
age_sorted = sorted(age_cols, key=lambda x: int(x.replace("이상", "1000")) if x.isdigit() else 999)

# 그래프용 전치 데이터 준비
chart_df = top5_df.set_index("행정구역")[age_sorted].T
chart_df.index.name = "연령"

# 기본 line chart 시각화
st.line_chart(chart_df)

# 주석
st.markdown("""
- 데이터 출처: 통계청  
- 단위: 명  
- 연령은 0세부터 100세 이상까지 포함됩니다.  
- 시각화 도구는 Streamlit 기본 기능 `st.line_chart`만 사용했습니다.
""")
