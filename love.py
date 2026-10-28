import os
import time
import itertools
import streamlit as st

DEFAULT_MUSIC_PATH = "music.mp3"

st.set_page_config(page_title="💖 Heart Name", page_icon="💖", layout="centered")

st.markdown(
    "<h1 style='text-align:center;color:#ff4d6d;'>💖 Vanqy chào phu nhân ! 💖</h1>",
    unsafe_allow_html=True,
)

music_file = st.file_uploader(
    "🎵 (Tuỳ chọn) Tải nhạc khác để ghi đè nhạc mặc định",
    type=["mp3", "wav", "ogg"],
)
if music_file is None and os.path.exists(DEFAULT_MUSIC_PATH):
    st.caption("🎶 Sẽ phát nhạc nền mặc định khi vẽ trái tim.")

with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Nhập chữ Tdy đi dợ", max_chars=5)
    with col2:
        size = st.slider("Kích thước (số dòng)", min_value=10, max_value=40, value=20)
    submitted = st.form_submit_button("✨ Vẽ trái tim")


def build_heart_rows(text: str, height: int):
    """Trả về list các chuỗi tạo hình trái tim, lấp bằng ký tự của `text` lặp vòng."""
    width = height * 2
    cyc = itertools.cycle(text)
    rows = []
    for yi in range(height, -height, -1):
        y = yi / height * 1.5
        row_chars = []
        for xi in range(-width, width):
            x = xi / width * 1.9
            f = (x ** 2 + y ** 2 - 1) ** 3 - (x ** 2) * (y ** 3)
            row_chars.append(next(cyc) if f <= 0 else " ")
        rows.append("".join(row_chars))
    return rows


if submitted:
    if not name.strip():
        st.error("Bạn chưa nhập tên!")
    elif len(name) > 5:
        st.error("Tên không được dài quá 5 ký tự!")
    else:
        name = name.strip()
        rows = build_heart_rows(name, size)

        if music_file is not None:
            st.audio(music_file, autoplay=True)
        elif os.path.exists(DEFAULT_MUSIC_PATH):
            st.audio(DEFAULT_MUSIC_PATH, autoplay=True)

        # font-size co giãn theo kích thước để hình không bị tràn khung
        font_size = max(6, min(16, int(220 / size)))

        placeholder = st.empty()
        for i in range(1, len(rows) + 1):
            text_block = "\n".join(rows[:i])
            html = f"""
            <pre style="
                background:#000;
                color:#ff4d6d;
                font-family:'Courier New', monospace;
                font-size:{font_size}px;
                line-height:{font_size}px;
                text-align:center;
                white-space:pre;
                padding:20px;
                border-radius:12px;
            ">{text_block}</pre>
            """
            placeholder.markdown(html, unsafe_allow_html=True)
            time.sleep(0.03)

        st.success(f"Hoàn thành: {name} 💖")
        st.balloons()
