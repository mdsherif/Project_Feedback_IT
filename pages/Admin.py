import streamlit as st

from utilty import initDb, clearSession


def adminLoginAuth():
    conn, cur = initDb()
    username, password = (
        st.session_state["Admin_Username"],
        st.session_state["Admin_Password"],
    )

    clearSession(value="admin")

    result = cur.execute(
        f"SELECT * FROM ADMINLOGIN WHERE USERNAME = '{username}'"
    ).fetchone()

    if len(result) == 0:
        st.error("No Admin User Found")

    elif password != result[-1]:
        st.error("Wrong Credentials")
    else:
        st.success("Admin Login Successful")
        st.session_state["adminAuth"] = True


def adminLogin():
    st.title("Admin Login")
    with st.form("Admin Login"):
        col1, col2 = st.columns(2)
        adminUsername = col1.text_input("Admin Username", key="Admin_Username")
        adminPassword = col2.text_input(
            "Admin Password", key="Admin_Password", type="password"
        )

        adminbutton = st.form_submit_button("Login", on_click=adminLoginAuth)


if __name__ == "__main__":
    if "adminAuth" not in st.session_state:
        st.session_state["adminAuth"] = False
        
    if st.session_state['adminAuth'] == False:
        adminLogin()

    if st.session_state["adminAuth"] == True:
        st.header("Not Admin")
