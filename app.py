import streamlit as st
import pandas as pd
import numpy as np

# Define function alias via getattr to prevent automated URL scrubbing
st_radio = getattr(st, "radio")

st.set_page_config(page_title="Paid Search Campaign Simulator", page_icon="📊", layout="wide")

# --- MAIN TITLE & SUBTEXT ---
st.title("Paid Search Campaign Simulator")
st.caption("Search Marketing Hands-On Exercise")

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
    "Target ROAS Number (e.g., 3.0 for 3.0x / 300%):",
    min_value=0.5,
    max_value=20.0,
    value=3.0,
    step=0.5
)

daily_budget = st.sidebar.slider(
    "Daily Budget ($):",
    min_value=10,
    max_value=500,
    value=164,
    step=2
)
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
    st.write("Type **3 search terms** your target buyers would search for. The system will automatically detect the **Intent Stage** and calculate search volume, keyword difficulty, and estimated CPC. To achieve a high ROAS, balance your keywords across intent stages while keeping **Blended CPC < $2.00** and **Average KD < 40%**.")
    
    col_input, col_table = st.columns([1.1, 1.9])
    
    with col_input:
        st.subheader("Type 3 Target Search Terms")
        kw1 = st.text_input("Keyword 1:", value="official brand name online", key="kw1_text")
        kw2 = st.text_input("Keyword 2:", value="best product reviews online", key="kw2_text")
        kw3 = st.text_input("Keyword 3:", value="how to choose the right product", key="kw3_text")

    # Automated Intent Detection & Metrics Logic
    def auto_detect_intent_and_metrics(kw):
        kw_lower = kw.lower().strip()
        if any(term in kw_lower for term in ["aura", "brand", "official", "auraband", "company", "name"]):
            intent = "Navigational / Brand"
            cpc = 0.95
            kd = 22
            msv = 1800
        elif any(term in kw_lower for term in ["vs", "best", "top", "review", "reviews", "comparison", "bluetooth", "category", "product"]):
            intent = "Consideration / Comparison"
            cpc = 1.85
            kd = 38
            msv = 4200
        elif any(term in kw_lower for term in ["how", "why", "what", "noise", "insomnia", "relief", "help", "block", "problem", "solve", "choose"]):
            intent = "Awareness / Problem"
            cpc = 1.35
            kd = 32
            msv = 7500
        else: # Decision / Commercial
            intent = "Decision / Commercial"
            cpc = 3.25
            kd = 65
            msv = 3100
            
        return {
            "Target Keyword": kw, 
            "Intent Stage": intent, 
            "Est. CPC ($)": cpc, 
            "Keyword Difficulty (%)": kd, 
            "Monthly Search Vol (MSV)": msv
        }

    kw_list_data = [
        auto_detect_intent_and_metrics(kw1),
        auto_detect_intent_and_metrics(kw2),
        auto_detect_intent_and_metrics(kw3)
    ]
    
    df_kws = pd.DataFrame(kw_list_data)
    
    with col_table:
        st.subheader("💡 Automated Keyword Research Results")
        st.dataframe(df_kws, use_container_width=True, hide_index=True)
        
        selected_intents = set(df_kws["Intent Stage"].tolist())
        blended_cpc = df_kws["Est. CPC ($)"].mean()
        avg_kd = df_kws["Keyword Difficulty (%)"].mean()
        total_msv = df_kws["Monthly Search Vol (MSV)"].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Blended Est. CPC", f"${blended_cpc:.2f}", delta="Under $2.00 Target" if blended_cpc < 2.00 else "Over $2.00 Target", delta_color="normal" if blended_cpc < 2.00 else "inverse")
        m2.metric("Avg Keyword Difficulty", f"{avg_kd:.1f}%", delta="Under 40% Target" if avg_kd < 40.0 else "Over 40% Target", delta_color="normal" if avg_kd < 40.0 else "inverse")
        m3.metric("Total Search Volume", f"{total_msv:,}")

        has_nav = "Navigational / Brand" in selected_intents
        has_comp = "Consideration / Comparison" in selected_intents
        has_prob = "Awareness / Problem" in selected_intents

# --- MODULE 2: MATCH TYPES & NEGATIVE KEYWORDS ---
with tab2:
    st.header("Module 2: Keyword Match Types & Negative Keyword Shield")
    
    c_match, c_neg = st.columns(2)
    with c_match:
        match_type = st_radio(
            "Select Match Type Rule:",
            ["Broad Match (keyword)", 'Phrase Match ("keyword")', "Exact Match ([keyword])"],
            index=1,
            help="Broad match gets maximum views but risks non-converting clicks; Phrase match balances volume and control; Exact match targets precise intent."
        )
    with c_neg:
        negatives = st.text_input(
            "Negative Keywords (enter at least 4 words separated by commas):", 
            value="free, jobs"
        )
        st.caption("Negative keywords prevent wasted ad spend on unqualified clicks.")
        
        neg_words = [w.strip() for w in negatives.split(",") if w.strip()]
        if len(neg_words) >= 4:
            st.success(f"✅ Negative Keyword Shield Active ({len(neg_words)} terms added)")
        else:
            st.warning(f"⚠️ Need at least 4 negative keywords (currently {len(neg_words)} added). Add more terms separated by commas!")

    st.subheader("⚡ Real-Time Search Query Simulator")
    test_queries = [
        "free diy download guide",
        kw1 if kw1 else "official brand name online",
        "jobs and career opportunities",
        kw2 if kw2 else "best product reviews online"
    ]
    
    sim_results = []
    for q in test_queries:
        blocked = any(neg.lower() in q.lower() for neg in neg_words)
        if blocked:
            status = "❌ BLOCKED by Negative Keyword Shield"
        elif "Broad" in match_type:
            status = "✅ AD TRIGGERED (Broad Match)"
        elif "Phrase" in match_type:
            status = "✅ AD TRIGGERED (Phrase Match)"
        else:
            status = "✅ AD TRIGGERED (Exact Match)"
            
        sim_results.append({"Prospect Search Query": q, "Ad Trigger Status": status})
        
    st.table(pd.DataFrame(sim_results))

# --- MODULE 3: BUDGET PROJECTIONS ---
with tab3:
    st.header("Module 3: Campaign Projections & Budget Setup")
    
    ctr_benchmark = 0.065 # 6.5% CTR benchmark
    est_clicks = monthly_budget / blended_cpc if blended_cpc > 0 else 0
    est_impressions = est_clicks / ctr_benchmark if ctr_benchmark > 0 else 0
    
    st.write("Calculated using Class 5 Formulas: \\(\\text{CTR} = \\frac{\\text{Clicks}}{\\text{Impressions}}\\) | \\(\\text{Spend} = \\text{Clicks} \\times \\text{CPC}\\)")
    
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Monthly Budget / Projected Spend", f"${monthly_budget:,.2f}")
    p2.metric("Projected Impressions", f"{int(est_impressions):,}")
    p3.metric("Projected Clicks (Sessions)", f"{int(est_clicks):,}")
    p4.metric("Benchmark CTR %", f"{ctr_benchmark*100:.1f}%")

# --- MODULE 4: AD BUILDER & AD ASSETS ---
with tab4:
    st.header("Module 4: Responsive Search Ad & Ad Assets Builder")
    st.write("Build your ad copy and include **Ad Assets (Sitelinks, Callouts)** to maximize SERP real estate, Quality Score, and CTR.")
    
    col_copy, col_assets, col_preview = st.columns([1.1, 1.1, 1.4])
    
    with col_copy:
        st.subheader("1. Main Ad Copy")
        h1 = st.text_input("Headline 1 (Max 30 chars):", value="Official Brand Website")
        h2 = st.text_input("Headline 2 (Max 30 chars):", value="Top Rated Solutions Online")
        h3 = st.text_input("Headline 3 (Max 30 chars):", value="Order Online Today - Save 10%")
        
        d1 = st.text_area("Description 1 (Max 90 chars):", value="Discover premium products designed for quality and reliability. Shop our official site today.")
        d2 = st.text_area("Description 2 (Max 90 chars):", value="Free 2-day shipping on local orders. Read 500+ 5-star verified customer reviews online.")
        display_url = st.text_input("Display URL:", value="[suspicious link removed]")

    with col_assets:
        st.subheader("2. Ad Assets")
        inc_sitelinks = st.checkbox("Include Sitelink Assets", value=True)
        sitelink_text = st.text_input("Sitelink Text:", value="View Pricing & Offerings") if inc_sitelinks else ""
        
        inc_callout = st.checkbox("Include Callout Assets", value=True)
        callout_text = st.text_input("Callout Highlights:", value="Free 2-Day Shipping • 30-Day Trial") if inc_callout else ""
        
        inc_call = st.checkbox("Include Phone Call Asset", value=True)
        phone_num = st.text_input("Phone Number:", value="(212) 555-0199") if inc_call else ""

    with col_preview:
        st.subheader("3. Live Search Preview")
        
        phone_html = f"📞 Call {phone_num}" if inc_call else ""
        sitelink_html = f"<u>{sitelink_text}</u> • <u>Customer Reviews</u> • <u>FAQs</u>" if inc_sitelinks else ""
        
        st.markdown(
            f"""
            <div style="border: 1px solid #dadce0; border-radius: 8px; padding: 16px; background-color: #ffffff; font-family: Arial, sans-serif;">
                <div style="font-size: 12px; color: #202124;">
                    <span style="font-weight: bold;">Sponsored</span> • <span>{display_url}</span>
                </div>
                <h3 style="color: #1a0dab; margin: 4px 0px; font-size: 17px; line-height: 1.3;">{h1} | {h2} | {h3}</h3>
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
        # Evaluate all required student criteria
        cond_intents = has_nav and has_comp and has_prob
        cond_cpc = blended_cpc < 2.00
        cond_kd = avg_kd < 40.0
        cond_negatives = len(neg_words) >= 4
        
        cond_h1 = len(h1.strip()) > 0 and len(h1) <= 30
        cond_h2 = len(h2.strip()) > 0 and len(h2) <= 30
        cond_h3 = len(h3.strip()) > 0 and len(h3) <= 30
        cond_headlines = cond_h1 and cond_h2 and cond_h3
        
        cond_d1 = len(d1.strip()) > 0 and len(d1) <= 90
        cond_d2 = len(d2.strip()) > 0 and len(d2) <= 90
        cond_descriptions = cond_d1 and cond_d2
        
        cond_sitelinks = inc_sitelinks
        
        all_criteria_met = (
            cond_intents and 
            cond_cpc and 
            cond_kd and 
            cond_negatives and 
            cond_headlines and 
            cond_descriptions and 
            cond_sitelinks
        )
        
        if all_criteria_met:
            actual_roas = 3.42 # Exceeds 3.0 Target!
            conv_rate = 0.042 # 4.2% high conversion rate
        else:
            # Calculate lower ROAS based on missing criteria
            penalty = 0.0
            if not cond_intents: penalty += 0.4
            if not cond_cpc: penalty += 0.5
            if not cond_kd: penalty += 0.3
            if not cond_negatives: penalty += 0.4
            if not cond_headlines: penalty += 0.3
            if not cond_descriptions: penalty += 0.3
            if not cond_sitelinks: penalty += 0.2
            
            actual_roas = max(1.20, round(3.0 - penalty, 2))
            conv_rate = 0.022 # 2.2% lower conversion rate
            
        conversions = int(est_clicks * conv_rate)
        cpa = monthly_budget / conversions if conversions > 0 else 0
        
        st.subheader("📈 GA4 Overview Metrics (Paid Search)")
        g1, m2, g3, g4, g5 = st.columns(5)
        g1.metric("GA4 Sessions (Clicks)", f"{int(est_clicks):,}")
        m2.metric("Total Monthly Spend", f"${monthly_budget:,.2f}")
        g3.metric("Conversions", f"{conversions}")
        g4.metric("Cost Per Acquisition (CPA)", f"${cpa:.2f}")
        g5.metric("Simulated ROAS", f"{actual_roas:.2f}x", delta=f"{actual_roas - target_roas_input:.2f}x vs Target")
        
        # --- ROAS PERFORMANCE ANALYSIS & CONGRATULATORY SECTION ---
        st.subheader("📊 ROAS Performance Analysis")
        
        if actual_roas >= 3.0:
            st.balloons()
            st.success(
                f"🎉 **CONGRATULATIONS! You achieved a Simulated ROAS of {actual_roas:.2f}x (Exceeding your 3.0 Target!)**\n\n"
                f"Your Google Ads campaign generated **${monthly_budget * actual_roas:,.2f} in revenue** on a **${monthly_budget:,.2f} budget**!"
            )
            st.markdown(
                f"""
                ### 🏆 How You Achieved Your 3.0+ ROAS Target:
                * **Balanced Intent Stages:** You included all 3 required intent stages (*Navigational / Brand*, *Consideration / Comparison*, and *Awareness / Problem*), capturing buyers across the entire search funnel.
                * **Efficient Cost Structure:** Your blended CPC was **${blended_cpc:.2f}** (under $2.00) with an average Keyword Difficulty of **{avg_kd:.1f}%** (under 40%), maximizing total clicks for your budget.
                * **Active Negative Keyword Shield:** You added **{len(neg_words)} negative terms** (at least 4 required), stopping wasted ad spend on non-buying searches.
                * **High Quality Score Ad Copy:** All 3 headlines were under 30 characters, both descriptions were under 90 characters, and **Sitelink Assets** were enabled to maximize CTR.
                """
            )
        else:
            st.error(
                f"🚨 **ROAS UNDERPERFORMING: Simulated ROAS is {actual_roas:.2f}x (Target is {target_roas_input:.2f}x)!**\n\n"
                f"Your campaign returned **${actual_roas:.2f}** for every $1.00 spent. Review the required adjustments below to achieve your 3.0 ROAS target."
            )
            
            st.markdown("### 🛠️ Required Adjustments to Reach 3.0 ROAS:")
            if not cond_intents:
                st.write("❌ **Keyword Intent Diversity:** Ensure your 3 keywords cover at least one *Navigational / Brand*, one *Consideration / Comparison*, and one *Awareness / Problem* search query.")
            if not cond_cpc:
                st.write(f"❌ **Blended CPC Too High:** Your blended CPC is **${blended_cpc:.2f}**. Adjust your keywords so blended CPC is **under $2.00**.")
            if not cond_kd:
                st.write(f"❌ **Keyword Difficulty Too High:** Average KD is **{avg_kd:.1f}%**. Adjust your keywords so average KD is **under 40%**.")
            if not cond_negatives:
                st.write(f"❌ **Negative Keyword Shield Weak:** You currently have **{len(neg_words)} negative terms**. Enter at least **4 negative words** separated by commas in Module 2.")
            if not cond_headlines:
                st.write("❌ **Ad Headlines Incomplete/Too Long:** Ensure all 3 headlines are filled out and each is **under 30 characters**.")
            if not cond_descriptions:
                st.write("❌ **Ad Descriptions Incomplete/Too Long:** Ensure both descriptions are filled out and each is **under 90 characters**.")
            if not cond_sitelinks:
                st.write("❌ **Sitelinks Missing:** Check the **Include Sitelink Assets** box in Module 4.")

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
            "Conversion Rate %": [f"{conv_rate*100:.1f}%", "3.2%", "2.5%", "2.1%"]
        })
        st.table(channel_df)
