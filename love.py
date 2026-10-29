import time
import base64
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

MUSIC_PATH = "choanhchutthoi.mp3"

st.set_page_config(page_title="💖 Heart Name", page_icon="💖", layout="centered")

st.markdown(
    "<h1 style='text-align:center;color:#ff4d6d;'>8/3 Secrect!</h1>",
    unsafe_allow_html=True,
)

with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("", max_chars=5)
    with col2:
        size = st.slider("Kích thước - Nên để 10 được gòi", min_value=5, max_value=30, value=15)
    submitted = st.form_submit_button("Bắt đầu")


def play_music_loop(path: str):
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <audio autoplay loop style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True,
    )


if submitted:
    if not name.strip():
        st.error("Nhập tên đi quý cô!")
    elif len(name) > 5:
        st.error("Tên không được dài quá 5 ký tự!")
    else:
        name = name.strip()

        play_music_loop(MUSIC_PATH)

        # --- Tạo đường cong trái tim (parametric heart curve) ---
        t = np.linspace(0, 2 * np.pi, 300)
        x = 16 * np.sin(t) ** 3
        y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

        x = x * (size / 15)
        y = y * (size / 15)

        # Lấp đầy bên trong trái tim bằng các điểm ngẫu nhiên có trọng số
        rng = np.random.default_rng(42)
        fill_t = rng.uniform(0, 2 * np.pi, 400)
        fill_r = rng.uniform(0, 1, 400) ** 0.5  # dồn điểm ra rìa ít hơn, đều hơn ở giữa
        fx = fill_r * 16 * np.sin(fill_t) ** 3
        fy = fill_r * (13 * np.cos(fill_t) - 5 * np.cos(2 * fill_t) - 2 * np.cos(3 * fill_t) - np.cos(4 * fill_t))
        fx = fx * (size / 15)
        fy = fy * (size / 15)

        # Trộn viền + điểm lấp đầy, sắp theo thứ tự "gõ phím" ngẫu nhiên nhưng cố định
        all_x = np.concatenate([x, fx])
        all_y = np.concatenate([y, fy])
        order = rng.permutation(len(all_x))
        all_x, all_y = all_x[order], all_y[order]

        # Gán mỗi điểm một ký tự trong tên, lặp vòng
        chars = [name[i % len(name)] for i in range(len(all_x))]

        placeholder = st.empty()
        max_dim = max(np.abs(all_x).max(), np.abs(all_y).max()) * 1.2

        step = max(1, len(all_x) // 120)  # giới hạn ~120 khung hình để mượt
        for i in range(step, len(all_x) + step, step):
            fig, ax = plt.subplots(figsize=(6, 6))
            fig.patch.set_facecolor("black")
            ax.set_facecolor("black")
            ax.set_xlim(-max_dim, max_dim)
            ax.set_ylim(-max_dim, max_dim)
            ax.axis("off")

            cx, cy = all_x[:i], all_y[:i]
            cchars = chars[:i]
            for px, py, ch in zip(cx, cy, cchars):
                ax.text(
                    px, py, ch,
                    color="white", fontsize=max(8, size / 2),
                    fontweight="bold", ha="center", va="center",
                    alpha=0.95,
                )

            placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(0.02)

        st.success(f"Món quà 8/3 dành cho {name} 💖")
        st.balloons()
