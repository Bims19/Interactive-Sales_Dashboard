import pandas as pd 
import plotly.express as px
import streamlit as st

#-------Based Config for Web page-------
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

#----------------DataFrame Cache--------------\
#----------------Start-------------------
@st.cache
def get_data_from_excel():
    df =pd.read_excel(
        io='supermarket_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )
    #----------DataFrame (Display Hour Column)---------------
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df
#-----------Call function to return the data frame and variable-----------
df = get_data_from_excel()
#------------------End-----------------------

#------------Create Side Bar & Filter Data Set Based On City, Customer Type, & Gender---------
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select City",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select Customer Type",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

#-------Data Frame Filter Method--------
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)


#---------Main Page Data KPI------------
st.title(":bar_chart: Interactive Sales Dashboard")
#---------Separate Title from KPI-------
st.markdown('##')

#----------Top KPI-------------
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

#----------Use 3 Columns to insert the figures beside each other------------
left_column, right_column  = st.columns(2)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"CAD $ {total_sales:,}")
with right_column:
    st.subheader("Average Sale Per Transaction:")
    st.subheader(f"CAD $ {average_sale_by_transaction}")


#----------Use divider to separate sections-------------
st.markdown("_ _ _")

#---------------Bar Chart 1 (Horizontal)--------------
#--------------Sales by Product Line-------------
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales By Product</b>",
    color_discrete_sequence=["#FFDF00"] * len(sales_by_product_line),
    template="plotly_white",
)

#-------------Edit Bar Chart 1 Layout------------
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#-------------Create or Plot Bar Chart 1-------------
#st.plotly_chart(fig_product_sales)

#--------------Bar Chart 2 (Sales By Hour)-----------------------
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Hourly Sales</b>",
    #color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    color_discrete_sequence=["#FFDF00"] * len(sales_by_hour),
    template="plotly_white",
)

#-------------Edit Bar Chart 2 Layout------------
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

#----------------Create or Plot Both Bar Charts Beside Each Other----------
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

#----------------Customer CSS To Hide Streamlit Style--------------
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)



