import streamlit as st
import pandas as pd
import altair as alt
import os

# -------------------
# 1. 기본 CSV 파일 확인
# -------------------
st.title("🌍 MBTI 유형별 Top 10 국가 분석")
st.write("기본 CSV 파일을 불러오거나, 없으면 업로드한 파일을 사용합니다.")

default_path = "countriesMBTI_16types.csv"
df = None

if os.path.exists(default_path):
    st.success(f"✅ 기본 데이터 파일({default_path})을 불러왔습니다.")
    df = pd.read_csv(default_path)
else:
    uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ 업로드한 데이터 파일을 사용합니다.")

# -------------------
# 2. 데이터 분석 및 시각화
# -------------------
if df is not None:
    mbti_types = df.columns[1:]  # 첫 번째 열은 Country, 나머지는 MBTI 유형
    selected_type = st.selectbox("🔎 MBTI 유형을 선택하세요:", mbti_types)

    # Top 10 국가 추출
    top10 = df[["Country", selected_type]].sort_values(by=selected_type, ascending=False).head(10)

    st.subheader(f"📊 {selected_type} 유형 비율 Top 10 국가")
    st.dataframe(top10)

    # Altair 그래프
    chart = (
        alt.Chart(top10)
        .mark_bar()
        .encode(
            x=alt.X(selected_type, title="비율"),
            y=alt.Y("Country", sort="-x", title="국가"),
            tooltip=["Country", selected_type]
        )
        .properties(width=600, height=400, title=f"{selected_type} 유형 Top 10 국가")
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("⬆️ 기본 데이터가 없으면 CSV 파일을 업로드해주세요.")
