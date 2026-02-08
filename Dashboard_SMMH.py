import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Mental Health & Social Media Dashboard",
    layout="wide"
)

st.title("📱 Mental Health & Social Media Dashboard")
st.markdown("Analyzing the impact of social media usage on mental health")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("mental_health_social_media_dataset.csv")

    # لو فيه عمود تاريخ
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    return df

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("🔍 Filters")

gender = st.sidebar.multiselect(
    "Gender",
    df['gender'].unique(),
    df['gender'].unique()
)

platform = st.sidebar.multiselect(
    "Platform",
    df['platform'].unique(),
    df['platform'].unique()
)

mental_state = st.sidebar.multiselect(
    "Mental State",
    df['mental_state'].unique(),
    df['mental_state'].unique()
)

df = df[
    df['gender'].isin(gender) &
    df['platform'].isin(platform) &
    df['mental_state'].isin(mental_state)
]

# --------------------------------------------------
# KPIs
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Users", df.shape[0])
col2.metric("⏱ Avg Screen Time (min)", round(df['daily_screen_time_min'].mean(), 1))
col3.metric("😰 Avg Anxiety Level", round(df['anxiety_level'].mean(), 2))
col4.metric("😴 Avg Sleep Hours", round(df['sleep_hours'].mean(), 2))

st.markdown("---")

# --------------------------------------------------
# First Row
# --------------------------------------------------
c1, c2, c3 = st.columns(3)

# Screen Time Distribution
with c1:
    fig = px.histogram(
        df,
        x="daily_screen_time_min",
        nbins=20,
        title="Daily Screen Time Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Insights"):
        st.write("""
        - Most users spend between 100 to 300 minutes on their devices daily.
        - A smaller group spends over 600 minutes, indicating potential overuse.
        """)

# Anxiety vs Screen Time
with c2:
    fig = px.scatter(
        df,
        x="daily_screen_time_min",
        y="anxiety_level",
        color="platform",
        title="Screen Time vs Anxiety Level"
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Insights"):
        st.write("""
        - There is a positive correlation between screen time and anxiety levels.
        - Users on certain platforms tend to report higher anxiety with increased screen time.
        """)

# Stress vs Sleep
with c3:
    fig = px.scatter(
        df,
        x="sleep_hours",
        y="stress_level",
        color="gender",
        title="Sleep Hours vs Stress Level"
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Insights"):
        (st.write("""
        - Lower sleep hours are associated with higher stress levels.
        - Users with less sleep tend to report higher stress.
        """))

# --------------------------------------------------
# Second Row
# --------------------------------------------------
c4, c5, c6 = st.columns(3)

# Platform Usage
with c4:
    platform_counts = df['platform'].value_counts().reset_index()
    platform_counts.columns = ['platform', 'count']

    fig = px.bar(
        platform_counts,
        x='platform',
        y='count',
        title="Platform Usage Distribution",
        labels={'platform': 'Platform', 'count': 'Number of Users'}
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Insights"):
        st.write("""
        - The most popular platform among users is Instagram, followed by Facebook and Twitter.
        - Platform preference may influence mental health outcomes.
        """)

# Mental State Distribution
with c5:
    fig = px.pie(
        df,
        names='mental_state',
        title="Mental State Distribution",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Insights"):
        st.write("""
        The figure illustrates the distribution of mental health states within the dataset, where the “Stressed” category represents the largest proportion of individuals, 
        while the “At_Risk” category appears with a small percentage but holds significant importance, highlighting the need for data balancing and close monitoring of at-risk cases.
        """)

# Mood Level by Platform
with c6:
    fig = px.box(
        df,
        x='platform',
        y='mood_level',
        title="Mood Level by Platform"
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Insights"):
        st.write("""
        - Mood levels vary across different social media platforms.
        - Some platforms show a wider range of mood levels among users.
        """)

# --------------------------------------------------
# Third Row
# --------------------------------------------------
st.markdown("### 📊 Advanced Analysis")

c7, c8 = st.columns(2)

# Physical Activity vs Anxiety
with c7:
    fig = px.scatter(
        df,
        x="physical_activity_min",
        y="anxiety_level",
        color="mental_state",
        title="Physical Activity vs Anxiety Level"
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Insights"):
        st.write("""
        - Increased physical activity is associated with lower anxiety levels.
        - Encouraging regular exercise may help improve mental health.
        """)

# Social Media Time vs Mood
with c8:
    fig = px.scatter(
        df,
        x="social_media_time_min",
        y="mood_level",
        color="platform",
        title="Social Media Time vs Mood Level"
    )
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Insights"):
        st.write("""
        - Higher social media usage tends to correlate with lower mood levels.
        - Different platforms impact mood in varying ways.
        """)
# --------------------------------------------------
# Raw Data
# --------------------------------------------------
with st.expander("📂 Show Raw Data"):
    st.dataframe(df)
