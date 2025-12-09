import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="eCommerce Funnel Dashboard", layout="wide")

st.title("🛒 eCommerce Funnel Performance Dashboard")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload your CSV", type=["csv"])
use_sample = st.sidebar.checkbox("Use sample data", value=not uploaded_file)

# Load data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Synthetic fallback data
    data = {
        "Event": [
            "Checkout Started", "Product Viewed", "Product Added", "Other events",
            "Checkout Started", "[Auto] Page View", "Product Viewed", "Other events",
            "Checkout Started", "Product Added", "Product Viewed", "Other events",
            "Sign Up Completed", "Product Viewed", "Checkout Started", "Sign Up Completed",
            "Other events", "Drop-off", "Product Viewed", "Checkout Started",
            "Products Searched", "Other events", "Drop-off", "Product Viewed",
            "Checkout Started", "Product Added", "Other events", "Drop-off"
        ],
        "Conversion %": [
            11.44, 10.63, 8.9, 10.8,
            13.82, 11.1, 9.64, 18.35,
            15.89, 10.12, 8.4, 27.0,
            100.0, 54.99, 11.07, 8.24,
            22.69, 3.0, 42.01, 15.07,
            8.56, 29.18, 5.19, 37.43,
            17.73, 9.22, 28.42, 7.2
        ],
        "Count": [
            801, 744, 623, 756,
            967, 777, 675, 1284,
            1112, 708, 588, 1890,
            6999, 3849, 775, 577,
            1588, 210, 2940, 1055,
            599, 2042, 363, 2620,
            1241, 645, 1989, 504
        ]
    }
    df = pd.DataFrame(data)

# Clean column names
df.columns = df.columns.str.strip()

# Summary KPIs
st.subheader("🔢 KPI Overview")
col1, col2, col3 = st.columns(3)
total_events = df["Count"].sum()
avg_conversion = df["Conversion %"].mean()
checkout_started = df[df["Event"].str.contains("Checkout", case=False)]["Count"].sum()

col1.metric("Total Events", f"{total_events:,}")
col2.metric("Avg Conversion %", f"{avg_conversion:.2f}%")
col3.metric("Total Checkouts", f"{checkout_started:,}")

# Funnel chart
st.subheader("📊 Funnel Stage Breakdown")
funnel_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("Event", sort="-y", title="Funnel Event"),
        y=alt.Y("Count", title="Event Count"),
        tooltip=["Event", "Count", "Conversion %"]
    )
    .properties(height=400)
)
st.altair_chart(funnel_chart, use_container_width=True)

# Conversion line chart
st.subheader("📈 Conversion Rates by Event")
line_chart = (
    alt.Chart(df)
    .mark_line(point=True)
    .encode(
        x=alt.X("Event", sort=None),
        y=alt.Y("Conversion %", title="Conversion Rate"),
        tooltip=["Event", "Conversion %"]
    )
    .properties(height=300)
)
st.altair_chart(line_chart, use_container_width=True)

# Drop-off table
st.subheader("🚨 Drop-off Analysis")
drop_df = df[df["Event"].str.contains("drop-off", case=False)]
if drop_df.empty:
    st.info("No drop-off events found.")
else:
    st.dataframe(drop_df, use_container_width=True)

# Raw preview
with st.expander("🔍 Raw Data"):
    st.dataframe(df, use_container_width=True)
