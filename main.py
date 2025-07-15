import streamlit as st
from astropy.io import fits
import numpy as np
import io

# 제목
st.title("FITS에서 겉보기 등급 계산기")

# FITS 이미지 업로드
uploaded_file = st.file_uploader("FITS 이미지를 업로드하세요", type=["fits", "fits.fz"])

# 등급 계산 함수 (겉보기 등급만)
def calculate_apparent_magnitude(data):
    if data is not None and np.any(data > 0):
        mean_flux = np.mean(data[data > 0])  # 0 이상인 데이터만 사용
        reference_flux = 3.64e-8  # Vega 0등급의 대략적인 플럭스 (W/m²)
        apparent_magnitude = -2.5 * np.log10(mean_flux / reference_flux)
        return apparent_magnitude
    return None

# FITS 처리 및 계산
if uploaded_file is not None:
    try:
        # 파일 데이터를 메모리에 복사
        file_content = uploaded_file.read()
        file_obj = io.BytesIO(file_content)
        
        # FITS 파일 열기
        with fits.open(file_obj) as hdul:
            # 2D 데이터가 있는 HDU 찾기
            data = None
            for i, hdu in enumerate(hdul):
                if hdu.data is not None and hdu.data.ndim == 2:
                    data = hdu.data
                    break
            
            if data is not None:
                # 겉보기 등급 계산
                apparent_mag = calculate_apparent_magnitude(data)
                if apparent_mag is not None:
                    st.success(f"**겉보기 등급**: {apparent_mag:.2f}")
                else:
                    st.error("데이터를 기반으로 등급을 계산할 수 없습니다.")
            else:
                st.error("2D 이미지 데이터를 포함한 HDU를 찾을 수 없습니다.")
        
        # 원본 FITS 다운로드
        st.download_button(
            label="원본 FITS 다운로드",
            data=file_content,
            file_name=uploaded_file.name,
            mime="application/fits"
        )
    except Exception as e:
        st.error(f"FITS 파일 처리 중 오류 발생: {str(e)}")
else:
    st.write("FITS 이미지를 업로드하면 겉보기 등급을 계산합니다.")

# 참고 설명
st.write("참고: 평균 플럭스를 기반으로 한 간단한 계산입니다. 정확한 값은 관측 조건과 보정 데이터가 필요할 수 있습니다.")
