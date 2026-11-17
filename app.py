import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 페이지 기본 설정
# --------------------------------------------------
st.set_page_config(page_title="Drone 유지보수 대시보드", layout="wide")

st.title("🚁 Drone 유지보수 프로젝트 대시보드")

# 사이드바 네비게이션
st.sidebar.header("📂 항목 선택")
sections = [
    "전체 보고서",
    "예측 CSV",
    "모델 결과",
    "위험 임계값",
    "Top‑20 재점검 계획",
]
selected = st.sidebar.radio("보여줄 항목", sections)

# --------------------------------------------------
# 헬퍼: 마크다운 파일을 읽어 표시
# --------------------------------------------------
def show_markdown(file_path: Path):
    if file_path.is_file():
        md_text = file_path.read_text(encoding="utf-8")
        st.markdown(md_text, unsafe_allow_html=True)
    else:
        st.error(f"`{file_path.name}` 파일을 찾을 수 없습니다.")

# --------------------------------------------------
# 각 섹션 별 내용
# --------------------------------------------------
if selected == "전체 보고서":
    st.subheader("📄 submission_bundle.md")
    show_markdown(Path(__file__).parent / "submission_bundle.md")

elif selected == "예측 CSV":
    st.subheader("📊 test_predictions_2025.csv")
    csv_path = Path(__file__).parent / "test_predictions_2025.csv"
    if csv_path.is_file():
        df = pd.read_csv(csv_path)
        st.dataframe(df)
    else:
        st.error("`test_predictions_2025.csv` 파일을 찾을 수 없습니다.")

elif selected == "모델 결과":
    st.subheader("📈 model_results.md")
    show_markdown(Path(__file__).parent / "model_results.md")

elif selected == "위험 임계값":
    st.subheader("⚖️ risk_threshold.md")
    show_markdown(Path(__file__).parent / "risk_threshold.md")

elif selected == "Top‑20 재점검 계획":
    st.subheader("🔝 top20_reinspection.md")
    show_markdown(Path(__file__).parent / "top20_reinspection.md")

# --------------------------------------------------
# 현재 백엔드 정보 표시 (SQLite vs Supabase)
# --------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.caption("백엔드: ")
secrets_path = Path(__file__).parent / ".streamlit" / "secrets.toml"
if secrets_path.is_file():
    txt = secrets_path.read_text(encoding="utf-8")
    if "sqlite" in txt.lower():
        backend = "SQLite (로컬)"
    elif "postgres" in txt.lower() or "supabase" in txt.lower():
        backend = "Postgres (Supabase)"
    else:
        backend = "알 수 없음"
    st.sidebar.write(backend)
else:
    st.sidebar.write("(secrets.toml 없음)")
