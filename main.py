import streamlit as st
from astropy.io import fits
from PIL import Image
import numpy as np

# 탭으로 기능 분리
tab1, tab2 = st.tabs(["거리 계산", "FITS 변환"])

# 탭 1: 거리 계산
with tab1:
    st.title("천체 거리 계산기")
    apparent_magnitude = st.number_input("겉보기 등급 (Apparent Magnitude)", value=0.0, step=0.1)
    absolute_magnitude = st.number_input("절대 등급 (Absolute Magnitude)", value=0.0, step=0.1)

    def calculate_distance(apparent_magnitude, absolute_magnitude):
        if apparent_magnitude is not None and absolute_magnitude is not None:
            distance_modulus = apparent_magnitude - absolute_magnitude
            distance_parsecs = 10 ** ((distance_modulus + 5) / 5)
            distance_lightyears = distance_parsecs * 3.262
            return distance_lightyears
        return None

    if st.button("거리 계산하기"):
        result = calculate_distance(apparent_magnitude, absolute_magnitude)
        if result is not None:
            st.success(f"천체까지의 거리: {result:.2f} 광년")
        else:
            st.error("유효한 등급 값을 입력하세요.")
    st.write("참고: 거리 모듈러스 공식 (m - M = 5 * log10(d/10))을 사용하며, 결과는 광년 단위로 표시됩니다.")

# 탭 2: FITS 변환
with tab2:
    st.title("이미지 FITS 변환기")
    uploaded_file = st.file_uploader("변환할 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

    def convert_to_fits(image_data):
        img = Image.open(image_data)
        img_gray = img.convert('L')
        img_array = np.array(img_gray)
        hdu = fits.PrimaryHDU(img_array)
        hdu.writeto("output.fits", overwrite=True)
        return "output.fits"

    if uploaded_file is not None:
        st.image(uploaded_file, caption="업로드된 이미지", use_column_width=True)
        if st.button("FITS로 변환"):
            fits_file = convert_to_fits(uploaded_file)
            with open(fits_file, "rb") as f:
                st.download_button(
                    label="FITS 파일 다운로드",
                    data=f,
                    file_name="converted_image.fits",
                    mime="application/fits"
                )
            st.success("FITS 파일로 변환되었습니다!")
