import streamlit as st
import pandas as pd

def app():
    st.title('대한민국 연령대별 인구 분포 (상위 5개 행정구역 기준)')

    # 데이터 불러오기 ('euc-kr' 인코딩 사용)
    df = pd.read_csv('202505_202505_연령별인구현황_월간.csv', encoding='euc-kr')

    # 데이터 전처리: 행정구역 이름 정제
    df['행정구역'] = df['행정구역'].astype(str).str.split(' ').str[0]

    # 열 이름 변경 (2025년 5월 기준 열에서 불필요한 접두사 제거)
    새로운_열_이름 = []
    for 열 in df.columns:
        if '2025년05월_계_' in 열:
            새_열 = 열.replace('2025년05월_계_', '')
            if '총인구수' in 새_열:
                새_열 = '총인구수'
            elif '연령구간인구수' in 새_열:
                새_열 = '연령구간인구수'
            else:
                새_열 = 새_열.replace('세', '세')  # 유지
            새로운_열_이름.append(새_열)
        else:
            새로운_열_이름.append(열)
    df.columns = 새로운_열_이름

    # 문자열 숫자에서 쉼표 제거 후 정수형으로 변환
    숫자열_목록 = [열 for 열 in df.columns if 열 != '행정구역']
    for 열 in 숫자열_목록:
        df[열] = df[열].astype(str).str.replace(',', '', regex=False).astype(int)

    # 총인구수 기준 상위 5개 행정구역 추출
    상위5_지역 = df.sort_values(by='총인구수', ascending=False).head(5)['행정구역'].tolist()
    df_상위5 = df[df['행정구역'].isin(상위5_지역)].copy()

    # 연령대별 인구 정보를 긴 형태로 변환
    df_변환 = df_상위5.melt(id_vars=['행정구역', '총인구수', '연령구간인구수'],
                          var_name='연령',
                          value_name='인구수')
    df_변환['연령'] = df_변환['연령'].str.extract('(\d+)').astype(int)

    st.write("---")
    st.header("원본 데이터")
    st.dataframe(df)

    st.write("---")
    st.header("상위 5개 행정구역의 연령대별 인구 분포")

    피벗_데이터 = df_변환.pivot_table(index='연령', columns='행정구역', values='인구수')
    st.line_chart(피벗_데이터)

if __name__ == '__main__':
    app()
