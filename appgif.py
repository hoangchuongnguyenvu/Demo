import streamlit as st
import base64

def add_bg_gif(gif_path):
    """Thêm GIF làm background trang"""
    with open(gif_path, "rb") as f:
        gif_data = f.read()
    gif_base64 = base64.b64encode(gif_data).decode("utf-8")

    # CSS để thêm GIF làm background
    st.markdown(
        f"""
        <style>
        body {{
            background: url(data:image/gif;base64,{gif_base64}) no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.title("Trang Web Trang Trí Bằng GIF")
    
    # Tải GIF từ máy tính lên
    gif_file = st.file_uploader("Tải lên một GIF để làm nền trang trí", type=["gif"])
    
    if gif_file is not None:
        # Lưu tạm GIF vào hệ thống
        with open("uploaded_gif.gif", "wb") as f:
            f.write(gif_file.getbuffer())
        
        # Thêm GIF làm background
        add_bg_gif("uploaded_gif.gif")

    st.write("Bạn có thể thêm nội dung khác ở đây.")

if __name__ == "__main__":
    main()
