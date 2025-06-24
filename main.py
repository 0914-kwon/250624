import streamlit as st
import pandas as pd

# CSV 파일 경로
CSV_PATH = "202505_202505_연령별인구현황_월간 (2).csv"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH, encoding="euc-kr")
    
    # 총인구수 컬럼 정리
    df["총인구수"] = df["2025년05월_계_총인구수"].str.replace(",", "").astype(int)

    # 연령별 인구 열만 선택
    age_cols = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
    rename_cols = {
        col: col.replace("2025년05월_계_", "").replace("세", "").replace(" ", "") 
        for col in age_cols
    }

    df_ages = df[["행정구역"] + age_cols].rename(columns=rename_cols)

    # 문자열 숫자 변환
    for col in df_ages.columns[1:]:
        if df_ages[col].dtype == object:
            df_ages[col] = df_ages[col].str.replace(",", "").astype(int)

    # 전체 병합
    df_full = pd.merge(df[["행정구역", "총인구수"]], df_ages, on="행정구역")
    return df_full

# 앱 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 데이터 불러오기
df = load_data()

# 상위 5개 행정구역 추출
top5_df = df.sort_values(by="총인구수", ascending=False).head(5)

# 전체 데이터프레임 보여주기
st.subheader("📋 원본 데이터 (총인구수 기준 상위 5개 지역)")
st.dataframe(top5_df)

# 연령 목록 추출
age_columns = [col for col in top5_df.columns if col not in ["행정구역", "총인구수"]]
age_sorted = sorted(age_columns, key=lambda x: int(x.replace("이상", "").replace("세", "")) if x.isdigit() else 999)

# 연령별 인구 선그래프
st.subheader("📈 연령별 인구 선 그래프")

top5_chart_df = top5_df.set_index("행정구역")[age_sorted].T
top5_chart_df.index.name = "연령"

st.line_chart(top5_chart_df)

# 설명
st.markdown("""
- 본 데이터는 통계청의 2025년 5월 기준 연령별 인구 자료를 기반으로 하며,
- 총인구수가 가장 많은 5개 행정구역을 기준으로 연령 분포를 시각화하였습니다.
""")
