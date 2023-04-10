import streamlit as st
import sqlite3


def initDb():
    conn = sqlite3.connect("sqlite.db")
    cur = conn.cursor()
    return conn, cur


def clearSession(value):
    if value == "login":
        st.session_state.profession = "Select"
        st.session_state.username = ""
        st.session_state.password = ""

    elif value == "admin":
        st.session_state["Admin_Username"] = ""
        st.session_state["Admin_Password"] = ""
