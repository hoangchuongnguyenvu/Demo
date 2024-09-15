import streamlit as st
import numpy as np
import cv2 as cv
from PIL import Image

# Thiết lập màu sắc và giá trị vẽ
BLUE = [255, 0, 0]        # rectangle color
RED = [0, 0, 255]         # PR BG
GREEN = [0, 255, 0]       # PR FG
BLACK = [0, 0, 0]         # sure BG
WHITE = [255, 255, 255]   # sure FG

DRAW_BG = {'color': BLACK, 'val': 0}
DRAW_FG = {'color': WHITE, 'val': 1}
DRAW_PR_BG = {'color': RED, 'val': 2}
DRAW_PR_FG = {'color': GREEN, 'val': 3}

st.title("Interactive Image Segmentation using GrabCut")

# Upload hình ảnh
uploaded_file = st.file_uploader("Chọn file ảnh", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv.imdecode(file_bytes, 1)
    img2 = img.copy()  # Copy ảnh gốc
    mask = np.zeros(img.shape[:2], dtype=np.uint8)  # Tạo mask trống
    output = np.zeros(img.shape, np.uint8)  # Ảnh kết quả

    # Chọn tọa độ cho hình chữ nhật
    x1 = st.slider("Chọn x1 (tọa độ trái)", 0, img.shape[1], 50)
    y1 = st.slider("Chọn y1 (tọa độ trên)", 0, img.shape[0], 50)
    x2 = st.slider("Chọn x2 (tọa độ phải)", x1 + 1, img.shape[1], 300)
    y2 = st.slider("Chọn y2 (tọa độ dưới)", y1 + 1, img.shape[0], 300)

    # Vẽ hình chữ nhật và các chấm tròn lên ảnh gốc
    img_with_rect = img.copy()
    cv.rectangle(img_with_rect, (x1, y1), (x2, y2), BLUE, 2)  # Vẽ hình chữ nhật
    cv.circle(img_with_rect, (x1, y1), 10, RED, -1)  # Vẽ chấm tròn tại góc trên trái
    cv.circle(img_with_rect, (x2, y2), 10, GREEN, -1)  # Vẽ chấm tròn tại góc dưới phải

    # Hiển thị ảnh có hình chữ nhật và các chấm tròn
    st.image(img_with_rect, caption="Ảnh gốc với vùng chọn", use_column_width=True)

    rect = (x1, y1, x2 - x1, y2 - y1)

    if st.button("Áp dụng GrabCut"):
        # Kiểm tra giá trị hình chữ nhật
        if rect[2] <= 0 or rect[3] <= 0:
            st.error("Kích thước hình chữ nhật không hợp lệ.")
        else:
            # Tạo mô hình nền và mô hình đối tượng
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)

            # Áp dụng thuật toán GrabCut
            cv.grabCut(img2, mask, rect, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_RECT)

            # Xử lý mask để tạo ảnh kết quả
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            output = img2 * mask2[:, :, np.newaxis]

            # Hiển thị ảnh sau khi áp dụng GrabCut
            st.image(output, caption="Kết quả phân đoạn", use_column_width=True)

    # Tùy chọn lưu kết quả
    if st.button("Lưu kết quả"):
        output_image = Image.fromarray(cv.cvtColor(output, cv.COLOR_BGR2RGB))
        output_image.save("grabcut_output.png")
        st.write("Ảnh đã được lưu với tên `grabcut_output.png`")
