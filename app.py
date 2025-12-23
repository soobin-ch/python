# %%
import streamlit as st

# ✅ 필수 수정 1: 반드시 첫 Streamlit 호출
st.set_page_config(page_title="CSV 상관관계 시각화", layout="wide")

import pandas as pd
import numpy as np
import plotly.express as px

st.title("CSV 업로드 → 체크박스 선택 → 상관관계 시각화")

uploaded = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded is None:
    st.info("CSV 파일을 업로드해주세요.")
    st.stop()

# --- Load CSV ---
try:
    df = pd.read_csv(uploaded)
except UnicodeDecodeError:
    df = pd.read_csv(uploaded, encoding="cp949")

st.subheader("원본 데이터 미리보기")
st.dataframe(df.head(20), use_container_width=True)

# --- Column selection (fields) ---
st.sidebar.header("1) 분석할 필드(컬럼) 선택")
all_cols = df.columns.tolist()

selected_cols = []
for c in all_cols:
    if st.sidebar.checkbox(c, value=False, key=f"col_{c}"):
        selected_cols.append(c)

if len(selected_cols) == 0:
    st.warning("왼쪽 사이드바에서 분석할 컬럼을 최소 1개 이상 선택하세요.")
    st.stop()

work = df[selected_cols].copy()


