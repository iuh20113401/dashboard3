
import hmac
import tkinter as TK
from pydoc import classname
from turtle import width
from cv2 import sort
import seaborn as sns
from dash import Dash, html, dcc
from matplotlib.pyplot import cla, tight_layout
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate(
    "./iuh-20113401-firebase-adminsdk-fafgb-58aa6e1fe0.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()
queryResults = list(dbFireStore.collection(
    u'tbl-20113401').where(u'DEALSIZE', u'==', 'Large').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))
df = pd.DataFrame(listQueryResult)
df["YEAR_ID"] = df["YEAR_ID"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")
df['profit'] = df["SALES"]-(df["QUANTITYORDERED"]*df['PRICEEACH'])
ds = pd.DataFrame(df.groupby(['YEAR_ID'], as_index=False)[
    'SALES'].sum())
ds_cat = pd.DataFrame(df.groupby(['YEAR_ID', "CATEGORY"], as_index=False)[
    'SALES'].sum())
profit_group = df.groupby(['MONTH_ID', 'YEAR_ID'], as_index=False)[
    'profit'].sum()
profit_group = pd.DataFrame(profit_group)
cag_group = df.groupby(['YEAR_ID', "CATEGORY"], as_index=False)[
    'profit'].sum()
cag_group = pd.DataFrame(cag_group)
app = Dash(__name__)
figds = px.bar(ds, x="YEAR_ID", y="SALES", color="YEAR_ID", labels={
               'YEAR_ID': 'Năm', 'SALES': 'Doanh số'}, title='Tổng doanh số theo năm')

figLoiNhuan = px.line(profit_group, x="MONTH_ID", y="profit", line_group="YEAR_ID", color="YEAR_ID", labels={
                      'YEAR_ID': 'Năm', 'profit': 'Lợi Nhuận'}, title='Lợi nhuận theo năm')
figdsCa = px.sunburst(
    ds_cat, path=['YEAR_ID', 'CATEGORY'], values='SALES', color='SALES', labels={'parent': 'Năm', 'labels': 'Doanh mục', 'SALES_sum': 'tổng lợi nhuận', 'SALES': "Doanh thu"},
    title='Tỉ lệ đóng góp của doanh thu theo từng doanh mục trong năm')
figLnCag = px.sunburst(cag_group, path=['YEAR_ID', 'CATEGORY'], values='profit', color='profit', labels={'parent': 'Năm', 'labels': 'Doanh mục', 'profit_sum': 'tổng lợi nhuận', 'profit': "Lợi Nhuận"},
                       title='Tỉ lệ đóng góp của lợi nhuận theo từng doanh mục trong năm')
figds.update_layout(
    margin=dict(l=50, r=50, t=50, b=50),
)
figLoiNhuan.update_layout(
    margin=dict(l=50, r=50, t=50, b=50),
)
figdsCa.update_layout(
    margin=dict(l=50, r=50, t=50, b=50),
)
figLnCag.update_layout(
    margin=dict(l=30, r=30, t=50, b=30),
)
doanhso = df["SALES"].sum()
loinhuan = df['profit'].sum()
topdoanhso = df['SALES'].max()
toploinhuan = df["profit"].max()
app.layout = html.Div(
    children=[
        html.Div
        (
            children=[
                html.P(
                    children="Xây dựng danh mục sản phẩm tiềm năng",
                    className="header-description2"
                ),
                html.P(
                    children="Đại học công nghiệp thành phố Hồ Chí Minh-DHHTTT16A-20113401-Nguyễn Tuấn Kiệt",
                    className="header-description3"
                )], className='header2'
        ),
        html.Div
        (
            children=[
                html.Div(
                    children=[html.P(
                        children="Doanh số SALES ",
                        className="title"
                    ),
                        html.P
                        (
                        children=str(doanhso),
                        className="slieu"
                    )], className='header-description'
                ),
                html.Div(
                    children=[html.P(
                        children=("Lợi nhuận"),
                        className="title"

                    ),
                        html.P
                        (
                        children=str(loinhuan),
                        className="slieu"

                    )], className='header-description'
                ),
                html.Div(
                    children=[html.P(
                        children=("Top doanh số"),
                        className="title"

                    ),
                        html.P
                        (
                        children=str(topdoanhso),
                        className="slieu"

                    )], className='header-description'
                ),
                html.Div(
                    children=[html.P(
                        children=("Top lợi nhuận"),
                        className="title"

                    ),
                        html.P
                        (
                        children=str(toploinhuan),
                        className="slieu"

                    )], className='header-description'
                ),
            ], className='menu'
        ),
        html.Div(
            children=[

                html.Div(
                    children=dcc.Graph(
                        id='doanhso-graph',
                        figure=figds),
                    className="card"
                ),
                html.Div(
                    children=dcc.Graph(
                        id='doanhso-graph2',
                        figure=figdsCa),
                    className="card"
                ),
                html.Div(
                    children=dcc.Graph(
                        id='doanhso-graph3',
                        figure=figLoiNhuan),
                    className="card"
                ),
                html.Div(
                    children=dcc.Graph(
                        id='doanhso-graph4',
                        figure=figLnCag),
                    className="card"
                ),

            ], className="wrapper2")
    ])
if __name__ == '__main__':
    app.run_server(debug=True, port=8090)
