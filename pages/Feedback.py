import streamlit as st
from dateutil import parser
from datetime import datetime

from config import config
from utilty import initDb, clearSession

st.set_page_config(page_title=config.feedback)

wards = []
rooms = []
patients = []

if "loginAuth" not in st.session_state:
    st.session_state["loginAuth"] = False


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

    conn.close()


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


# def clearFunc():
#     st.session_state["patientName"] = " "
#     st.session_state["age"] = 0
#     st.session_state["sex"] = ""
#     st.session_state["mstatus"] = ""
#     st.session_state["address"] = ""
#     st.session_state["pNo"] = ""
#     st.session_state["email"] = ""
#     st.session_state["insurance"] = ""
#     st.session_state["category"] = ""
#     st.session_state["admittedby"] = ""
#     st.session_state["admittedon"] = datetime.now()
#     st.session_state["diagnosis"] = ""
#     st.session_state["dischargedate"] = datetime.now()
#     st.session_state["consultantname"] = ""


class FeedbackFunction:
    def __init__(self):
        self.firstSearch()

    def firstSearch(self):
        conn, cur = initDb()
        global wards
        wards = []

        results = cur.execute("SELECT DISTINCT WARDID FROM DETAILS").fetchall()
        try:
            wards = [i[0] for i in results]
            wards.insert(0, "Select")
        except IndexError or TypeError:
            st.error("Some Error")
        conn.close()

    def secondSearch(self):
        global rooms
        rooms = []
        conn, cur = initDb()

        ward = st.session_state["ward"]

        results = cur.execute(
            f"SELECT DISTINCT ROOMNO FROM DETAILS WHERE WARDID = '{ward}'"
        ).fetchall()

        try:
            rooms = [i[0] for i in results]
            rooms.insert(0, "Select")
        except IndexError or TypeError:
            st.error("No Such Ward")

        conn.close()

    def thirdSearch(self):
        global patients
        patients = []
        conn, cur = initDb()

        roomno = st.session_state["roomno"]
        results = cur.execute(
            f'SELECT IPID FROM DETAILS WHERE ROOMNO = "{roomno}"'
        ).fetchall()
        try:
            patients = [i[0] for i in results]
            patients.insert(0, "Select")
        except IndexError or TypeError:
            st.error("No Patient in Room: {roomno}")
        conn.close()

    def fillFunc(self):
        conn, cur = initDb()

        ipid = st.session_state["patientIpNo"]
        # ipid = ipid.split("-")[0]
        if ipid != None:
            results = cur.execute(
                f"SELECT * FROM DETAILS WHERE IPID = {int(ipid)}"
            ).fetchone()

            st.session_state["patientName"] = results[4]
            st.session_state["age"] = results[5]

            if results[6] == 1:
                st.session_state["sex"] = "MALE"
            elif results[6] == 2:
                st.session_state["sex"] = "FEMALE"
            elif results[6] == 3:
                st.session_state["sex"] = "TRANS"
            else:
                st.session_state["sex"] = "UNKNOWN"

            if results[7] == 1:
                st.session_state["mstatus"] = "MARRIED"
            elif results[7] == 1:
                st.session_state["mstatus"] = "SINGLE"
            else:
                st.session_state["mstatus"] = "WIDOW"

            st.session_state[
                "address"
            ] = f"{results[8]}, {results[9]}, {results[10]}, {results[11]}, {results[12]}"

            st.session_state["pNo"] = str(results[13])
            st.session_state["email"] = results[14]
            st.session_state["insurance"] = str(results[15])
            st.session_state["category"] = str(results[16])
            st.session_state["admittedon"] = parser.parse(results[17])
            st.session_state["admittedby"] = results[18]
            st.session_state["dischargedate"] = parser.parse(results[19])
            st.session_state["diagnosis"] = results[20]
            st.session_state["consultantname"] = results[21]

        conn.close()

    def clearFunc(self):
        st.session_state["patientName"] = " "
        st.session_state["age"] = 0
        st.session_state["sex"] = ""
        st.session_state["mstatus"] = ""
        st.session_state["address"] = ""
        st.session_state["pNo"] = ""
        st.session_state["email"] = ""
        st.session_state["insurance"] = ""
        st.session_state["category"] = ""
        st.session_state["admittedby"] = ""
        st.session_state["admittedon"] = datetime.now()
        st.session_state["diagnosis"] = ""
        st.session_state["dischargedate"] = datetime.now()
        st.session_state["consultantname"] = ""

    def run(self):
        st.write(" ")
        wardCol, roomCol, ipCol = st.columns(3)

        ward = wardCol.selectbox("Ward", wards, key="ward")
        if ward != "Select" or None:
            self.secondSearch()

        roomno = roomCol.selectbox("Room No", rooms, key="roomno")
        if roomno != "Select" or None:
            self.thirdSearch()

        patientIpNo = ipCol.selectbox("Patient Ip No", patients, key="patientIpNo")

        if patientIpNo != "Select" or None:
            self.fillFunc()

        clear = st.button("Clear", on_click=self.clearFunc)
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

            buttom = st.form_submit_button("")


class Form:
    def __init__(self, currDate):
        self.currDate = currDate
        self.ipId = st.session_state["patientIpNo"]

    def saveONDB(self):
        conn, cur = initDb()
        dInput = st.session_state["dInput"]
        nInput = st.session_state["nInput"]
        mInput = st.session_state["mInput"]
        mcInput = st.session_state["mCInput"]
        aOInput = st.session_state["aOInput"]
        fInput = st.session_state["fInput"]
        rInput = st.session_state["rInput"]

        result = cur.execute("""SELECT MAX(ID) FROM FEEDBACKFORM""")
        id = result.fetchone()[-1]

        cur.execute(
            f"""INSERT INTO FEEDBACKFORM VALUES({int(id+1)}, {str(self.ipId)}, '{self.currDate}', '{dInput}', '{nInput}', '{mInput}', '{mcInput}', '{aOInput}', '{fInput}', '{rInput}')"""
        )
        conn.commit()
        conn.close()
        st.session_state["dInput"] = "Yes"
        st.session_state["nInput"] = "Yes"
        st.session_state["mInput"] = "Yes"
        st.session_state["mCInput"] = ""
        st.session_state["aOInput"] = ""
        st.session_state["fInput"] = "Positive"
        st.session_state["rInput"] = ""

    def run(self):
        with st.form("Feedback Form"):
            col1, col2, col3 = st.columns(3)

            dInput = col1.radio("Satisfaction With Doctor", ["Yes", "No"], key="dInput")
            nInput = col2.radio("Satisfaction With Nurse", ["Yes", "No"], key="nInput")
            mInput = col3.radio("Medicine Given Timely", ["Yes", "No"], key="mInput")

            mCInput = st.text_area("Medical Complains", key="mCInput")
            aOInput = st.text_area("Any Other Complains", key="aOInput")

            fInput = st.radio(
                "Overall Feedback Type",
                ["Positive", "Negative", "No Comments"],
                horizontal=True,
                key="fInput",
            )
            rInput = st.text_area("Any Other Remarks", key="rInput")
            st.form_submit_button("Submit", on_click=self.saveONDB)


class OTForm:
    def __init__(self, currDate):
        self.currDate = currDate
        self.ot = [
            "Select",
            "OPERATION THEATRE",
            "CARDIAC OPERATION THEATER",
            "Post Operative Ward",
            "OPERATIONS",
        ]

    def saveONDB(self):
        conn, cur = initDb()
        result = cur.execute("""SELECT MAX(ID) FROM DETAILS""")
        id = result.fetchone()[-1]
        cur.execute(
            f"""INSERT INTO DETAILS VALUES({int(id+1)}, "{st.session_state['OT']}", "", "", "", "", "", "", "", "", "", "", "", "","", "", "", "", "", "", "", "",'{st.session_state['complains']}', '{st.session_state['actionTaken']}')"""
        )
        conn.commit()
        conn.close()

        st.session_state["OT"] = "Select"
        st.session_state["complains"] = ""
        st.session_state["actionTaken"] = ""

    def run(self):
        with st.form("OT Form"):
            ot = st.selectbox("OT", self.ot, key="OT")
            complains = st.text_area("Complains", key="complains")
            action = st.text_area("Actions Taken", key="actionTaken")

            button = st.form_submit_button("Save", on_click=self.saveONDB)


if __name__ == "__main__":
    if LoginFunction():
        date = st.date_input("Date", key="currDate")

        wardFeedback, otFeedback = st.tabs(["Ward Feedback", "OT Feedback"])

        with wardFeedback:
            fform = FeedbackFunction()
            fform.run()
            form = Form(date)
            form.run()

        with otFeedback:
            otform = OTForm(date)
            otform.run()
