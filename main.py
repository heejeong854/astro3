import streamlit as st
from astropy.io import fits
import numpy as np

# 제목
st.title("FITS에서 등급 계산기")

# FITS 이미지 업로드
uploaded_file = st.file_uploader("FITS 이미지를 업로드하세요", type=["fits", "fits.fz"])

# 사용자 입력
distance = st.number_input("천체까지의 거리 (광년)", value=0.0, step=1.0)

# 등급 계산 함수
def calculate_magnitudes(data, distance):
    if data is not None and distance > 0:
        mean_flux = np.mean(data)
        reference_flux = 3.64e-8  # Vega 0등급의 대략적인 플럭스 (W/m²)
        apparent_magnitude = -2.5 * np.log10(mean_flux / reference_flux)
        distance_parsecs = distance / 3.262
        distance_modulus = 5 * np.log10(distance_parsecs / 10)
        absolute_magnitude = apparent_magnitude - distance_modulus
        return apparent_magnitude, absolute_magnitude
    return None, None

# FITS 처리 및 계산
if uploaded_file is not None:
    try:
        # 업로드된 파일을 임시로 열기
        with fits.open(uploaded_file) as hdul:
            data = hdul[0].data
            header = hdul[0].header
        
        if data is not None and data.ndim == 2:
            st.image(data, caption="FITS 이미지", use_column_width=True)
            st.write("### FITS 헤더 정보")
            st.write(dict(header))
            
            # 등급 계산
            apparent_mag, absolute_mag = calculate_magnitudes(data, distance)
            if apparent_mag is not None:
                st.success(f"겉보기 등급: {apparent_mag:.2f}")
                st.success(f"절대 등급: {absolute_mag:.2f}")
            else:
                st.error("유효한 거리 값을 입력하세요.")
        else:
            st.error("유효한 2D FITS 이미지가 아닙니다.")
        
        # 원본 FITS 다운로드
        st.download_button(
            label="원본 FITS 다운로드",
            data=uploaded_file.getvalue(),
            file_name=uploaded_file.name,
            mime="application/fits"
        )
    except Exception as e:
        st.error(f"FITS 파일 처리 중 오류 발생: {str(e)}")
else:
    st.write("FITS 이미지를 업로드하면 등급을 계산합니다.")

# 참고 설명
st.write("참고: 평균 플럭스를 기반으로 한 간단한 계산입니다. 정확한 값은 관측 조건과 보정 데이터가 필요할 수 있습니다.")
