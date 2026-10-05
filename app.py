import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="GA4 & Google Ads Campaign Simulator", page_icon="📊", layout="wide")

st.title("📊 Paid Search & GA4 Campaign Simulator")
st.caption("Class 5 Hands-On Exercise: Keyword Research, Match Types, Ad Building & GA4 Analytics")

# --- SIDEBAR: CLIENT & CAMPAIGN SETUP ---
st.sidebar.header("⚙️ Campaign Configuration")
brand = st.sidebar.selectbox(
    "Select Your Group Project Brand:",
    [
        "Book Club Bar (Literary Nightlife)",
        "Thanks! Social Club (Pet Supplies)",
        "NYC Great Movers (Student Moving)",
        "Cloudy (Natural Sleep Solutions)",
        "Ando Patisserie (Asian Bakery)",
        "Trainwell (Online Personal Training)",
        "Brasil Run Club (Social Running)",
        "Parkii (Organic Skincare)"
    ]
)

st.sidebar.subheader("📍 Location & Bidding")
location = st.sidebar.multiselect(
    "Target Locations:",
    ["NYC Metro (5 Boroughs)", "Tri-State Area (NY/NJ/CT)", "Nationwide (US)", "Target Zip Codes"],
    default=["NYC Metro (5 Boroughs)"]
)

bidding_strategy = st.sidebar.selectbox(
    "Smart Bidding Strategy:",
    ["Maximize Clicks", "Maximize Conversions", "Target CPA (Cost Per Acquisition)", "Target ROAS (Return on Ad Spend)"]
)

daily_budget = st.sidebar.slider("Daily Campaign Budget ($):", min_value=10, max_value=500, value=50, step=10)
monthly_budget = daily_budget * 30.4

# --- TAB NAVIGATION ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Keyword Planner", 
    "2. Match Types & Negatives", 
    "3. Campaign & Budget", 
    "4. Ad Builder (RSA / PMax)", 
    "5. GA4 Analytics Dashboard"
])

# --- MODULE 1: KEYWORD PLANNER ---
with tab1:
    st.header("Module 1: Keyword Research & Selection")
    st.write("Select target search terms based on Monthly Search Volume (MSV), Keyword Difficulty (KD %), and Cost Per Click (CPC).")
    
    # Pre-populated Keyword Database
    kw_data = {
        "Book Club Bar": [
            {"Keyword": "bookstore bar nyc", "Intent": "Commercial", "MSV": 4400, "KD %": 42, "Est. CPC ($)": 2.10},
            {"Keyword": "where to meet readers nyc", "Intent": "Problem/Discovery", "MSV": 1800, "KD %": 28, "Est. CPC ($)": 1.45},
            {"Keyword": "solo friendly bars East Village", "Intent": "Location", "MSV": 2900, "KD %": 35, "Est. CPC ($)": 1.85},
            {"Keyword": "book club bar tickets", "Intent": "Brand/High-Intent", "MSV": 1200, "KD %": 18, "Est. CPC ($)": 0.95},
        ],
        "Thanks! Social Club": [
            {"Keyword": "dog separation anxiety solutions", "Intent": "Problem", "MSV": 12100, "KD %": 58, "Est. CPC ($)": 3.40},
            {"Keyword": "calming spray for dogs review", "Intent": "Comparison", "MSV": 3600, "KD %": 41, "Est. CPC ($)": 2.25},
            {"Keyword": "natural dog anxiety relief", "Intent": "Commercial", "MSV": 8800, "KD %": 49, "Est. CPC ($)": 2.90},
            {"Keyword": "how to stop dog barking when leaving", "Intent": "Info/Problem", "MSV": 14500, "KD %": 52, "Est. CPC ($)": 1.80},
        ],
        "NYC Great Movers": [
            {"Keyword": "best student movers nyc", "Intent": "Commercial", "MSV": 6600, "KD %": 62, "Est. CPC ($)": 4.80},
            {"Keyword": "cheap walk up moving company Manhattan", "Intent": "Problem/Location", "MSV": 3200, "KD %": 47, "Est. CPC ($)": 3.90},
            {"Keyword": "small apartment moving quotes nyc", "Intent": "High-Intent", "MSV": 4100, "KD %": 51, "Est. CPC ($)": 4.15},
            {"Keyword": "dorm moving service NYU Columbia", "Intent": "Niche/Brand", "MSV": 1900, "KD %": 31, "Est. CPC ($)": 2.60},
        ]
    }
    
    brand_key = brand.split(" (")[0]
    data = kw_data.get(brand_key, kw_data["Book Club Bar"])
    df_kw = pd.DataFrame(data)
    
    edited_df = st.data_editor(
        df_kw,
        column_config={"Select": st.column_config.CheckboxColumn("Target?", default=True)},
        disabled=["Keyword", "Intent", "MSV", "KD %", "Est. CPC ($)"],
        hide_index=True,
    )
    
    st.subheader("💡 Selected Keyword Metrics Summary")
    selected_kws = edited_df
    avg_cpc = selected_kws["Est. CPC ($)"].mean()
    total_msv = selected_kws["MSV"].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Monthly Search Volume", f"{total_msv:,}")
    col2.metric("Average Keyword Difficulty", f"{selected_kws['KD %'].mean():.1f}%")
    col3.metric("Blended Est. CPC", f"${avg_cpc:.2f}")

# --- MODULE 2: MATCH TYPES & NEGATIVE KEYWORDS ---
with tab2:
    st.header("Module 2: Match Types & Negative Keyword Sandbox")
    st.write("Assign match types to control ad triggers, and add negative keywords to block irrelevant clicks.")
    
    col1, col2 = st.columns(2)
    with col1:
        match_type = st.radio(
            "Select Keyword Match Type:",
            ["Broad Match (keyword)", 'Phrase Match ("keyword")', "Exact Match ([keyword])"],
            help="Broad match captures variations; Phrase match captures phrase order; Exact match requires exact meaning."
        )
    
    with col2:
        negatives = st.text_input("Enter Negative Keywords (comma separated):", value="free, jobs, pdf, cheap, reddit, diy")
        st.caption("Negative keywords stop your ad from displaying when users search for these terms.")

    st.subheader("⚡ Live Search Query Trigger Test")
    st.write("Testing sample customer search queries against your selected match types & negative filters:")
    
    test_queries = [
        f"free {brand_key.lower()} pdf download",
        f"buy {brand_key.lower()} tickets online",
        f"best {brand_key.lower()} alternatives 2026",
        f"jobs at {brand_key.lower()} nyc"
    ]
    
    neg_list = [n.strip().lower() for n in negatives.split(",")]
    
    results = []
    for q in test_queries:
        blocked = any(neg in q.lower() for neg in neg_list if neg)
        if blocked:
            status = "❌ BLOCKED by Negative Keyword"
        elif "Broad" in match_type:
            status = "✅ AD TRIGGERED (Broad Match)"
        elif "Phrase" in match_type and brand_key.lower() in q.lower():
            status = "✅ AD TRIGGERED (Phrase Match)"
        elif "Exact" in match_type and q.strip().lower() == brand_key.lower():
            status = "✅ AD TRIGGERED (Exact Match)"
        else:
            status = "⚠️ NOT TRIGGERED (Query mismatch)"
        results.append({"User Search Query": q, "Ad Status": status})
    
    st.table(pd.DataFrame(results))

# --- MODULE 3: CAMPAIGN & BUDGET CONTROLS ---
with tab3:
    st.header("Module 3: Campaign Projections & Budget Setup")
    st.write("Model your monthly projections based on Class 5 formulas.")
    
    est_ctr = 0.065 # 6.5% standard benchmarks
    est_clicks = monthly_budget / avg_cpc
    est_impressions = est_clicks / est_ctr
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Monthly Budget", f"${monthly_budget:,.2f}")
    c2.metric("Projected Impressions", f"{int(est_impressions):,}")
    c3.metric("Projected Clicks", f"{int(est_clicks):,}")
    c4.metric("Est. CTR %", f"{est_ctr*100:.1f}%")

# --- MODULE 4: AD BUILDER (RSA & PMAX) ---
with tab4:
    st.header("Module 4: Responsive Search Ad & Performance Max Builder")
    
    ad_type = st.radio("Select Ad Format:", ["Responsive Search Ad (RSA)", "Performance Max / AI Max Asset Group"])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Write Ad Copy")
        h1 = st.text_input("Headline 1 (Max 30 chars):", value=f"Official {brand_key}")
        h2 = st.text_input("Headline 2 (Max 30 chars):", value="Book Your Experience Today")
        h3 = st.text_input("Headline 3 (Max 30 chars):", value="Top Rated in NYC")
        
        d1 = st.text_area("Description 1 (Max 90 chars):", value="Discover the premier social literary experience in NYC. Reserve your spot online now!")
        d2 = st.text_area("Description 2 (Max 90 chars):", value="Join hundreds of readers. Laptop-free intentional social space in East Village.")
        
        final_url = st.text_input("Final Landing Page URL:", value=f"https://www.{brand_key.lower().replace(' ', '')}.com/reserve")

    with col2:
        st.subheader("📱 Live Search Preview")
        st.markdown(
            f"""
            <div style="border: 1px solid #dadce0; border-radius: 8px; padding: 16px; background-color: #ffffff;">
                <span style="font-weight: bold; color: #202124; font-size: 12px;">Sponsored</span> • <span>{final_url}</span>
                <h3 style="color: #1a0dab; margin-top: 4px; font-size: 18px;">{h1} | {h2} | {h3}</h3>
                <p style="color: #4d5156; font-size: 14px;">{d1} {d2}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Policy & Strength Validation
        st.subheader("🛡️ Policy Guardrails & Ad Strength")
        warnings = []
        if "!" in h1 or "!" in h2:
            warnings.append("⚠️ Avoid exclamation marks in headlines (Google Policy).")
        if h1.isupper() or h2.isupper():
            warnings.append("⚠️ Avoid ALL CAPS in headlines.")
        if len(h1) > 30 or len(h2) > 30 or len(h3) > 30:
            warnings.append("❌ Headline exceeds 30 character limit.")
            
        if warnings:
            for w in warnings:
                st.warning(w)
        else:
            st.success("✅ Ad Quality Score: EXCELLENT (All Policy Guardrails Passed)")

# --- MODULE 5: GA4 ANALYTICS DASHBOARD ---
with tab5:
    st.header("Module 5: Simulated GA4 Performance & Attribution Dashboard")
    st.write("Simulate 30 days of post-click user traffic and conversion data in Google Analytics 4.")
    
    if st.button("🚀 Launch Campaign & Run GA4 Simulation"):
        conv_rate = 0.032 # 3.2% conversion rate
        conversions = int(est_clicks * conv_rate)
        cpa = monthly_budget / conversions if conversions > 0 else 0
        roas = (conversions * 85.00) / monthly_budget # Assuming $85 average order value
        
        st.subheader("📈 GA4 Overview Metrics (Paid Search Channel)")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Sessions (Clicks)", f"{int(est_clicks):,}")
        m2.metric("Total Spend", f"${monthly_budget:,.2f}")
        m3.metric("Conversions", f"{conversions}")
        m4.metric("Cost Per Acquisition (CPA)", f"${cpa:.2f}")
        m5.metric("Target ROAS", f"{roas:.2f}x")
        
        # Simulated Daily Traffic Chart
        days = np.arange(1, 31)
        daily_clicks = np.random.normal(est_clicks / 30, 5, 30).astype(int)
        chart_data = pd.DataFrame({"Day": days, "GA4 Paid Search Sessions": daily_clicks})
        
        st.line_chart(chart_data.set_index("Day"))
        
        st.subheader("📊 GA4 Default Channel Grouping Comparison")
        channel_data = pd.DataFrame({
            "Default Channel Grouping": ["Paid Search (Google Ads)", "Organic Search (Google)", "Direct", "Organic Social (TikTok/IG)"],
            "Sessions": [int(est_clicks), int(est_clicks * 1.4), int(est_clicks * 0.8), int(est_clicks * 1.1)],
            "Engagement Rate %": ["68.4%", "72.1%", "54.2%", "61.0%"],
            "Conversions": [conversions, int(conversions * 1.6), int(conversions * 0.7), int(conversions * 0.9)],
            "Conversion Rate %": ["3.2%", "3.6%", "2.8%", "2.6%"]
        })
        st.table(channel_data)
