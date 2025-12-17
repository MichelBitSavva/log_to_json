import streamlit as st
from parser.parser import Parser

st.set_page_config(layout="wide", page_title="CallContext Parser Compare")

# ==============================
# Инициализация состояния
# ==============================
def init_state():
    defaults = {
        "left_input": "",
        "left_result": None,
        "right_input": "",
        "right_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ==============================
# Служебные функции
# ==============================
def reset_all():
    st.session_state.left_input = ""
    st.session_state.left_result = None
    st.session_state.right_input = ""
    st.session_state.right_result = None

def parse_left():
    text = st.session_state.left_input.strip()
    if not text:
        return
    parser = Parser(text)
    st.session_state.left_result = parser.parse()

def parse_right():
    text = st.session_state.right_input.strip()
    if not text:
        return
    parser = Parser(text)
    st.session_state.right_result = parser.parse()

def clear_left():
    st.session_state.left_input = ""
    st.session_state.left_result = None

def clear_right():
    st.session_state.right_input = ""
    st.session_state.right_result = None

# ==============================
# UI
# ==============================
st.button("Сбросить всё", on_click=reset_all)

col1, col2 = st.columns(2)

# -------- ЛЕВОЕ ОКНО --------
with col1:
    st.subheader("Левое окно")

    st.text_area(
        "Лог для левого окна",
        key="left_input",
        height=200
    )

    btn1, btn2 = st.columns(2)
    btn1.button("Парсить левое", on_click=parse_left)
    btn2.button("Очистить левое", on_click=clear_left)

    if st.session_state.left_result is not None:
        st.subheader("Результат")
        st.json(st.session_state.left_result)

# -------- ПРАВОЕ ОКНО --------
with col2:
    st.subheader("Правое окно")

    st.text_area(
        "Лог для правого окна",
        key="right_input",
        height=200
    )

    btn3, btn4 = st.columns(2)
    btn3.button("Парсить правое", on_click=parse_right)
    btn4.button("Очистить правое", on_click=clear_right)

    if st.session_state.right_result is not None:
        st.subheader("Результат")
        st.json(st.session_state.right_result)
