import streamlit as st

st.set_page_config(page_title="SIMS Feedback", layout="wide")

import plotly.express as px
import streamlit as st
import pandas as pd
import sqlite3


def fetchDB():
    con = sqlite3.connect("sqlite.db")
    df = pd.read_sql_query("SELECT * FROM FEEDBACKFORM", con, index_col="IPID")
    con.close()
    df["DATE_OF_FEEDBACK"] = pd.to_datetime(df["DATE_OF_FEEDBACK"])
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
        date = self.df["DATE_OF_FEEDBACK"].sort_values()

        lineValues = date.dt.date.value_counts()
        lineChart = px.line(
            x=date,
            title="Time Series Plot",
            labels={"x": "Date", "y": "Count"},
        )
        st.plotly_chart(lineChart, use_container_width=True)

        col1, col2, col3 = st.tabs(["Date", "Month", "Year"])
        dailyChart = px.bar(
            date.dt.date,
            labels={"id": "Date", "value": "Count"},
            title="Count Plot on Daily Basis",
        )
        col1.plotly_chart(dailyChart, use_container_width=True)
        monthlyChart = px.bar(
            date.dt.month.value_counts(),
            labels={"id": "Month", "value": "Count"},
            title="Count Plot Based on Month",
        )
        col2.plotly_chart(monthlyChart)

        yearChart = px.bar(
            date.dt.year.value_counts(),
            labels={"id": "Year", "value": "Count"},
            title="Count Plot Based on Year",
        )
        col3.plotly_chart(yearChart, use_container_width=True)

        doctorChart, nurserChart, medicineChart, overAllFeedback = st.tabs(
            [
                "Satisfaction With Doctor",
                "Satisfaction With Nurse",
                "Medicine Given Timely",
                "Over All Feedback",
            ]
        )
        pieChart1 = px.histogram(
            self.df["SATISFACTION_WITH_DOCTOR"],
            title="Satisfaction With Doctor",
            labels={"value": "Yes Or No", "count": "Count"},
        )
        doctorChart.plotly_chart(pieChart1, use_container_width=True)

        pieChart2 = px.histogram(
            self.df["SATISFACTION_WTIH_NURSE"],
            title="Satisfaction With Nurse",
            labels={"value": "Yes Or No", "count": "Count"},
        )
        nurserChart.plotly_chart(pieChart2, use_container_width=True)

        pieChart3 = px.histogram(
            self.df["MEDICINE_GIVEN_TIMELY"],
            title="Medicine Given Timely",
            labels={"value": "Yes Or No", "count": "Count"},
        )
        medicineChart.plotly_chart(pieChart3, use_container_width=True)

        pieChart4 = px.histogram(
            self.df["FEEDBACK_TYPE"],
            title="Over All Feedback",
            labels={"value": "Postivie - Negative - No Comments", "count": "Count"},
        )
        overAllFeedback.plotly_chart(pieChart4, use_container_width=True)


if __name__ == "__main__":
    dashboard = DashBoardView()
    dashboard.run()
