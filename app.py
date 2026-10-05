import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="GA4 & Google Ads Campaign Simulator", page_icon="📊", layout="wide")

st.title("📊 Paid Search & GA4 Campaign Simulator")
st.caption("NYU INTG1-GC 2105 | Class 5: Hands-On Google Ads & GA4 Campaign Builder")

# --- SIDEBAR: CAMPAIGN CONFIGURATION ---
st.sidebar.header("⚙️ 1. Campaign Settings")

brand = st.sidebar.selectbox(
    "Select Group Project Company:",
    [
        "Book Club Bar",
        "Thanks! Social Club",
        "NYC Great Movers",
        "Cloudy",
        "Ando Patisserie",
        "Trainwell",
        "Brasil Run Club",
        "Parkii"
    ]
)

campaign_objective = st.sidebar.selectbox(
    "Campaign Marketing Objective:",
    ["Lead Generation (Form Fill / Booking)", "Website Traffic & Awareness", "E-Commerce Sales / RSVPs"]
)

st.sidebar.subheader("🌐 Networks & Location")
networks = st.sidebar.multiselect(
    "Select Ad Networks:",
    ["Google Search Network", "Google Search Partners", "Google Display Network (Opt-Out Recommended)"],
    default=["Google Search Network"]
)

location = st.sidebar.multiselect(
    "Target Locations:",
    ["NYC Metro (5 Boroughs)", "Tri-State Area (NY/NJ/CT)", "Nationwide (US)", "Specific Zip Codes"],
    default=["NYC Metro (5 Boroughs)"]
)

st.sidebar.subheader("💰 Bidding & Budget")
bidding_strategy = st.sidebar.selectbox(
    "Smart Bidding Strategy:",
    ["Maximize Clicks", "Maximize Conversions", "Target CPA", "Target ROAS"]
)

daily_budget = st.sidebar.slider("Daily Budget (\$):", min_value=10, max_value=500, value=50, step=10)
monthly_budget = daily_budget * 30.4

st.sidebar.subheader("🔗 GA4 Tracking & Attribution")
utm_campaign = st.sidebar.text_input("GA4 UTM Campaign Tag:", value=f"fall2026_{brand.lower().replace(' ', '_')}_search")
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
    st.header("Module 1: Keyword Research & Custom Keyword Planner")
    st.write("Enter **5 custom keywords** your prospective buyers would search for. The planner will estimate Search Volume (MSV), Keyword Difficulty (KD %), and Cost Per Click (CPC).")
    
    col_kws, col_metrics = st.columns([1, 1.5])
    
    with col_kws:
        st.subheader("Type 5 Target Search Terms")
        kw1 = st.text_input("Keyword 1:", value=f"best {brand.lower()} nyc" if "Bar" in brand or "Patisserie" in brand else f"buy {brand.lower()} online")
        kw2 = st.text_input("Keyword 2:", value=f"how to solve {brand.lower()} problems" if "Thanks" in brand or "Cloudy" in brand else f"cheap {brand.lower()} quotes")
        kw3 = st.text_input("Keyword 3:", value=f"top rated {brand.lower()} reviews")
        kw4 = st.text_input("Keyword 4:", value=f"where to find {brand.lower()} near me")
        kw5 = st.text_input("Keyword 5:", value=f"{brand.lower()} vs competitors")
        
        user_input_kws = [k.strip() for k in [kw1, kw2, kw3, kw4, kw5] if k.strip()]

    # Heuristic Data Generator for Custom Keywords
    def estimate_kw_metrics(kw_list):
        parsed_data = []
        for kw in kw_list:
            kw_lower = kw.lower()
            # Determine Intent
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
                "Est. CPC (\$)": round(cpc, 2)
            })
        return pd.DataFrame(parsed_data)

    df_custom_kws = estimate_kw_metrics(user_input_kws)
    
    with col_metrics:
        st.subheader("💡 Keyword Planner Research Results")
        st.dataframe(df_custom_kws, use_container_width=True, hide_index=True)
        
        avg_cpc = df_custom_kws["Est. CPC (\$)"].mean()
        total_msv = df_custom_kws["Monthly Search Vol (MSV)"].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Targeted Search Vol", f"{total_msv:,}")
        m2.metric("Blended Est. CPC", f"\${avg_cpc:.2f}")
        m3.metric("Keywords Analyzed", f"{len(user_input_kws)} / 5")

# --- MODULE 2: MATCH TYPES & NEGATIVES ---
with tab2:
    st.header("Module 2: Keyword Match Types & Negative Keyword Filters")
    
    c_match, c_neg = st.columns(2)
    with c_match:
        match_type = st.radio(
            "Select Match Type Rule:",
            ["Broad Match (keyword)", 'Phrase Match ("keyword")', "Exact Match ([keyword])"],
            help="Broad match gets maximum views; Phrase match targets order; Exact match targets precise intent."
        )
    with c_neg:
        negatives = st.text_input("Negative Keywords (comma separated):", value="free, jobs, cheap, pdf, diy, reddit, wholesale")
        st.caption("Negative keywords prevent wasted ad spend on unqualified clicks.")

    st.subheader("⚡ Real-Time Search Query Simulator")
    test_queries = [
        f"free {brand.lower()} pdf guide",
        f"{user_input_kws if user_input_kws else brand.lower()}",
        f"jobs at {brand.lower()} nyc",
        f"reviews for {brand.lower()} pricing"
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
    st.header("Module 3: Campaign Projections & Formulas")
    
    ctr_benchmark = 0.065 # 6.5% CTR
    est_clicks = monthly_budget / avg_cpc if avg_cpc > 0 else 0
    est_impressions = est_clicks / ctr_benchmark if ctr_benchmark > 0 else 0
    
    st.write("Calculated using Class 5 Formulas: \\(\\text{CTR} = \\frac{\\text{Clicks}}{\\text{Impressions}}\\) | \\(\\text{Spend} = \\text{Clicks} \\times \\text{CPC}\\)")
    
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Monthly Ad Budget", f"\${monthly_budget:,.2f}")
    p2.metric("Projected Impressions", f"{int(est_impressions):,}")
    p3.metric("Projected Clicks (Sessions)", f"{int(est_clicks):,}")
    p4.metric("Benchmark CTR %", f"{ctr_benchmark*100:.1f}%")

# --- MODULE 4: AD BUILDER & AD ASSETS ---
with tab4:
    st.header("Module 4: Responsive Search Ad & Ad Assets Builder")
    st.write("Build your ad copy and include **Ad Assets** (Step 6) to increase Quality Score and CTR.")
    
    col_copy, col_assets, col_preview = st.columns([1.2, 1.2, 1.5])
    
    with col_copy:
        st.subheader("1. Main Ad Copy")
        h1 = st.text_input("Headline 1 (Max 30 chars):", value=f"Official {brand}")
        h2 = st.text_input("Headline 2 (Max 30 chars):", value="Top Rated Experience in NYC")
        h3 = st.text_input("Headline 3 (Max 30 chars):", value="Book & Reserve Online Today")
        
        d1 = st.text_area("Description 1 (Max 90 chars):", value=f"Discover why New Yorkers choose {brand}. Educational, authentic, and top-rated service.")
        d2 = st.text_area("Description 2 (Max 90 chars):", value="Explore pricing, upcoming events, and customer reviews. Visit our official site now!")
        display_url = st.text_input("Display URL:", value=f"www.{brand.lower().replace(' ', '')}.com/nyc")

    with col_assets:
        st.subheader("2. Ad Assets (Extensions)")
        inc_sitelinks = st.checkbox("Include Sitelink Assets", value=True)
        sitelink_text = st.text_input("Sitelink 1 Text:", value="View Pricing & Packages") if inc_sitelinks else ""
        
        inc_callout = st.checkbox("Include Callout Assets", value=True)
        callout_text = st.text_input("Callout Highlights:", value="24/7 Support • No Hidden Fees • Top Rated") if inc_callout else ""
        
        inc_call = st.checkbox("Include Phone Call Asset", value=True)
        phone_num = st.text_input("Phone Number:", value="(212) 555-0199") if inc_call else ""
        
        inc_location = st.checkbox("Include Location Asset (Google Maps)", value=True)
        inc_rating = st.checkbox("Include Star Rating / Reviews Asset", value=True)
        inc_image = st.checkbox("Include Visual Image Asset", value=True)
        image_url = st.text_input("Image Asset URL:", value="https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=200") if inc_image else ""

    with col_preview:
        st.subheader("3. Live Google SERP Ad Preview")
        
        # Render SERP Box
        rating_html = "⭐ 4.9 (128 reviews) • Business Rating" if inc_rating else ""
        phone_html = f"📞 Call {phone_num}" if inc_call else ""
        location_html = "📍 197 E 3rd St, East Village, NYC" if inc_location else ""
        sitelink_html = f"<u>{sitelink_text}</u> • <u>Contact Us</u> • <u>FAQs</u>" if inc_sitelinks else ""
        
        st.markdown(
            f"""
            <div style="border: 1px solid #dadce0; border-radius: 8px; padding: 16px; background-color: #ffffff; font-family: Arial, sans-serif;">
                <div style="font-size: 12px; color: #202124;">
                    <span style="font-weight: bold;">Sponsored</span> • <span>{display_url}</span>
                </div>
                <h3 style="color: #1a0dab; margin: 4px 0px; font-size: 18px; line-height: 1.3;">{h1} | {h2} | {h3}</h3>
                <div style="color: #4d5156; font-size: 13px; margin-bottom: 6px;">{d1} {d2}</div>
                {"<div style='color: #f4b400; font-size: 12px; margin-bottom: 4px;'>" + rating_html + "</div>" if inc_rating else ""}
                {"<div style='color: #006621; font-size: 12px; margin-bottom: 4px;'>" + callout_text + "</div>" if inc_callout else ""}
                {"<div style='color: #1a0dab; font-size: 12px; margin-bottom: 4px;'>" + sitelink_html + "</div>" if inc_sitelinks else ""}
                {"<div style='color: #5f6368; font-size: 12px;'>" + location_html + " " + phone_html + "</div>" if (inc_location or inc_call) else ""}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Ad Quality & Policy Check
        st.subheader("🛡️ Policy & Quality Check")
        asset_count = sum([inc_sitelinks, inc_callout, inc_call, inc_location, inc_rating, inc_image])
        if asset_count >= 3:
            st.success(f"✅ Quality Score Boost: {asset_count} Ad Assets Included (Google recommends 3+)")
        else:
            st.warning(f"⚠️ Only {asset_count} Ad Assets selected. Add more assets to improve Quality Score.")

# --- MODULE 5: GA4 ANALYTICS DASHBOARD ---
with tab5:
    st.header("Module 5: Simulated GA4 Performance & Channel Attribution")
    
    if st.button("🚀 Launch Campaign & Run GA4 Analytics Simulation"):
        conv_rate = 0.034 # 3.4% conversion rate
        conversions = int(est_clicks * conv_rate)
        cpa = monthly_budget / conversions if conversions > 0 else 0
        roas = (conversions * 95.00) / monthly_budget if monthly_budget > 0 else 0
        
        st.subheader("📈 GA4 Campaign Overview (Paid Search Channel)")
        g1, m2, g3, g4, g5 = st.columns(5)
        g1.metric("GA4 Sessions (Clicks)", f"{int(est_clicks):,}")
        m2.metric("Total Spend", f"\${monthly_budget:,.2f}")
        g3.metric("Conversions", f"{conversions}")
        g4.metric("Cost Per Acquisition (CPA)", f"\${cpa:.2f}")
        g5.metric("Target ROAS", f"{roas:.2f}x")
        
        # Simulated 30-Day Trend
        days = np.arange(1, 31)
        daily_sessions = np.random.normal(est_clicks / 30, 4, 30).astype(int)
        chart_df = pd.DataFrame({"Day": days, "GA4 Paid Search Traffic": daily_sessions})
        st.line_chart(chart_df.set_index("Day"))
        
        st.subheader("📊 GA4 Default Channel Grouping Comparison Table")
        st.caption("How Paid Search performs alongside Organic Search, Direct, and Organic Social in GA4:")
        
        channel_df = pd.DataFrame({
            "Default Channel Grouping": ["Paid Search (Google Ads)", "Organic Search (Google)", "Direct", "Organic Social (TikTok/IG)"],
            "Sessions": [int(est_clicks), int(est_clicks * 1.5), int(est_clicks * 0.7), int(est_clicks * 1.2)],
            "Engagement Rate %": ["68.5%", "73.2%", "52.0%", "59.4%"],
            "Conversions": [conversions, int(conversions * 1.4), int(conversions * 0.6), int(conversions * 0.8)],
            "Conversion Rate %": ["3.4%", "3.2%", "2.5%", "2.1%"]
        })
        st.table(channel_df)
        
        # Diagnostic Feedback Narrative
        st.info(
            f"💡 **GA4 Diagnostic Analysis for {brand}:**\n"
            f"* **Paid Search Conversion Rate (3.4%)** outperforms Organic Social (2.1%) because paid search targets buyers in the **Decision Stage** who are actively searching for solutions.\n"
            f"* **Attribution Insight:** Paid Search generated **{conversions} direct conversions** while driving secondary brand awareness. UTM campaign tag (`{utm_campaign}`) successfully captured all attribution data in GA4."
        )
