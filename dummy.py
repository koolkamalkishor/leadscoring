import streamlit as st
import pandas as pd
import numpy as np
import time
import google.generativeai as genai

# Configure Gemini API key
genai.configure(api_key="AIzaSyD0K-Mc4lMnxWU2CUdoHmiKgyIHlDdcjzc")  # Replace with your actual API key

# Function to generate email using Gemini LLM
def generate_email(lead_name, company, lead_score, engagement):
    prompt = f"""
    Generate a personalized follow-up email for {lead_name} from {company}.
    - Lead Score: {lead_score}/100
    - Recent Engagement: {engagement}
    - Keep it professional but engaging.
    - Include a strong Call-To-Action (CTA) such as booking a demo.
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Simulated real-time lead data
def get_lead_data():
    return pd.DataFrame({
        'Lead Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Score': np.random.randint(30, 100, 4),
        'Industry': ['Tech', 'Finance', 'Healthcare', 'Retail'],
        'Source': ['LinkedIn', 'Referral', 'Cold Call', 'Email'],
        'Conversion Probability': [f"{x}%" for x in np.random.randint(40, 90, 4)],
        'Last Contact': [time.strftime("%Y-%m-%d")] * 4
    })

# Header Section
st.title("🚀 AI-Powered Lead Scoring Dashboard")
st.sidebar.header("📅 Filters & Settings")

# Sidebar Filters
date_range = st.sidebar.date_input("Select Date Range", [])
lead_source = st.sidebar.selectbox("Lead Source", ["All", "Website", "Referral", "LinkedIn", "Email", "Event"])
industry_filter = st.sidebar.selectbox("Industry", ["All"] + list(get_lead_data()["Industry"].unique()))
score_range = st.sidebar.slider("Lead Score Range", 0, 100, (30, 100))
st.sidebar.button("Apply Filters")

# Fetch dynamic lead data
df = get_lead_data()

# Apply filters
filtered_df = df[(df["Score"] >= score_range[0]) & (df["Score"] <= score_range[1])]
if industry_filter != "All":
    filtered_df = filtered_df[filtered_df["Industry"] == industry_filter]

# KPI Metrics
st.subheader("📊 Lead Score Overview")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Leads", len(filtered_df))
col2.metric("Hot Leads", sum(filtered_df["Score"] > 80), "🔥")
col3.metric("Warm Leads", sum((filtered_df["Score"] >= 50) & (filtered_df["Score"] <= 79)), "🟡")
col4.metric("Cold Leads", sum(filtered_df["Score"] < 50), "🔴")
col5.metric("Avg Conversion Rate", f"{round(filtered_df['Conversion Probability'].apply(lambda x: int(x.strip('%'))).mean(), 2)}%")

# Lead Score Distribution Chart
st.subheader("📊 Lead Score Distribution")
lead_data = pd.DataFrame({
    "Score Range": ["0-30", "31-50", "51-80", "81-100"],
    "Count": np.random.randint(50, 300, 4)
})
st.bar_chart(lead_data.set_index("Score Range"))

# Lead Prioritization Table
st.subheader("🔍 Lead Table")
st.dataframe(filtered_df)

# Lead Engagement Timeline
with st.expander("📜 Lead Engagement Timeline"):
    st.write("📧 Email Opened - 2 days ago")
    st.write("🌐 Visited Pricing Page - 5 days ago")
    st.write("📞 Sales Rep Called - Interested in pricing")
    st.write("📅 Demo scheduled for next week")

# AI Lead Insights
def generate_ai_insights(lead_name, score, industry, source):
    prompt = f"""
    The lead '{lead_name}' has a score of {score}, from the {industry} industry, and was sourced via {source}.
    Explain why this lead got this score and suggest the best action for a sales rep.
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

st.subheader("🔬 AI-Generated Lead Explanations")
for _, row in filtered_df.iterrows():
    if st.button(f"Explain {row['Lead Name']}"):
        explanation = generate_ai_insights(row['Lead Name'], row['Score'], row['Industry'], row['Source'])
        st.info(explanation)

# AI-Generated Next Best Action (NBA)
st.subheader("📌 AI-Recommended Next Steps")
for _, row in filtered_df.iterrows():
    if row["Score"] > 80:
        action_prompt = f"What should the sales rep do next for lead '{row['Lead Name']}' with score {row['Score']}?"
        model = genai.GenerativeModel("gemini-pro")
        action_response = model.generate_content(action_prompt)
        st.success(f"🔥 {row['Lead Name']} - Suggested Action: {action_response.text}")

# AI-Based Email Generation
st.subheader("📧 AI-Based Email Generation")
selected_lead = st.selectbox("Select a Lead", filtered_df["Lead Name"].tolist())
lead_info = filtered_df[filtered_df["Lead Name"] == selected_lead].iloc[0]

if st.button("Generate Email"):
    email_content = generate_email(lead_info["Lead Name"], "Your Company", lead_info["Score"], "Recent Interaction")
    st.text_area("Generated Email", email_content, height=200)
    st.button("Copy Email")

# Lead Performance Trends
st.subheader("📈 Lead Performance Trends")
trend_data = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=10, freq="D"),
    "Leads Converted": np.random.randint(5, 20, 10)
})
st.line_chart(trend_data.set_index("Date"))

# Conversational AI for Lead Insights
st.subheader("🤖 Ask the AI Agent")
user_query = st.text_input("Ask about lead scores, recommendations, or insights...")
if user_query:
    model = genai.GenerativeModel("gemini-pro")
    chat_response = model.generate_content(user_query)
    st.write(chat_response.text)

# Export & Integration
st.subheader("📤 Export & Integrations")
st.button("Export to CSV")
st.button("Sync with Salesforce")