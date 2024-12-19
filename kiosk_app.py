import streamlit as st
from collections import Counter  # 중복된 항목의 개수를 집계

# 페이지 레이아웃 설정
st.set_page_config(
    page_title="키오스크",   # 브라우저 탭 제목
    page_icon="☕",         # 브라우저 탭 아이콘
    layout="wide"          # 레이아웃: wide
)

# 상태 관리 초기화
if "page" not in st.session_state:
    st.session_state.page = "시즌메뉴"  # 초기값을 categories 키 중 하나로 설정
if "order" not in st.session_state:
    st.session_state.order = []

# 카테고리별 상품 데이터
categories = {
    "시즌메뉴": {
        "바닐라 크림 콜드브루": {"price": 5500, "image": "https://via.placeholder.com/150?text=바닐라+콜드브루"},
        "딸기 라떼": {"price": 6000, "image": "https://via.placeholder.com/150?text=딸기+라떼"},
    },
    "커피(HOT)": {
        "아메리카노": {"price": 4000, "image": "https://via.placeholder.com/150?text=아메리카노+HOT"},
        "카페라떼": {"price": 4500, "image": "https://via.placeholder.com/150?text=카페라떼+HOT"},
    },
    "커피(ICE)": {
        "아이스 아메리카노": {"price": 4500, "image": "https://via.placeholder.com/150?text=아이스+아메리카노"},
        "아이스 카페라떼": {"price": 5000, "image": "https://via.placeholder.com/150?text=아이스+카페라떼"},
    },
}

# 전체 레이아웃 구성
layout = st.columns([2, 6, 4])  # 좌측(카테고리 버튼), 중앙(상품), 우측(장바구니)

# 1. 좌측: 카테고리 버튼
with layout[0]:
    st.header("카테고리")
    if st.button("시즌메뉴"):
        st.session_state.page = "시즌메뉴"
    if st.button("커피(HOT)"):
        st.session_state.page = "커피(HOT)"
    if st.button("커피(ICE)"):
        st.session_state.page = "커피(ICE)"

# 2. 중앙: 선택된 카테고리의 상품 표시
with layout[1]:
    if st.session_state.page not in categories:
        st.error("잘못된 카테고리입니다. 기본 카테고리로 초기화합니다.")
        st.session_state.page = "시즌메뉴"

    st.header(f"{st.session_state.page} 상품")
    selected_category = st.session_state.page
    products = categories[selected_category]
    cols = st.columns(len(products))  # 상품 개수에 따라 동적으로 열 배치
    for i, (product, details) in enumerate(products.items()):
        with cols[i]:
            st.image(details["image"], caption=f"{product}\n{details['price']}원", use_column_width=True)
            if st.button(f"추가 ({product})"):
                st.session_state.order.append(product)
                st.success(f"{product}이(가) 장바구니에 추가되었습니다!")

# 3. 우측: 장바구니
with layout[2]:
    st.header("장바구니")
    if st.session_state.order:
        total_price = 0

        # 중복된 항목 집계
        order_counts = Counter(st.session_state.order)
        for item, count in order_counts.items():
            # 가격 가져오기
            price = next(
                details["price"] for category in categories.values() for name, details in category.items() if name == item
            )
            st.write(f"- {item} x {count} - {price * count}원")
            total_price += price * count

        st.write(f"**총 결제 금액: {total_price}원**")
        if st.button("모든 상품 구매하기"):
            st.success(f"총 {total_price}원 결제가 완료되었습니다!")
            st.session_state.order = []  # 구매 후 장바구니 초기화
    else:
        st.write("장바구니가 비어 있습니다.")
