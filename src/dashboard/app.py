import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from streamlit.config import get_option

PROJECT_ROOT = Path(__file__).parent.parent.parent
LIVE_DIR = PROJECT_ROOT / "data" / "dashboard" / "live"
TIMESERIES_DIR = PROJECT_ROOT / "data" / "dashboard" / "time_series"

st.set_page_config(
    page_title="Reddit Happiness Index",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1400px;
    }

    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #1f77b4;
    }

    [data-testid="stMetricDelta"] {
        font-size: 16px;
        font-weight: 600;
    }

    h1 {
        font-weight: 800;
        font-size: 2.8rem !important;
        padding-bottom: 0.5rem;
        background: linear-gradient(120deg, #1f77b4, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h2 {
        font-weight: 700;
        font-size: 1.8rem !important;
        padding-top: 1.5rem;
        padding-bottom: 0.5rem;
    }

    h3 {
        font-weight: 600;
        padding-top: 1rem;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 1.2rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(240, 242, 246, 0.8) 0%, rgba(240, 242, 246, 0.4) 100%);
        padding-top: 2rem;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    .stSelectbox label {
        font-weight: 600;
        font-size: 1rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 1rem;
        padding: 0.5rem 1.5rem;
    }

    hr {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        border: none;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }

    @media (prefers-color-scheme: dark) {
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(20, 25, 35, 0.9) 0%, rgba(20, 25, 35, 0.4) 100%);
        }

        [data-testid="stMetricValue"] {
            color: #58a6ff;
        }

        hr {
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
    }

    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    .metric-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)


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
        if not df_timeseries.empty:
            try:
                df_timeseries['Date'] = pd.to_datetime(live_file_to_load.stem)
            except Exception:
                df_timeseries['Date'] = pd.NaT
    else:
        for file_path in ts_files:
            try:
                df = pd.read_csv(file_path)
                df['Date'] = pd.to_datetime(file_path.stem)
                all_timeseries_data.append(df)
            except Exception:
                continue

        df_live_with_date = df_live.copy()
        try:
            df_live_with_date['Date'] = pd.to_datetime(live_file_to_load.stem)
            all_timeseries_data.append(df_live_with_date)
        except Exception:
            pass

        if all_timeseries_data:
            df_timeseries = pd.concat(all_timeseries_data, ignore_index=True)
            df_timeseries = df_timeseries.sort_values(by='Date')
        else:
            df_timeseries = pd.DataFrame(columns=['country', 'happiness_value', 'Date'])

    return df_live, df_timeseries, live_file_to_load


df_live, df_timeseries, df_live_path = load_data()

col1, col2 = st.columns([3, 1])
with col1:
    st.title("🌍 Reddit Happiness Index")
    st.markdown(
        '<p class="subtitle">Real-time sentiment analysis across countries based on Reddit community discussions</p>',
        unsafe_allow_html=True)

with col2:
    if df_live is not None and not df_live.empty:
        st.metric(
            label="Countries Tracked",
            value=len(df_live),
            delta=f"Updated {df_live_path.name[:10]}" if df_live_path else "Today"
        )

if df_live is None or df_live.empty:
    st.error("❌ Live data not found. Please run the `main.py` pipeline first.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_happiness = df_live['happiness_value'].mean()
    st.metric(
        label="🌟 Global Average",
        value=f"{avg_happiness:.3f}",
        delta=f"{avg_happiness:+.3f}" if avg_happiness != 0 else "0.000"
    )

with col2:
    happiest = df_live.loc[df_live['happiness_value'].idxmax()]
    st.metric(
        label="😊 Happiest Country",
        value=happiest['country'],
        delta=f"{happiest['happiness_value']:.3f}"
    )

with col3:
    saddest = df_live.loc[df_live['happiness_value'].idxmin()]
    st.metric(
        label="😔 Lowest Score",
        value=saddest['country'],
        delta=f"{saddest['happiness_value']:.3f}",
        delta_color="inverse"
    )

with col4:
    score_range = df_live['happiness_value'].max() - df_live['happiness_value'].min()
    st.metric(
        label="📊 Score Range",
        value=f"{score_range:.3f}",
        delta="Variance"
    )

st.divider()

with st.sidebar:
    st.header("⚙️ Filters & Settings")

    st.subheader("Happiness Score Range")
    score_filter = st.slider(
        "Filter by score",
        min_value=-1.0,
        max_value=1.0,
        value=(-1.0, 1.0),
        step=0.1,
        label_visibility="collapsed"
    )

    st.subheader("Quick Stats")
    show_top = st.number_input("Show top N countries", min_value=5, max_value=20, value=10)

    st.divider()

    st.caption(f"📅 Last updated: {df_live_path.name[:10] if df_live_path else 'Unknown'}")
    st.caption(f"📊 Total countries: {len(df_live)}")
    st.caption(f"🕒 Data points: {len(df_timeseries) if not df_timeseries.empty else 'N/A'}")

df_filtered = df_live[
    (df_live['happiness_value'] >= score_filter[0]) &
    (df_live['happiness_value'] <= score_filter[1])
    ]

tab1, tab2, tab3 = st.tabs(["🗺️ Global Map", "📊 Rankings", "📈 Trends"])

with tab1:
    st.subheader("Interactive World Happiness Map")

    current_theme = get_option("theme.base")
    is_dark = current_theme == "dark"
    plotly_template = "plotly_dark" if is_dark else "plotly_white"

    bg_color = "rgba(14, 17, 23, 0)" if is_dark else "rgba(255, 255, 255, 0)"
    grid_color = "rgba(255, 255, 255, 0.1)" if is_dark else "rgba(0, 0, 0, 0.1)"

    try:
        fig_map = px.choropleth(
            df_filtered,
            locations="country",
            locationmode="country names",
            color="happiness_value",
            hover_name="country",
            hover_data={"happiness_value": ':.3f', "country": False},
            color_continuous_scale="RdYlGn",
            color_continuous_midpoint=0,
            range_color=[-1, 1],
            labels={'happiness_value': 'Happiness Score'},
            template=plotly_template
        )

        fig_map.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            geo=dict(
                bgcolor=bg_color,
                showframe=False,
                showcountries=True,
                countrycolor=grid_color,
                projection_type='natural earth',
                showlakes=False,
                coastlinecolor=grid_color
            ),
            coloraxis_colorbar=dict(
                title="Score",
                thickness=20,
                len=0.7,
                bgcolor=bg_color,
                tickfont=dict(size=12),
                x=1.02
            ),
            height=600,
            hoverlabel=dict(
                bgcolor="white" if not is_dark else "#1e1e1e",
                font_size=13,
                font_family="Arial"
            )
        )

        st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})

    except Exception as e:
        st.error(f"⚠️ Error rendering map: {e}")

with tab2:
    st.subheader("Country Rankings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### 🏆 Top {show_top} Happiest Countries")
        top_countries = df_filtered.nlargest(show_top, 'happiness_value')

        fig_top = go.Figure()
        fig_top.add_trace(go.Bar(
            x=top_countries['happiness_value'],
            y=top_countries['country'],
            orientation='h',
            marker=dict(
                color=top_countries['happiness_value'],
                colorscale='Greens',
                showscale=False
            ),
            text=top_countries['happiness_value'].round(3),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>'
        ))

        fig_top.update_layout(
            template=plotly_template,
            height=400,
            margin=dict(l=0, r=40, t=20, b=0),
            xaxis_title="Happiness Score",
            yaxis=dict(autorange="reversed"),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            showlegend=False
        )

        st.plotly_chart(fig_top, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown(f"#### 📉 Bottom {show_top} Countries")
        bottom_countries = df_filtered.nsmallest(show_top, 'happiness_value')

        fig_bottom = go.Figure()
        fig_bottom.add_trace(go.Bar(
            x=bottom_countries['happiness_value'],
            y=bottom_countries['country'],
            orientation='h',
            marker=dict(
                color=bottom_countries['happiness_value'],
                colorscale='Reds',
                showscale=False
            ),
            text=bottom_countries['happiness_value'].round(3),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>'
        ))

        fig_bottom.update_layout(
            template=plotly_template,
            height=400,
            margin=dict(l=0, r=40, t=20, b=0),
            xaxis_title="Happiness Score",
            yaxis=dict(autorange="reversed"),
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            showlegend=False
        )

        st.plotly_chart(fig_bottom, use_container_width=True, config={'displayModeBar': False})

    st.markdown("#### 📊 Score Distribution")
    fig_hist = px.histogram(
        df_filtered,
        x='happiness_value',
        nbins=30,
        labels={'happiness_value': 'Happiness Score', 'count': 'Number of Countries'},
        template=plotly_template,
        color_discrete_sequence=['#1f77b4']
    )

    fig_hist.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=20, b=0),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        showlegend=False,
        bargap=0.1
    )

    st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})

with tab3:
    if not df_timeseries.empty:
        st.subheader("Historical Trends Analysis")

        col1, col2 = st.columns([2, 1])

        with col1:
            country_list = sorted(df_timeseries['country'].unique())
            selected_country = st.selectbox(
                "🔍 Select a country to analyze trends",
                country_list,
                index=0
            )

        with col2:
            if selected_country:
                df_country = df_timeseries[df_timeseries['country'] == selected_country].copy()
                if len(df_country) > 1:
                    trend_change = df_country['happiness_value'].iloc[-1] - df_country['happiness_value'].iloc[0]
                    st.metric(
                        "Overall Change",
                        f"{trend_change:+.3f}",
                        delta=f"{(trend_change / abs(df_country['happiness_value'].iloc[0]) * 100):+.1f}%" if
                        df_country['happiness_value'].iloc[0] != 0 else "N/A"
                    )

        if selected_country:
            df_trend = df_timeseries[df_timeseries['country'] == selected_country].copy()

            fig_trend = go.Figure()

            fig_trend.add_trace(go.Scatter(
                x=df_trend['Date'],
                y=df_trend['happiness_value'],
                mode='lines+markers',
                name=selected_country,
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=8, color='#1f77b4', line=dict(width=2, color='white')),
                hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Score: %{y:.3f}<extra></extra>'
            ))

            avg_line = df_trend['happiness_value'].mean()
            fig_trend.add_hline(
                y=avg_line,
                line_dash="dash",
                line_color="gray",
                opacity=0.5,
                annotation_text=f"Average: {avg_line:.3f}",
                annotation_position="right"
            )

            fig_trend.update_layout(
                title=f"Happiness Trend for {selected_country}",
                template=plotly_template,
                height=500,
                margin=dict(l=0, r=0, t=40, b=0),
                xaxis_title="Date",
                yaxis_title="Happiness Score",
                yaxis=dict(range=[-1, 1]),
                paper_bgcolor=bg_color,
                plot_bgcolor=bg_color,
                hovermode='x unified',
                showlegend=False
            )

            st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Average Score", f"{df_trend['happiness_value'].mean():.3f}")
            with col2:
                st.metric("Highest", f"{df_trend['happiness_value'].max():.3f}")
            with col3:
                st.metric("Lowest", f"{df_trend['happiness_value'].min():.3f}")
            with col4:
                st.metric("Std Dev", f"{df_trend['happiness_value'].std():.3f}")
    else:
        st.info("📊 Historical time series data is not yet available. Run more data collection cycles to see trends!")

st.divider()
st.caption("🔄 Dashboard auto-refreshes with new data • Built with Streamlit & Plotly • Data source: Reddit API")