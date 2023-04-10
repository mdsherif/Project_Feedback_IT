import streamlit as st

from config import config
from utilty import initDb, clearSession

st.set_page_config(page_title=config.feedback)

if "loginAuth" not in st.session_state:
    st.session_state["loginAuth"] = False

wards = []
rooms = []
patients = []


def loginAuth():
    conn, cur = initDb()
    username, password, profession = (
        st.session_state["username"],
        st.session_state["password"],
        st.session_state["profession"],
    )
    clearSession(value="login")

    result = cur.execute(
        f'SELECT * FROM LOGIN WHERE USERNAME = "{username}"'
    ).fetchone()
    try:
        if profession != result[1]:
            st.error("Wrong Profession")
        elif password != result[-1]:
            st.error("Invalid Credentials")
        else:
            st.success("Login Successful")
            st.session_state["loginAuth"] = True

    except TypeError:
        st.error("No User Found")


def LoginFunction():
    st.title("Login")

    col1, col2, col3 = st.columns(3)

    profession = col1.selectbox(
        "Profession",
        ["Select", "Nursing", "Guest Relation", "Doctor"],
        key="profession",
    )
    username = col2.text_input("Username", key="username")
    password = col3.text_input("Password", key="password", type="password")

    button = st.button("Login", on_click=loginAuth)

    return st.session_state["loginAuth"]


def firstSearch():
    conn, cur = initDb()
    global wards
    wards = []

    results = cur.execute("SELECT DISTINCT WARDID FROM DETAILS").fetchall()
    for result in results:
        wards.append(result[0])
    wards.insert(0, "Select")


def secondSearch():
    conn, cur = initDb()
    global rooms
    rooms = []

    ward = st.session_state["ward"]

    results = cur.execute(
        f"SELECT DISTINCT ROOMNO FROM DETAILS WHERE WARDID = '{ward}'"
    ).fetchall()

    try:
        for result in results:
            rooms.append(result[0])
        rooms.insert(0, "Select")
    except:
        st.error("No Such Ward")

    print(rooms)


def thirdSearch():
    pass


def FeedbackFunction():
    firstSearch()
    st.write(" ")
    date = st.date_input("Date", key="currDate")
    wardCol, roomCol, ipCol = st.columns(3)

    ward = wardCol.selectbox("Ward", wards, key="ward", on_change=secondSearch)
    roomno = roomCol.selectbox("Room No", rooms, key="roomno", on_change=thirdSearch)
    patientIpNo = ipCol.selectbox("Patient Ip No", patients, key="patientIpNo")
    clear = st.button("Clear")
    st.write(" ")

    with st.form("Patient Details Form"):
        st.title("Patient Details")

        patientName = st.text_input("Patient Name", key="patientName")

        col6, col7, col8 = st.columns(3)
        age = col6.number_input("Age", min_value=0, key="age")
        sex = col7.text_input(
            "Sex",
            key="sex",
        )
        mstatus = col8.text_input("Martial Status", key="mstatus")

        address = st.text_area("Address", key="address")

        col9, col10 = st.columns(2)
        phone = col9.text_input("Phone Number", key="pNo")
        email = col10.text_input("Email", key="email")

        col11, col12, col13 = st.columns(3)
        insurance = col11.text_input("Insurance", key="insurance")
        category = col12.text_input("Category", key="category")
        admittedby = col13.text_input("Admitted By", key="admittedby")

        col14, col15 = st.columns(2)
        admittedon = col14.date_input("Admitted On", key="admittedon")
        dischargedate = col15.date_input("Discharge Date", key="dischargedate")

        col16, col17 = st.columns(2)
        diagnosis = col16.text_input("Diagnosis", key="diagnosis")
        consultantname = col17.text_input("Consultant Name", key="consultantname")

        button = st.form_submit_button("")


if __name__ == "__main__":
    LoginFunction()
    FeedbackFunction()
