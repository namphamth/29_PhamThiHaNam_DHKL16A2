import streamlit as st
from PIL import Image

# Trạng thái LED mô phỏng
if "led_on" not in st.session_state:
    st.session_state.led_on = False

# Xử lý sự kiện nút trước khi render
col1, col2 = st.columns(2)
with col1:
    if st.button("BẬT LED"):
        st.session_state.led_on = True
with col2:
    if st.button("TẮT LED"):
        st.session_state.led_on = False

# Sau khi cập nhật trạng thái → render ảnh
st.title("Điều khiển LED mô phỏng bằng Streamlit")

if st.session_state.led_on:
    image_file = "images/led_on_white_120.png"
    caption = "LED is ON"
else:
    image_file = "images/led_off_white_120.png"
    caption = "LED is OFF"

image = Image.open(image_file)
st.image(image, caption=caption, width=200)
