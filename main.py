import streamlit as st

# MBTI 유형별 추천 직업 사전
mbti_jobs = {
    "ISTJ": ["회계사", "행정관", "감사원"],
    "ISFJ": ["간호사", "초등교사", "사회복지사"],
    "INFJ": ["심리학자", "작가", "상담가"],
    "INTJ": ["전략기획가", "데이터 과학자", "엔지니어"],
    "ISTP": ["기술자", "항공 정비사", "경찰관"],
    "ISFP": ["디자이너", "요리사", "물리치료사"],
    "INFP": ["시인", "작가", "예술가"],
    "INTP": ["연구원", "개발자", "과학자"],
    "ESTP": ["세일즈 매니저", "기업가", "경찰관"],
    "ESFP": ["연예인", "이벤트 플래너", "교사"],
    "ENFP": ["마케터", "작가", "기획자"],
    "ENTP": ["창업가", "광고기획자", "기술 컨설턴트"],
    "ESTJ": ["경영 관리자", "군인", "프로젝트 매니저"],
    "ESFJ": ["간호사", "상담가", "인사담당자"],
    "ENFJ": ["교사", "리더십 코치", "상담가"],
    "ENTJ": ["CEO", "변호사", "전략 컨설턴트"]
}

st.title("MBTI 기반 직업 추천기")

selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(mbti_jobs.keys()))

if selected_mbti:
    st.subheader(f"{selected_mbti} 유형에게 추천하는 직업:")
    for job in mbti_jobs[selected_mbti]:
        st.write(f"- {job}")
