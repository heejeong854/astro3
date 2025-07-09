import streamlit as st
import numpy as np

# 제목
st.title("천체 밝기 계산기")

# 이미지 업로드
uploaded_file = st.file_uploader("천체 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

# 사용자 입력
st.header("입력 정보")
flux = st.number_input("플럭스 값 (W/m²) 입력", value=0.0, step=0.001)
distance = st.number_input("천체까지의 거리 (광년) 입력", value=0.0, step=1.0)
reference_magnitude = st.number_input("기준 등급 (예: 0 등급의 Vega)", value=0.0, step=0.1)

# 계산 함수
def calculate_magnitudes(flux, distance, reference_magnitude):
    if flux <= 0 or distance <= 0:
        return None, None
    
    # 겉보기 등급 계산 (간단화된 모델)
    apparent_magnitude = -2.5 * np.log10(flux) + reference_magnitude
    
    # 절대 등급 계산 (거리 보정)
    # 거리 모듈러스: 5 * log10(거리/10)
    distance_modulus = 5 * np.log10(distance / 10)
    absolute_magnitude = apparent_magnitude - distance_modulus
    
    return apparent_magnitude, absolute_magnitude

# 계산 버튼
if st.button("계산하기"):
    if uploaded_file is not None:
        st.image(uploaded_file, caption="업로드된 이미지", use_column_width=True)
    result = calculate_magnitudes(flux, distance, reference_magnitude)
    if result[0] is not None:
        st.success(f"겉보기 등급: {result[0]:.2f}")
        st.success(f"절대 등급: {result[1]:.2f}")
    else:
        st.error("유효한 플럭스와 거리 값을 입력하세요.")

# 참고 설명
st.write("참고: 플럭스 값은 이미지 메타데이터나 관측 데이터에서 추출해야 합니다. 정확한 계산을 위해 우주 망원경 데이터(예: Hubble FITS 파일)를 사용하는 것이 이상적입니다.")
