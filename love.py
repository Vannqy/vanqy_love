import os
import time
import itertools
import matplotlib.pyplot as plt
import streamlit as st

DEFAULT_MUSIC_PATH = "music.mp3"

st.set_page_config(page_title="💖 Heart Name", page_icon="💖", layout="centered")

st.markdown(
    "<h1 style='text-align:center;color:#ff4d6d;'>💖 Vẽ Trái Tim Từ Tên Bạn 💖</h1>",
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
        name = st.text_input("Nhập tên (tối đa 5 ký tự)", max_chars=5)
    with col2:
        size = st.slider("Kích thước (số dòng)", min_value=10, max_value=30, value=18)
    submitted = st.form_submit_button("✨ Vẽ trái tim")


def build_heart_grid(text: str, height: int):
    """Sinh lưới (cột, dòng, ký tự) ngay hàng thẳng lối tạo hình trái tim."""
    width = height * 2
    cyc = itertools.cycle(text)
    cells = []
    for yi in range(height, -height, -1):          # từ trên xuống dưới
        y = yi / height * 1.5
        for xi in range(-width, width):             # từ trái qua phải
            x = xi / width * 1.9
            f = (x ** 2 + y ** 2 - 1) ** 3 - (x ** 2) * (y ** 3)
            if f <= 0:
                cells.append((xi, yi, next(cyc)))
    return cells, width, height


if submitted:
    if not name.strip():
        st.error("Bạn chưa nhập tên!")
    elif len(name) > 5:
        st.error("Tên không được dài quá 5 ký tự!")
    else:
        name = name.strip()
        cells, width, height = build_heart_grid(name, size)

        if music_file is not None:
            st.audio(music_file, autoplay=True)
        elif os.path.exists(DEFAULT_MUSIC_PATH):
            st.audio(DEFAULT_MUSIC_PATH, autoplay=True)

        placeholder = st.empty()
        font_size = max(6, min(18, int(260 / size)))

        total = len(cells)
        step = max(1, total // 80)  # ~80 khung hình để vẽ nhanh, mượt

        for i in range(step, total + step, step):
            fig, ax = plt.subplots(figsize=(6, 6))
            fig.patch.set_facecolor("black")
            ax.set_facecolor("black")
            ax.set_xlim(-width - 1, width + 1)
            ax.set_ylim(-height - 1, height + 1)
            ax.axis("off")

            for cx, cy, ch in cells[:i]:
                ax.text(
                    cx, cy, ch,
                    color="white", fontsize=font_size,
                    fontfamily="monospace", fontweight="bold",
                    ha="center", va="center",
                )

            placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(0.015)

        st.success(f"Hoàn thành trái tim từ tên: {name} 💖")
        st.balloons()
