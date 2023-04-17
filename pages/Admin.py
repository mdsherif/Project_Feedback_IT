import streamlit as st
import datetime

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


class Admin:
    def __int__(self):
        self.wards = []
        self.rooms = []
        self.finalResult = None

    def searchWithDate(self):
        date = st.session_state["date"]
        self.wards = []
        self.rooms = []

        conn, cur = initDb()
        results = cur.execute(
            f'SELECT WARDID, ROOMNO FROM FEEDBACKFORM WHERE DATE_OF_FEEDBACK = "{date}"'
        ).fetchall()
        conn.close()

        if len(results) > 0:
            for i in results:
                self.wards.append(i[0])
                self.rooms.append(i[1])
            self.wards = list(set(self.wards))
            self.rooms = list((set(self.rooms)))
            self.wards.insert(0, "Select")
            self.rooms.insert(0, "Select")
            return self.wards, self.rooms
        else:
            st.error(f"No Feedback Taken On {date}")
            return [], []

    def formGenerator(self, results):
        for i in results:
            print(i)

    def finalSearch(self):
        date = st.session_state["date"]
        ward = st.session_state["ward"]
        room = st.session_state["room"]
        conn, cur = initDb()
        self.finalResult = cur.execute(
            f"SELECT * FROM FEEDBACKFORM WHERE WARDID = '{ward}' AND ROOMNO = '{room}' AND DATE_OF_FEEDBACK = '{date}'"
        ).fetchall()
        conn.close

        for i, result in enumerate(self.finalResult):
            st.text_input("IPID", value=result[1], key=i)

    def clearFunc(self):
        # st.session_state['date'] = datetime.datetime.now().date
        st.session_state["ward"] = "Select"
        st.session_state["room"] = "Select"

    def run(self):
        col1, col2, col3 = st.columns(3)
        col1.date_input("Date", key="date")
        wards, rooms = self.searchWithDate()
        col2.selectbox("Wards", wards, key="ward")

        col3.selectbox("Rooms", rooms, key="room")
        btnCol1, btnCol2, _, _, _, _ = st.columns(6)
        btnCol1.button("Clear", on_click=self.clearFunc)
        if btnCol2.button("Submit"):
            self.finalSearch()


if __name__ == "__main__":
    if "adminAuth" not in st.session_state:
        st.session_state["adminAuth"] = False

    if st.session_state["adminAuth"] == False:
        adminLogin()

    if st.session_state["adminAuth"] == True:
        admin = Admin()
        admin.run()
