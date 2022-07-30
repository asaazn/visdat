import io
from numpy import average
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import plotly.graph_objects as go

# streamlit page configuration
st.set_page_config(page_title="1900018412 - Arif Setia Aji",
                   page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
st.title(":bar_chart: Dashboard Penindakan Pelanggaran Lalu Lintas dan Angkutan Jalan Tahun 2021 bulan Juli")
st.markdown("##")
st.header("Tabel Data Penindakan Pelanggaran Lalu Lintas dan Angkutan Jalan Tahun 2021 bulan Juli")
@st.cache  # using cache to load data from excel
def get_data_from_excel():
    df = pd.read_excel(
        io="datapelanggaranlalinjuli2021.xlsx",
        engine="openpyxl",
        sheet_name="Sheet",
        skiprows=0,
        usecols="A:Z",
        nrows=7,
    )
    # Add 'hour' column to datetime
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df


df = get_data_from_excel()
st.dataframe(df)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
wilayah = st.sidebar.multiselect(
    "Select Wilayah:",
    options=df["wilayah"].unique(),
    default=df["wilayah"].unique()
)

# customer_type = st.sidebar.multiselect(
#     "Select the Customer Type:",
#     options=df["Customer_type"].unique(),
#     default=df["Customer_type"].unique()
# )

# gender = st.sidebar.multiselect(
#     "Select the Gender:",
#     options=df["Gender"].unique(),
#     default=df["Gender"].unique()
# )

df_selection = df.query(
    "wilayah == @wilayah"
    # "City == @city & Customer_type == @customer_type & Gender == @gender"
)
st.markdown("""---""")
# ---- MAINPAGE ----
# st.title(":bar_chart: Dashboard Data Penindakan Pelanggaran Lalu Lintas dan Angkutan Jalan Tahun 2021 bulan Januari")
# st.markdown("##")

st.header("Rekaptulasi Penindakan Bulan Juli")
# TOP KPI's
total = int(df_selection["bap_tilang"].sum())
average_rating = round(df_selection["bap_tilang"].mean(), 1)
maks = int(df_selection["bap_tilang"].max())
minim = round(df_selection["bap_tilang"].min())
# star_rating = ":star:" * int(round(average_rating, 0))
# average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, right_column, = st.columns(2)
with left_column:
    st.subheader("Total BAP Tilang:")
    st.subheader(f"{total:,}")
with right_column:
    st.subheader("Rata-rata BAP Tilang:")
    st.subheader(f"{average_rating}")

left_column, right_column, = st.columns(2)
with left_column:
    st.subheader("Total Maksimal BAP Tilang:")
    st.subheader(f"{maks}")
with right_column:
    st.subheader("Total Minimal BAP Tilang:")
    st.subheader(f"{minim}")
# with right_column:
#     st.subheader("Average Sales For Transaction:")
#     st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# (BAR CHART)
bap_tilang_line = (
    df_selection.groupby(by=["wilayah"]).sum()[
        ["bap_tilang"]].sort_values(by="bap_tilang")
)

fig_bap_tilang = px.bar(
    bap_tilang_line,
    x=bap_tilang_line.index,
    y="bap_tilang",
    orientation="v",
    title="<b>Diagram Batang Pemeriksaan Tilang</b>",
    color_discrete_sequence=["#0000FF"] * len(bap_tilang_line),
    template="plotly_white",
)

fig_bap_tilang.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_bap_tilang, use_container_width=True)

st.markdown("""---""")

# (LINE CHART)
bap_tilang_line = (
    df_selection.groupby(by=["wilayah"]).sum()[
        ["bap_tilang"]].sort_values(by="bap_tilang")
)

fig_bap_tilang = px.line(
    bap_tilang_line,
    x=bap_tilang_line.index,
    y="bap_tilang",
    orientation="h",
    title="<b>Diagram Garis Pemeriksaan Tilang</b>",
    color_discrete_sequence=["#0000FF"] * len(bap_tilang_line),
    template="plotly_white",
)

fig_bap_tilang.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=True))
)
st.plotly_chart(fig_bap_tilang, use_container_width=True)

st.markdown("""---""")

# (PIE CHART)
values = df['stop_operasi']
names = df['wilayah']

fig = px.pie(
    df,
    values = values,
    names = names,
    title = '<b>Diagram Pie Stop Operasi</b>'
)

fig.update_traces (
    textposition = 'inside',
    textinfo = 'percent'
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""---""")