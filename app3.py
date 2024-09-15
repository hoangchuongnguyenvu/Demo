import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageDraw

def draw_rectangle(image, rect):
    """ Vẽ hình chữ nhật trên ảnh """
    img_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(img_pil)
    left, top, width, height = rect
    draw.rectangle([left, top, left + width, top + height], outline="blue", width=2)
    return np.array(img_pil)

def grabcut_segmentation(image, rect):
    """ Áp dụng thuật toán GrabCut để phân đoạn ảnh """
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    mask = np.zeros(image.shape[:2], np.uint8)
    
    if rect:
        # GrabCut with rectangle
        cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 1, cv2.GC_INIT_WITH_RECT)
    else:
        # GrabCut with mask
        cv2.grabCut(image, mask, None, bgd_model, fgd_model, 1, cv2.GC_INIT_WITH_MASK)
    
    mask2 = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')
    segmented_image = cv2.bitwise_and(image, image, mask=mask2)
    return segmented_image

def main():
    st.title("Ứng Dụng Phân Đoạn Hình Ảnh với GrabCut")

    uploaded_file = st.file_uploader("Tải ảnh lên", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(image)

        st.write("Chọn cách nhập tọa độ vùng hình chữ nhật:")
        
        # Tạo lựa chọn giữa thanh kéo và nhập giá trị
        input_mode = st.radio("Chọn phương thức nhập:", ("Thanh kéo (Slider)", "Nhập thủ công (Number Input)"))

        # Kiểm tra phương thức được chọn
        if input_mode == "Thanh kéo (Slider)":
            # Nhập giá trị bằng thanh kéo
            left = st.slider("Tọa độ X của góc trái trên", 0, image_np.shape[1], 0)
            top = st.slider("Tọa độ Y của góc trái trên", 0, image_np.shape[0], 0)
            right = st.slider("Tọa độ X của góc phải dưới", 0, image_np.shape[1], image_np.shape[1])
            bottom = st.slider("Tọa độ Y của góc phải dưới", 0, image_np.shape[0], image_np.shape[0])

        else:
            # Nhập giá trị bằng hộp nhập liệu
            left = st.number_input("Nhập X của góc trái trên", 0, image_np.shape[1], 0)
            top = st.number_input("Nhập Y của góc trái trên", 0, image_np.shape[0], 0)
            right = st.number_input("Nhập X của góc phải dưới", 0, image_np.shape[1], image_np.shape[1])
            bottom = st.number_input("Nhập Y của góc phải dưới", 0, image_np.shape[0], image_np.shape[0])

        # Tạo hình chữ nhật từ giá trị đã điều chỉnh
        rect = (left, top, right - left, bottom - top)
        
        # Hiển thị ảnh gốc với hình chữ nhật
        img_with_rect = draw_rectangle(image_np, rect)
        st.image(img_with_rect, caption="Ảnh với hình chữ nhật", use_column_width=True)

        if st.button("Segment"):
            if rect:
                segmented_image = grabcut_segmentation(image_np, rect)
                st.image(segmented_image, caption="Ảnh phân đoạn với GrabCut", use_column_width=True)
            else:
                st.write("Vui lòng nhập tọa độ hình chữ nhật.")

if __name__ == "__main__":
    main()
