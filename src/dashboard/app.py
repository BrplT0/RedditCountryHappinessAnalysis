import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
LIVE_DIR = PROJECT_ROOT / "data" / "dashboard" / "live"
TIMESERIES_DIR = PROJECT_ROOT / "data" / "dashboard" / "time_series"

st.set_page_config(
    page_title="Reddit Country Happiness Index",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_data():
    live_files = list(LIVE_DIR.glob("*.csv"))
    if not live_files:
        return None, None, None

    live_file_to_load = live_files[0]

    try:
        df_live = pd.read_csv(live_file_to_load)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return None, None, None

    ts_files = list(TIMESERIES_DIR.glob("*.csv"))
    all_timeseries_data = []

    if not ts_files:
        df_timeseries = df_live.copy()
        df_timeseries['Date'] = pd.to_datetime(live_file_to_load.stem)
    else:
        for file_path in ts_files:
            try:
                df = pd.read_csv(file_path)
                df['Date'] = pd.to_datetime(file_path.stem)
                all_timeseries_data.append(df)
            except Exception:
                continue

        df_live_with_date = df_live.copy()
        df_live_with_date['Date'] = pd.to_datetime(live_file_to_load.stem)
        all_timeseries_data.append(df_live_with_date)

        df_timeseries = pd.concat(all_timeseries_data, ignore_index=True)
        df_timeseries = df_timeseries.sort_values(by='Date')

    return df_live, df_timeseries, live_file_to_load


df_live, df_timeseries, df_live_path = load_data()

st.title("🌍 Reddit Country Happiness Index")
st.markdown("This dashboard visualizes weekly sentiment changes across countries based on Reddit comments.")

if df_live is None or df_live.empty:
    st.error("❌ Live data not found. Please run the `main.py` pipeline first.")
    st.stop()

st.header("Current Happiness Map")
st.markdown(f"Most recent data from (`{df_live_path.name}`)")

try:
    fig_map = px.choropleth(
        df_live,
        locations="country",
        locationmode="country names",
        color="happiness_value",
        hover_name="country",
        hover_data={"happiness_value": ':.2f', "country": False},
        color_continuous_scale="RdYlGn",
        range_color=[-1, 1],
        labels={'happiness_value': 'Happiness Score (-1 to +1)'}
    )

    fig_map.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(bgcolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig_map, use_container_width=True)

except Exception as e:
    st.error(f"An error occurred while drawing the map: {e}")

if not df_timeseries.empty:
    st.header("Country-Specific Time Series Trend")

    country_list = sorted(df_timeseries['country'].unique())
    selected_country = st.selectbox(
        "Select a country to see its trend:",
        country_list
    )

    if selected_country:
        df_trend = df_timeseries[df_timeseries['country'] == selected_country].copy()

        fig_trend = px.line(
            df_trend,
            x='Date',
            y='happiness_value',
            title=f"Happiness Trend for {selected_country}",
            markers=True,
            labels={'happiness_value': 'Happiness Score', 'Date': 'Date'}
        )

        fig_trend.update_yaxes(range=[-1, 1])
        st.plotly_chart(fig_trend, use_container_width=True)

else:
    st.info("Historical time series data is not yet available.")