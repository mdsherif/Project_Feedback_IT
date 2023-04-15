import streamlit as st
import pandas as pd

from utilty import initDb

st.set_page_config(layout="wide")


def firstLoad():
    conn, cur = initDb()

    fromDate = st.session_state["fromDate"]
    toDate = st.session_state["toDate"]

    df = pd.read_sql_query("""SELECT * FROM FEEDBACKFORM;""", conn)
    df["DATE_OF_FEEDBACK"] = pd.to_datetime(df["DATE_OF_FEEDBACK"])
    df = df[df["DATE_OF_FEEDBACK"].isin(pd.date_range(fromDate, toDate))]

    conn.close()

    return df


# def changeIp():
#     fromDate = st.session_state["fromDate"]
#     toDate = st.session_state["toDate"]
#     conn, cur = initDb()
#     keyword = st.session_state["changeIp"]
#     print(keyword)
#     df = pd.read_sql_query(
#         f"""SELECT * FROM FEEDBACKFORM WHERE IPID = {keyword}""", conn
#     )
#     df["DATE_OF_FEEDBACK"] = pd.to_datetime(df["DATE_OF_FEEDBACK"])
#     df = df[df["DATE_OF_FEEDBACK"].isin(pd.date_range(fromDate, toDate))]
#     st.session_state["df"] = df
#     conn.close()


def loadDf(df):
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9, gap="small")

    col1.text_input("IPID", key="changeIp")
    col2.text_input("Feedback Date")
    col3.text_input("Sat With Doctor")
    col4.text_input("Sat With Nurse")
    col5.text_input("Medicine Given Timely")
    col6.text_input("Complains")
    col7.text_input("Any Other Complains")
    col8.text_input("Feedback Type")
    col9.text_input("Remarks")

    return df


def genReport():
    df = firstLoad()
    df = df.reset_index(drop=True)

    csvFile = df.to_csv().encode("utf-8")

    df.to_excel("temp.xlsx")
    with open("./temp.xlsx", "rb") as template_file:
        template_byte = template_file.read()

    copy, csv, excel, _, _, _, _, _, _, _, _, _, _, _ = st.columns(14)

    copy.button("COPY", on_click=df.to_clipboard)

    csv.download_button(
        label="CSV",
        data=csvFile,
        file_name="Data.csv",
        mime="text/csv",
    )
    excel.download_button(
        label="Excel",
        data=template_byte,
        file_name="Data.xlsx",
        mime="application/octet-stream",
    )

    st.session_state["df"] = loadDf(df)

    st.dataframe(st.session_state["df"])


if __name__ == "__main__":
    col1, col2 = st.columns(2)

    fromDate = col1.date_input("From", key="fromDate")
    toDate = col2.date_input("To", key="toDate")

    genBtn = st.button("Generate")

    if genBtn:
        genReport()
