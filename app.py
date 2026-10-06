import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Paid Search Campaign Simulator", page_icon="📊", layout="wide")

# --- MAIN TITLE ---
st.title("Paid Search Campaign Simulator")
st.caption("Class 5 Hands-On Exercise: Keyword Research, Match Types, Ad Building & GA4 Analytics")

# --- SIDEBAR: CAMPAIGN CONFIGURATION ---
st.sidebar.header("⚙️ Campaign Settings")

campaign_objective = st.sidebar.selectbox(
    "Campaign Marketing Objective:",
    ["Sales", "Leads", "Website Traffic", "Brand Awareness"]
)

conversion_goal = st.sidebar.selectbox(
    "Conversion Goals:",
    ["Purchases", "Lead Form Submissions", "Phone Calls", "Page Views"]
)

target_locations = st.sidebar.text_input(
    "Target Locations (U.S. States or Zip Codes):",
    value="NY, NJ, CT, 10001, 10003"
)

st.sidebar.subheader("💰 Bidding & Budget")
bidding_strategy = st.sidebar.selectbox(
    "Smart Bidding Strategy:",
    ["Maximize Clicks", "Maximize Conversions", "Target CPA", "Target ROAS"]
)

target_roas_input = st.sidebar.number_input(
    "Target ROAS Number (e.g., 3.5 for 3.5x / 350%):",
    min_value=0.5,
    max_value=20.0,
    value=3.5,
    step=0.5
)

daily_budget = st.sidebar.slider("Daily Budget ($):", min_value=10, max_value=500, value=50, step=10)
monthly_budget = daily_budget * 30.4

st.sidebar.subheader("🔗 GA4 Tracking & Attribution")
utm_campaign = st.sidebar.text_input("GA4 UTM Campaign Tag:", value="fall2026_paid_search_campaign")
auto_tagging = st.sidebar.checkbox("Enable Google Auto-Tagging (GCLID for GA4)", value=True)

# --- TAB NAVIGATION ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Custom Keyword Planner", 
    "2. Match Types & Negatives", 
    "3. Budget Projections", 
    "4. Ad Builder & Assets", 
    "5. GA4 Analytics Dashboard"
])

# --- MODULE 1: CUSTOM KEYWORD PLANNER ---
with tab1:
    st.header("Module 1: Custom Keyword Research")
    st.write("Type **5 target search terms** your prospective buyers search for. The simulator will estimate Search Volume (MSV), Keyword Difficulty (KD %), and Cost Per Click (CPC).")
    
    col_kws, col_metrics = st.columns([1, 1.5])
    
    with col_kws:
        st.subheader("Type 5 Search Terms")
        kw1 = st.text_input("Keyword 1:", value="buy products online")
        kw2 = st.text_input("Keyword 2:", value="best services near me")
        kw3 = st.text_input("Keyword 3:", value="top rated customer reviews")
        kw4 = st.text_input("Keyword 4:", value="pricing and quotes")
        kw5 = st.text_input("Keyword 5:", value="affordable solutions in nyc")
        
        user_input_kws = [k.strip() for k in [kw1, kw2, kw3, kw4, kw5] if k.strip()]

    # Heuristic Data Generator for Custom Keywords
    def estimate_kw_metrics(kw_list):
        parsed_data = []
        for kw in kw_list:
            kw_lower = kw.lower()
            if any(term in kw_lower for term in ["buy", "cost", "price", "quote", "tickets", "book"]):
                intent = "Decision / Commercial"
                cpc = np.random.uniform(3.20, 5.50)
                kd = np.random.randint(55, 78)
                msv = np.random.randint(1200, 4800)
            elif any(term in kw_lower for term in ["vs", "best", "top", "review", "comparison"]):
                intent = "Consideration / Comparison"
                cpc = np.random.uniform(2.10, 3.80)
                kd = np.random.randint(40, 65)
                msv = np.random.randint(2500, 8900)
            elif any(term in kw_lower for term in ["how", "why", "what", "near me", "where"]):
                intent = "Awareness / Problem"
                cpc = np.random.uniform(1.20, 2.50)
                kd = np.random.randint(25, 48)
                msv = np.random.randint(4500, 15000)
            else:
                intent = "Navigational / Brand"
                cpc = np.random.uniform(0.80, 1.95)
                kd = np.random.randint(15, 35)
                msv = np.random.randint(800, 3100)
                
            parsed_data.append({
                "Target Keyword": kw,
                "Estimated Intent Stage": intent,
                "Monthly Search Vol (MSV)": msv,
                "Keyword Difficulty (KD %)": f"{kd}%",
                "Est. CPC ($)": round(cpc, 2)
            })
        return pd.DataFrame(parsed_data)

    df_custom_kws = estimate_kw_metrics(user_input_kws)
    
    with col_metrics:
        st.subheader("💡 Keyword Planner Research Results")
        st.dataframe(df_custom_kws, use_container_width=True, hide_index=True)
        
        avg_cpc = df_custom_kws["Est. CPC ($)"].mean()
        total_msv = df_custom_kws["Monthly Search Vol (MSV)"].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Search Volume", f"{total_msv:,}")
        m2.metric("Blended Est. CPC", f"${avg_cpc:.2f}")
        m3.metric("Keywords Analyzed", f"{len(user_input_kws)} / 5")

# --- MODULE 2: MATCH TYPES & NEGATIVES ---
with tab2:
    st.header("Module 2: Keyword Match Types & Negative Keyword Filters")
    
    c_match, c_neg = st.columns(2)
    with c_match:
        match_type = st.radio(
            "Select Match Type Rule:",
            ["Broad Match (keyword)", 'Phrase Match ("keyword")', "Exact Match ([keyword])"],
            help="Broad match gets maximum views; Phrase match targets phrase order; Exact match targets precise intent."
        )
    with c_neg:
        negatives = st.text_input("Negative Keywords (comma separated):", value="free, jobs, cheap, pdf, diy, reddit")
        st.caption("Negative keywords prevent wasted ad spend on unqualified clicks.")

    st.subheader("⚡ Real-Time Search Query Simulator")
    test_queries = [
        "free pdf guide download",
        user_input_kws[0] if user_input_kws else "target search term",
        "jobs and career opportunities",
        "reviews and competitor pricing"
    ]
    
    neg_list = [n.strip().lower() for n in negatives.split(",") if n.strip()]
    
    sim_results = []
    for q in test_queries:
        blocked = any(neg in q.lower() for neg in neg_list)
        if blocked:
            status = "❌ BLOCKED by Negative Keyword"
        elif "Broad" in match_type:
            status = "✅ AD TRIGGERED (Broad Match)"
        elif "Phrase" in match_type:
            status = "✅ AD TRIGGERED (Phrase Match)" if any(kw.lower() in q.lower() for kw in user_input_kws) else "⚠️ NOT TRIGGERED"
        else:
            status = "✅ AD TRIGGERED (Exact Match)" if any(kw.lower() == q.lower() for kw in user_input_kws) else "⚠️ NOT TRIGGERED"
            
        sim_results.append({"Prospect Search Query": q, "Ad Trigger Status": status})
        
    st.table(pd.DataFrame(sim_results))

# --- MODULE 3: BUDGET PROJECTIONS ---
with tab3:
    st.header("Module 3: Campaign Projections & Budget Setup")
    
    ctr_benchmark = 0.065 # 6.5% CTR benchmark
    est_clicks = monthly_budget / avg_cpc if avg_cpc > 0 else 0
    est_impressions = est_clicks / ctr_benchmark if ctr_benchmark > 0 else 0
    
    st.write("Calculated using Class 5 Formulas: \\(\\text{CTR} = \\frac{\\text{Clicks}}{\\text{Impressions}}\\) | \\(\\text{Spend} = \\text{Clicks} \\times \\text{CPC}\\)")
    
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Monthly Budget", f"${monthly_budget:,.2f}")
    p2.metric("Projected Impressions", f"{int(est_impressions):,}")
    p3.metric("Projected Clicks (Sessions)", f"{int(est_clicks):,}")
    p4.metric("Benchmark CTR %", f"{ctr_benchmark*100:.1f}%")

# --- MODULE 4: AD BUILDER & AD ASSETS ---
with tab4:
    st.header("Module 4: Responsive Search Ad & Ad Assets Builder")
    st.write("Build your ad copy and include **Ad Assets** to increase Quality Score and CTR.")
    
    col_copy, col_assets, col_preview = st.columns([1.2, 1.2, 1.5])
    
    with col_copy:
        st.subheader("1. Main Ad Copy")
        h1 = st.text_input("Headline 1 (Max 30 chars):", value="Official Brand Website")
        h2 = st.text_input("Headline 2 (Max 30 chars):", value="Top Rated Services in NYC")
        h3 = st.text_input("Headline 3 (Max 30 chars):", value="Book & Reserve Online Today")
        
        d1 = st.text_area("Description 1 (Max 90 chars):", value="Discover why customers choose our services. Authentic, reliable, and top-rated experience.")
        d2 = st.text_area("Description 2 (Max 90 chars):", value="Explore pricing, upcoming availability, and customer reviews. Visit our site now!")
        display_url = st.text_input("Display URL:", value="www.yourcompany.com/nyc")

    with col_assets:
        st.subheader("2. Ad Assets & Image Upload")
        uploaded_image = st.file_uploader("Upload Ad Image Asset (PNG / JPG):", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Ad Image Asset Preview", width=180)
            
        inc_sitelinks = st.checkbox("Include Sitelink Assets", value=True)
        sitelink_text = st.text_input("Sitelink Text:", value="View Pricing & Packages") if inc_sitelinks else ""
        
        inc_callout = st.checkbox("Include Callout Assets", value=True)
        callout_text = st.text_input("Callout Highlights:", value="24/7 Support • No Hidden Fees") if inc_callout else ""
        
        inc_call = st.checkbox("Include Phone Call Asset", value=True)
        phone_num = st.text_input("Phone Number:", value="(212) 555-0199") if inc_call else ""

    with col_preview:
        st.subheader("3. Live Search Preview")
        
        phone_html = f"📞 Call {phone_num}" if inc_call else ""
        sitelink_html = f"<u>{sitelink_text}</u> • <u>Contact Us</u> • <u>FAQs</u>" if inc_sitelinks else ""
        
        st.markdown(
            f"""
            <div style="border: 1px solid #dadce0; border-radius: 8px; padding: 16px; background-color: #ffffff; font-family: Arial, sans-serif;">
                <div style="font-size: 12px; color: #202124;">
                    <span style="font-weight: bold;">Sponsored</span> • <span>{display_url}</span>
                </div>
                <h3 style="color: #1a0dab; margin: 4px 0px; font-size: 18px; line-height: 1.3;">{h1} | {h2} | {h3}</h3>
                <div style="color: #4d5156; font-size: 13px; margin-bottom: 6px;">{d1} {d2}</div>
                {"<div style='color: #006621; font-size: 12px; margin-bottom: 4px;'>" + callout_text + "</div>" if inc_callout else ""}
                {"<div style='color: #1a0dab; font-size: 12px; margin-bottom: 4px;'>" + sitelink_html + "</div>" if inc_sitelinks else ""}
                {"<div style='color: #5f6368; font-size: 12px;'>" + phone_html + "</div>" if inc_call else ""}
            </div>
            """,
            unsafe_allow_html=True
        )

# --- MODULE 5: GA4 ANALYTICS DASHBOARD ---
with tab5:
    st.header("Module 5: Simulated GA4 Performance & Channel Attribution")
    
    if st.button("Launch Campaign Simulation"):
        conv_rate = 0.032 # 3.2% conversion rate
        conversions = int(est_clicks * conv_rate)
        cpa = monthly_budget / conversions if conversions > 0 else 0
        
        # Calculate Simulated Actual ROAS based on $85 order value
        total_revenue = conversions * 85.00
        actual_roas = total_revenue / monthly_budget if monthly_budget > 0 else 0
        
        st.subheader("📈 GA4 Overview Metrics (Paid Search)")
        g1, m2, g3, g4, g5 = st.columns(5)
        g1.metric("GA4 Sessions (Clicks)", f"{int(est_clicks):,}")
        m2.metric("Total Monthly Spend", f"${monthly_budget:,.2f}")
        g3.metric("Conversions", f"{conversions}")
        g4.metric("Cost Per Acquisition (CPA)", f"${cpa:.2f}")
        g5.metric("Simulated ROAS", f"{actual_roas:.2f}x", delta=f"{actual_roas - target_roas_input:.2f}x vs Target")
        
        # --- ROAS ANALYSIS & DIAGNOSTIC FEEDBACK ---
        st.subheader("📊 ROAS Performance Analysis")
        
        if actual_roas < target_roas_input or actual_roas < 2.0:
            st.error(
                f"🚨 **ROAS WARNING: Generated ROAS ({actual_roas:.2f}x) is BELOW your Target ROAS ({target_roas_input:.2f}x)!**\n\n"
                f"Your campaign is currently returning **${actual_roas:.2f}** for every **$1.00 spent**, which is underperforming your desired profitability benchmark."
            )
            st.markdown(
                """
                ### 🛠️ How to Improve Your ROAS Number:
                1. **Tighten Keyword Match Types & Add Negatives:** Switch broad match terms to **Phrase Match** or **Exact Match**, and expand your negative keyword list to eliminate non-converting clicks that waste ad budget.
                2. **Optimize Landing Page Conversion Rate & Ad Quality:** Improve landing page load speed and offer clarity to raise your conversion rate from 3.2% to 4.5%+, or rewrite ad copy with stronger Call-to-Actions (CTAs) to boost Quality Score and lower your average CPC.
                """
            )
        else:
            st.success(
                f"🎉 **EXCELLENT PERFORMANCE: Generated ROAS ({actual_roas:.2f}x) MEETS or EXCEEDS your Target ROAS ({target_roas_input:.2f}x)!**\n\n"
                f"Your campaign is generating **${actual_roas:.2f} in revenue for every $1.00 spent**, creating a highly profitable return on investment."
            )
            st.markdown(
                """
                ### 🚀 Next Steps to Scale Performance:
                1. **Increase Daily Budget:** Reinvest profits into high-converting exact match keywords.
                2. **Expand Ad Assets:** Add additional sitelinks and visual callouts to capture more SERP real estate.
                """
            )

        # Simulated Daily Trend Line
        st.subheader("📈 30-Day GA4 Traffic Trend")
        days = np.arange(1, 31)
        daily_sessions = np.random.normal(est_clicks / 30, 4, 30).astype(int)
        chart_df = pd.DataFrame({"Day": days, "GA4 Paid Search Traffic": daily_sessions})
        st.line_chart(chart_df.set_index("Day"))
        
        # GA4 Channel Comparison Table
        st.subheader("📊 GA4 Default Channel Grouping Comparison Table")
        channel_df = pd.DataFrame({
            "Default Channel Grouping": ["Paid Search (Google Ads)", "Organic Search (Google)", "Direct", "Organic Social (TikTok/IG)"],
            "Sessions": [int(est_clicks), int(est_clicks * 1.5), int(est_clicks * 0.7), int(est_clicks * 1.2)],
            "Engagement Rate %": ["68.5%", "73.2%", "52.0%", "59.4%"],
            "Conversions": [conversions, int(conversions * 1.4), int(conversions * 0.6), int(conversions * 0.8)],
            "Conversion Rate %": ["3.2%", "3.6%", "2.5%", "2.1%"]
        })
        st.table(channel_df)
