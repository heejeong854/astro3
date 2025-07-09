import streamlit as st
import numpy as np

# 제목
st.title("천체 거리 계산기")

# 사용자 입력
st.header("입력 정보")
apparent_magnitude = st.number_input("겉보기 등급 (Apparent Magnitude)", value=0.0, step=0.1)
absolute_magnitude = st.number_input("절대 등급 (Absolute Magnitude)", value=0.0, step=0.1)

# 거리 계산 함수
def calculate_distance(apparent_magnitude, absolute_magnitude):
    if apparent_magnitude is not None and absolute_magnitude is not None:
        # 거리 모듈러스 계산
        distance_modulus = apparent_magnitude - absolute_magnitude
        # 거리 계산 (단위: 파섹)
        distance_parsecs = 10 ** ((distance_modulus + 5) / 5)
        # 파섹을 광년으로 변환 (1 파섹 ≈ 3.262 광년)
        distance_lightyears = distance_parsecs * 3.262
        return distance_lightyears
    return None

# 계산 버튼
if st.button("계산하기"):
    result = calculate_distance(apparent_magnitude, absolute_magnitude)
    if result is not None:
        st.success(f"천체까지의 거리: {result:.2f} 광년")
    else:
        st.error("유효한 등급 값을 입력하세요.")

# 참고 설명
st.write("참고: 거리 모듈러스 공식 (m - M = 5 * log10(d/10))을 사용하며, 결과는 광년 단위로 표시됩니다.")
