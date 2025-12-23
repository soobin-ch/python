%%writefile app.py
import streamlit as st

# 반드시 첫 Streamlit 호출
st.set_page_config(page_title="CSV 상관관계 시각화", layout="wide")

import pandas as pd
import numpy as np
import plotly.express as px

st.title("CSV 업로드 → 필드 선택 → 상관관계 분석")

# -------------------------------
# 1. CSV 업로드
# -------------------------------
uploaded = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded is None:
    st.info("CSV 파일을 업로드해주세요.")
    st.stop()

# CSV 로딩 (한글 대응)
try:
    df = pd.read_csv(uploaded)
except UnicodeDecodeError:
    df = pd.read_csv(uploaded, encoding="cp949")

st.subheader("원본 데이터 미리보기")
st.dataframe(df.head(20), use_container_width=True)

# -------------------------------
# 2. 필드(컬럼) 선택 UI
# -------------------------------
st.sidebar.header("① 분석할 필드 선택")

selected_cols = []
for col in df.columns:
    if st.sidebar.checkbox(col, key=f"col_{col}"):
        selected_cols.append(col)

if len(selected_cols) < 2:
    st.warning("상관관계 분석을 위해 최소 2개 이상의 컬럼을 선택하세요.")
    st.stop()

data = df[selected_cols].copy()

# -------------------------------
# 3. 수치형 컬럼 자동 판별
# -------------------------------
numeric_cols = [
    c for c in data.columns
    if pd.api.types.is_numeric_dtype(data[c])
]

if len(numeric_cols) < 2:
    st.error("선택된 컬럼 중 수치형 컬럼이 2개 이상 필요합니다.")
    st.stop()

num_df = data[numeric_cols].dropna(how="all")

if num_df.empty:
    st.error("필터 후 데이터가 없습니다.")
    st.stop()

# -------------------------------
# 4. 상관계수 설정
# -------------------------------
st.sidebar.header("② 상관관계 설정")

method = st.sidebar.selectbox(
    "상관계수 방식",
    ["pearson", "spearman"],
    index=0
)

min_corr = st.sidebar.slider(
    "표시할 최소 |상관계수|",
    0.0, 1.0, 0.0, 0.05
)

# -------------------------------
# 5. 상관관계 계산
# -------------------------------
corr = num_df.corr(method=method)
corr_filtered = corr.where(np.abs(corr) >= min_corr)

# -------------------------------
# 6. 상관관계 히트맵
# -------------------------------
st.subheader(f"상관관계 히트맵 ({method})")

fig = px.imshow(
    corr_filtered,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="RdBu_r",
    title="Correlation Heatmap"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 7. 산점도 매트릭스
# -------------------------------
st.subheader("선택된 필드 간 산점도")

max_cols = min(6, len(numeric_cols))
scatter_cols = st.multiselect(
    "산점도로 볼 컬럼 선택 (최대 6개)",
    numeric_cols,
    default=numeric_cols[:max_cols]
)

if len(scatter_cols) >= 2:
    fig2 = px.scatter_matrix(
        num_df[scatter_cols],
        dimensions=scatter_cols,
        title="Scatter Matrix"
    )
    fig2.update_traces(diagonal_visible=False)
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# 8. 간단한 해석 문구
# -------------------------------
st.subheader("📊 상관관계 해석 요약")

strong_corr = (
    corr.abs()
    .where(lambda x: (x >= 0.7) & (x < 1.0))
    .stack()
    .reset_index()
)

if strong_corr.empty:
    st.write("강한 상관관계(|r| ≥ 0.7)가 발견되지 않았습니다.")
else:
    for _, row in strong_corr.iterrows():
        st.write(
            f"- **{row['level_0']} ↔ {row['level_1']}** : 상관계수 {row[0]:.2f}"
        )

# -------------------------------
# 9. 결과 데이터 다운로드
# -------------------------------
st.subheader("분석에 사용된 데이터 다운로드")

csv_bytes = num_df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "CSV 다운로드",
    data=csv_bytes,
    file_name="correlation_data.csv",
    mime="text/csv"
)
