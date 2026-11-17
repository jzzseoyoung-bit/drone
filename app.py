cd C:\workspaces\drone_data
# 기존에 app.py 가 있으면 덮어쓰지 않도록 이름 확인
# 아래 명령은 파일이 없으면 새로 생성합니다.
cat > app.py <<'EOF'
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Drone 유지보수 대시보드", layout="wide")
st.title("🚁 Drone 유지보수 프로젝트 대시보드")
st.markdown(
    """
    *위 보고서는 `submission_bundle.md`에 포함된 5개의 제출물을 한 번에 보여줍니다.*  
    아래는 자동으로 마크다운을 렌더링한 결과이며, 필요 시 파일을 수정하고 **git push** 하면 바로 반영됩니다.
    """
)

# submission_bundle.md 를 그대로 읽어 화면에 출력
md_path = Path(__file__).parent / "submission_bundle.md"
if md_path.is_file():
    st.markdown(md_path.read_text(encoding="utf-8"), unsafe_allow_html=True)
else:
    st.error("`submission_bundle.md` 파일을 찾을 수 없습니다.")
EOF