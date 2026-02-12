import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bank Marketing Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("bank_marketing_cleaned.csv")
df= load_data()


# ==================== SIDEBAR FILTERS ====================
st.sidebar.title("Filters")
page = st.sidebar.radio("Page", ["Overview", "EDA", "Analysis", "Insights"])

selected_months = st.sidebar.multiselect("Month", df['month'].unique(),default=df['month'].unique())
selected_jobs = st.sidebar.multiselect("Job",df['job'].unique(),default=df['job'].unique())
age_range=st.sidebar.slider("Age Range",min_value=int(df['age'].min()),max_value=int(df['age'].max()),value=(int(df['age'].min()), int(df['age'].max())))

# Apply filters
filtered = df[(df['month'].isin(selected_months))&(df['job'].isin(selected_jobs))&(df['age'].between(age_range[0], age_range[1]))]

if page == "Overview":
    st.title("Overview — Bank Marketing Campaign Analysis")
    
    st.markdown("""
    ### 📌 About This Data
    This dataset contains records from a **Portuguese bank's direct marketing campaign** targeting term deposit subscriptions. 
    The bank reached out to customers via phone calls to convince them to open term deposit accounts.
    
    ### 🎯 The Business Problem
    **How can the bank improve its marketing campaign effectiveness?**
    
    The bank faces a critical challenge:
    - **Low subscription rate** — Most customers contacted do NOT subscribe to term deposits
    - **Resource inefficiency** — Marketing campaigns consume time and money with minimal conversion
    - **Lack of targeting** — Without insights, the bank contacts everyone equally, wasting effort on unlikely customers
    
    ### 💡 Our Solution
    By analyzing **customer demographics, call patterns, and economic indicators**, we identify:
    - **Who are the best customers to target?** (age, job, marital status)
    - **When should we contact them?** (optimal months for campaigns)
    - **How to engage them?** (call duration, previous interactions)
    - **What external factors matter?** (economic indicators like interest rates)
    
    This dashboard helps the bank **segment customers strategically** and **maximize campaign ROI**.
    
    ---
    
    ### 📈 Key Metrics
    """)

    # KPIs
    total_calls = len(filtered)
    subscription_rate = round((filtered['y'] == 'yes').mean() * 100, 2)
    
    m1, m2 = st.columns(2)
    m1.metric("📞 Total Calls (Contacts)", f"{total_calls:,}")
    m2.metric("✅ Subscription Rate", f"{subscription_rate}%")
    
    st.markdown("---")
    
    st.subheader("📋 Data Preview")
    st.dataframe(filtered.head(100), use_container_width=True)


elif page == "EDA":
    st.title("📉 Exploratory Data Analysis (EDA)")
    
    st.markdown("""
    ### 🔍 Understanding the Data Distribution
    
    EDA helps us explore the underlying patterns in customer demographics and campaign characteristics.
    By visualizing distributions, we identify:
    - **Key customer segments** (age groups, job types)
    - **Campaign reach patterns** (contact timing, frequency)
    - **Risk factors** (default rates, loan status)
    
        This foundation enables better ta    rgeting strategies.
    """) 
    st.subheader("📊 Statistical Summary")

    summary_table = df.describe()  
    st.dataframe(summary_table)


    st.markdown("---")

    st.subheader("Age Distribution of Clients")
    fig=px.histogram(filtered, x='age', nbins=30)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("💡**Insight:** Most clients are middle-aged (30–50); extreme ages are rare.")

    st.subheader("Job Distribution")
    job_counts = filtered['job'].value_counts().reset_index()
    fig2 = px.bar(job_counts, x='job', y='count')
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("💡**Insight:** Majority are employees, administrative and technical staff; some jobs underrepresented.")

    st.subheader("Subscription Outcome Distribution")
    sub_counts = df['y'].value_counts().reset_index()
    fig3 = px.pie(sub_counts, names='y', values='count',
             title="Subscription Distribution")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("💡**Insight:** Subscription rate is very low compared to non-subscription.")

    st.subheader("Call Duration Distribution")
    fig4 = px.histogram(filtered, x='duration',
                       nbins=40)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("💡**Insight:** Most calls are short; a few are long.")

    st.subheader("Number of Campaign Contacts per Client")
    fig5= px.histogram(filtered, x='campaign',
                       nbins=30)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("💡**Insight:** Most clients were contacted 1–3 times; few contacted many times.")

    st.subheader("Contact Timing — Contacts by Month")
    month_counts = filtered['month'].value_counts().reset_index()
    fig6 = px.bar(month_counts, x='month', y='count')
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("💡**Insight:** Peak activity in summer months (May–Aug).")

    st.subheader("Housing Loan Status")
    housing_counts = filtered['housing'].value_counts().reset_index()
    fig7= px.pie(housing_counts,
                 names='housing',
                 values='count')
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown("💡**Insight:** A substantial portion of clients have housing loans.")

    st.subheader("Credit Default Status")
    default = filtered['default'].value_counts().reset_index()
    fig8= px.pie(default,
                 names='default',
                 values='count')
    st.plotly_chart(fig8, use_container_width=True)
    st.markdown("💡**Insight:** Most clients have no credit defaults.")


elif page == "Analysis":
    st.title("Analysis")
    
    st.markdown("""
    ### 🎯 Research Questions
    
    Here we test **critical hypotheses** to understand what drives customer subscriptions:
    - **Demographic factors** — Does age/job/marital status matter?
    - **Behavioral factors** — Do previous interactions predict future success?
    - **Call quality** — Does spending more time on the call improve conversion?
    - **Timing & frequency** — When and how often should we contact?
    - **Economic context** — Do economic conditions affect decisions?
    
    Each chart reveals patterns that shape our recommendations.
    """)
    
    st.markdown("---")
    # Q1: Age vs Subscription
    st.subheader("Does client age influence the likelihood of subscribing to the term deposit?")
    age_sub = filtered.groupby('age')['y'].value_counts().reset_index(name='count')
    fig = px.bar(age_sub, x="age", y="count",
                 color="y",
                 barmode="group",
                 title="Age vs Subscription")
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Insight:** Age distribution shows varied subscription patterns. Younger and mid-age clients show different subscription behaviors.")

    st.markdown("---")

    # Q2: Job vs Subscription
    st.subheader("Does a client's job type affect their subscription decision?")
    job_sub = filtered.groupby('job')['y'].value_counts().sort_values(ascending=False).reset_index(name='count')
    fig = px.bar(job_sub, x="job", y="count",
                 color="y",
                 barmode="group",
                 title="Job vs Subscription")
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Insight:** Certain job categories have significantly higher subscription rates.")

    st.markdown("---")

    # Q3: Marital Status vs Subscription
    st.subheader("Do marital status and education level impact the probability of subscription?")
    marital_sub = filtered.groupby('marital')['y'].value_counts().sort_values(ascending=False).reset_index(name='count')
    fig = px.bar(marital_sub, x="marital", y="count",
                 color="y",
                 barmode="group",
                 title="Marital Status vs Subscription")
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Insight:** Marital status shows correlation with subscription decisions.")

    st.markdown("---")

    # Q4: Previous Contact vs Subscription
    st.subheader("Are clients who were contacted previously more likely to subscribe?")
    contact_prev = filtered.groupby('contacted_before')['y'].value_counts().reset_index(name='count')
    fig = px.bar(contact_prev, x="contacted_before", y="count",
                 color="y",
                 barmode="group",
                 title="Contacted Before vs Subscription")
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Insight:** Previously contacted clients are more likely to subscribe. Business: Prioritize follow-ups for past contacts.")

    st.markdown("---")

    # Q5: Previous Campaign Outcome vs Subscription
    st.subheader("Does the outcome of previous marketing campaigns affect current subscription success?")
    poutcome_sub = filtered.groupby('poutcome')['y'].value_counts().sort_values(ascending=False).reset_index(name='count')
    fig = px.bar(poutcome_sub, x="poutcome", y="count",
                 color="y",
                 barmode="group",
                 title="Previous Campaign Outcome vs Subscription")
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Insight:** Previous campaign outcomes strongly influence current success.")

    st.markdown("---")

    # Q6: Duration Category vs Subscription
    st.subheader("Does call duration category influence the probability of subscription?")
    dur_sub = filtered.groupby('duration_cat')['y'].value_counts().sort_values(ascending=False).reset_index(name='count')
    fig = px.bar(dur_sub, x="duration_cat", y="count",
                 color="y",
                 barmode="group",
                 title="Duration Category vs Subscription")
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Insight:** Longer calls are strongly associated with subscriptions.")

    st.markdown("---")

    # Q7: Campaign Contacts vs Subscription
    st.subheader("Does the number of contacts during the campaign increase subscription success?")
    camp_sub = filtered.groupby('campaign_cat')['y'].value_counts().sort_values(ascending=False).reset_index(name='count')
    fig = px.bar(camp_sub, x="campaign_cat", y="count",
                 color="y",
                 barmode="group",
                 title="Campaign Contacts vs Subscription")
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Insight:** Fewer contacts (1–3) perform better than many contacts.")

    st.markdown("---")

    # Q8: Loans vs Subscription
    st.subheader("Do clients with housing or personal loans subscribe less frequently?")
    housing_sub = filtered.groupby('housing')['y'].value_counts().sort_values(ascending=False).reset_index(name='count')
    fig = px.bar(housing_sub, x="housing", y="count",
                 color="y",
                 barmode="group",
                 title="Housing Loan vs Subscription")
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Insight:** Clients without housing loans show higher subscription rates.")

    loan = df.groupby('loan')['y'].value_counts().sort_values(ascending=False).reset_index(name='count')
    fig = px.bar(loan, x="loan", y="count",
             color="y",
             barmode="group",
             title="Loan Status vs Subscription")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Q9: Month vs Subscription
    st.subheader("Does the month of contact influence subscription success?")
    month_sub = filtered.groupby('month')['y'].value_counts().sort_values(ascending=False).reset_index(name='count')
    fig = px.bar(month_sub, x="month", y="count",
                 color="y",
                 barmode="group",
                 title="Month vs Subscription")
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Insight:** Certain months show higher conversion rates. Seasonal trends matter.")

    st.markdown("---")

    # Q10: Economic Indicators vs Subscription
    st.subheader("Do economic indicators impact clients' subscription decisions?")
    fig = px.box(filtered, x="y", y="euribor3m",
                 title="Euribor Rate vs Subscription")
    st.plotly_chart(fig, use_container_width=True)
    st.info("💡 **Insight:** Euribor rates correlate with subscription behavior. Economic conditions matter.")


else:  # Insights
    st.title("Insights & Recommendations")
    
    st.markdown("""
    ### 🎯 Actionable Strategies Based on Analysis
    
    This section summarizes **subscription rates by key dimensions** to guide strategic decisions:
    
    - **Which jobs are goldmines?** (Highest conversion by profession)
    - **When should we campaign?** (Best-performing months)
    - **How to improve engagement?** (Call duration impact)
    """)
    
    st.markdown("---")
    
    st.subheader("🏆 Top Subscription Rates by Job Type")
    st.markdown("**Which professions are most likely to subscribe?**")
    grp_job = filtered.groupby('job')['y'].apply(lambda x: (x=='yes').mean()).reset_index(name='subscription_rate')
    grp_job['subscription_rate'] = (grp_job['subscription_rate'] * 100).round(2)
    st.dataframe(grp_job.sort_values('subscription_rate', ascending=False), use_container_width=True)

    st.markdown("---")
    
    st.subheader("📅 Best Months for Campaign Launches")
    st.markdown("**When do customers show highest subscription intent?**")
    grp_month = filtered.groupby('month')['y'].apply(lambda x: (x=='yes').mean()).reset_index(name='subscription_rate')
    grp_month['subscription_rate'] = (grp_month['subscription_rate'] * 100).round(2)
    st.dataframe(grp_month.sort_values('subscription_rate', ascending=False), use_container_width=True)

    st.subheader("⏱️ Impact of Call Duration on Conversion")
    st.markdown("**How does conversation length affect outcomes?**")
    grp_dur = filtered.groupby('duration_cat')['y'].apply(lambda x: (x=='yes').mean()).reset_index(name='subscription_rate')
    grp_dur['subscription_rate'] = (grp_dur['subscription_rate'] * 100).round(2)
    st.dataframe(grp_dur.sort_values('subscription_rate', ascending=False), use_container_width=True)

    st.markdown("---")
    
    st.subheader("Strategic Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        ✅ **Prioritize High-Conversion Jobs**
        
        Target professions with subscription rates >30%. Customize messaging for each sector.
        """)
        
        st.success("""
        ✅ **Focus on Peak Seasons**
        
        Concentrate budget on best-performing months to maximize ROI.
        """)
        
        st.success("""
        ✅ **Extend Quality Conversations**
        
        Longer calls = higher conversion. Train agents for deeper engagement.
        """)
    
    with col2:
        st.success("""
        ✅ **Re-engage Past Success**
        
        Customers who subscribed before are gold. Prioritize re-engagement.
        """)
        
        st.success("""
        ✅ **Monitor Economic Conditions**
        
        Time campaigns when interest rates favor term deposit investments.
        """)
        
        st.success("""
        ✅ **Smart Segment Targeting**
        
        Use filters to create micro-segments by age, job, and loan status.
        """)
