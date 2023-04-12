import streamlit as st

st.set_page_config(page_title="SIMS Feedback")

import plotly.express as px
import streamlit as st
import pandas as pd
import sqlite3


def fetchDB():
    con = sqlite3.connect("sqlite.db")
    df = pd.read_sql_query("SELECT * FROM FEEDBACKFORM", con, index_col="id")
    con.close()
    df["Date_Of_Feedback"] = pd.to_datetime(df["Date_Of_Feedback"])
    return df


# columns = [
#     "Patient_IPID",
#     "Date_Of_Feedback",
#     "Satisfaction_With_Doctor",
#     "Satisfaction_With_Nurse",
#     "Medicine Given Timely",
#     "Medical",
#     "Any Other Complains",
#     "Overall_Feedback_Type",
#     "Remarks",
#     "Complains",
#     "Action_Taken",
# ]


class DashBoardView:
    def __init__(self):
        self.df = fetchDB()

    def run(self):
        self.singleFeature()

    def singleFeature(self):
        date = self.df["Date_Of_Feedback"]

        lineValues = date.dt.date.value_counts()
        lineChart = px.line(
            x=date.dt.date, title="Time Series Plot", labels={"x": "Date", "y": "Count"}
        )
        st.plotly_chart(lineChart)

        col1, col2 = st.tabs(["Month", "Year"])
        monthChart = px.bar(
            date.dt.year,
            labels={"id": "Month", "value": "Count"},
            title="Count Plot Based on Month",
        )
        col1.plotly_chart(monthChart)
        yearChart = px.bar(
            date.dt.year,
            labels={"id": "Year", "value": "Count"},
            title="Count Plot Based on Year",
        )
        col2.plotly_chart(yearChart)

        doctorChart, nurserChart, medicineChart = st.tabs(
            [
                "Satisfaction With Doctor",
                "Satisfaction With Nurse",
                "Medicine Given Timely",
            ]
        )
        pieChart = px.histogram(
            self.df["Satisfaction_With_Doctor"],
            title="Satisfaction With Doctor",
            labels={"value": "Yes Or No", "count": "Count"},
        )
        doctorChart.plotly_chart(pieChart)
        pieChart = px.histogram(
            self.df["Satisfaction_With_Nurse"],
            title="Satisfaction With Nurse",
            labels={"value": "Yes Or No", "count": "Count"},
        )
        nurserChart.plotly_chart(pieChart)
        pieChart = px.histogram(
            self.df["Medicine Given Timely"],
            title="Medicine Given Timely",
            labels={"value": "Yes Or No", "count": "Count"},
        )
        medicineChart.plotly_chart(pieChart)


# if __name__ == "__main__":
#     dashboard = DashBoardView()
#     dashboard.run()
