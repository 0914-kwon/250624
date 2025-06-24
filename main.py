import streamlit as st
import pandas as pd

# CSV 파일명
CSV_FILE = "202505_202505_연령별인구현황_월간 (1).csv"

@st.cache_data
def load_data():
    # CSV 파일 읽기 (EUC-KR 인코딩)
    df = pd.read_csv(CSV_FILE, encoding="euc-kr")

    # 열 이름 정리: 앞뒤 공백, 중간 공백, 전각 공백 제거
    df.columns = df.columns.str.strip().str.replace(" ", "").str.replace("\u3000", "")

    # 디버깅용: 전체 컬럼 목록 출력
    st.write("✅ CSV 파일에서 불러온 컬럼 목록:", df.columns.tolist())

    # '총인구수'가 포함된 열 찾기
    col_match = [col for col in df.columns if '총인구수' in col]
    st.write("🔍 총인구수 관련 열 후보:", col_match)

    if not col_match:
        st.error("'총인구수'라는 열 이름이 포함된 컬럼을 찾을 수 없습니다. 파일 구조를 확인해주세요.")
        st.stop()

    # 총인구수 처리
    df["총인구수"] = df[col_match[0]].str.replace(",", "").astype(int)

    # 연령별 인구 열 추출
    age_cols = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]

    # 열 이름을 숫자 연령으로 변환
    rename_map = {
        col: col.replace("2025년05월_계_", "").replace("세", "").replace(" ", "")
        for col in age_cols
    }
    df_age = df[["행정구역"] + age_cols].rename(columns=rename_map)

    # 쉼표 제거 및 숫자 변환
    for col in df_age.columns[1:]:
        if df_age[col].dtype == object:
            df_age[col] = df_age[col].str.replace(",", "").astype(int)

    # 병합
    df_result = pd.merge(df[["행정구역", "총인구수"]], df_age, on="행정구역")
    return df_result

# ----------------------------------------
# Streamlit 앱 시작
# ----------------------------------------

# 제목
st.title("2025년 5월 연령별 인구 현황 분석")

# 데이터 로드
df_all = load_data()

# 상위 5개 행정구역 추출
top5_df = df_all.sort_values(by="총인구수", ascending=False).head(5)

# 원본 데이터 표시
st.subheader("📋 총인구수 기준 상위 5개 행정구역 데이터")
st.dataframe(top5_df)

# 연령별 인구 선 그래프
st.subheader("📈 연령별 인구 선 그래프")

# 연령 컬럼 정렬
age_cols = [col for col in top5_df.columns if col not in ["행정구역", "총인구수"]]
age_sorted = sorted(age_cols, key=lambda x: int(x.replace("이상", "1000")) if x.isdigit() else 999)

# 전치하여 연령별로 정리
chart_df = top5_df.set_index("행정구역")[age_sorted].T
chart_df.index.name = "연령"

# Streamlit 기본 line_chart 시각화
st.line_chart(chart_df)

# 주석
st.markdown("""
- 데이터 출처: 통계청  
- 단위: 명  
- 연령은 0세부터 100세 이상까지 포함됩니다.  
- 시각화 도구는 Streamlit 기본 기능 `st.line_chart`만 사용했습니다.
""")
