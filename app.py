import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Q-Commerce Analytics Suite", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Custom Corporate Style Sheet Injection
st.markdown("""
<style>
    .reportview-container { background: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1f2937; border-radius: 8px; padding: 15px; border: 1px solid #374151; }
    div[data-testid="stMetricValue"] { font-family: 'Roboto Monospace', monospace; font-size: 2rem; color: #38bdf8; }
</style>
""", unsafe_allow_html=True)

st.title("Quick Commerce Business Intelligence Dashboard")
st.markdown("""
This analytics framework provides data aggregation, predictive forecasting, and interactive 
business performance visualization for hyper-local fulfillment applications.
""")

st.sidebar.subheader("Localization Controls")
currency = st.sidebar.selectbox("Reporting Currency Baseline", ["INR", "USD", "EUR", "AED"])
rates = {"INR": 1.0, "USD": 0.012, "EUR": 0.011, "AED": 0.044}
fx_factor = rates[currency]
currency_symbol = "₹" if currency == "INR" else "$" if currency == "USD" else "€" if currency == "EUR" else "AED "

# State initialization for active session tracker
if 'orders_db' not in st.session_state:
    st.session_state.orders_db = pd.DataFrame(columns=['Platform', 'Order_Value', 'Discount', 'Operational_Day'])

t_bulk, t_manual = st.tabs(["Bulk Data Processing Engine", "Granular Transaction Ingestion Log"])
df = None

with t_bulk:
    st.subheader("Automated Dataset Parsing Matrix")
    st.markdown("""
    **Required CSV Layout Template:**
    Your uploaded file must contain the following column headers and data formats:
    
    | Company | Order_Value | Discount_Applied | Operational_Day |
    | :--- | :--- | :--- | :--- |
    | Blinkit | 450.00 | Yes | 1 |
    | Zepto | 210.50 | No | 1 |
    | Swiggy Instamart | 890.00 | Yes | 2 |
    """)
    
    src_file = st.file_uploader(
        "Select target store transaction ledger (.csv format)", 
        type=["csv"],
        help="Ensure the source dataset contains categorical platform and numeric order value parameters."
    )
    if src_file is not None:
        df = pd.read_csv(src_file)
        st.success("Dataset successfully ingested and parsed from active volume storage.")

with t_manual:
    st.subheader("Granular Transaction Ledger Administration")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        inp_platform = st.selectbox("Fulfillment Platform", ["Blinkit", "Swiggy Instamart", "Zepto", "BigBasket", "Other"])
    with c2:
        inp_value = st.number_input("Gross Order Value (INR Basis)", min_value=0.0, step=50.0, value=250.0)
    with c3:
        inp_discount = st.selectbox("Marketing Incentive Applied", ["Yes", "No"])
    with c4:
        inp_day = st.slider("Operational Time Index (Day Count)", min_value=1, max_value=30, value=1)
        
    if st.button("Commit Record to Distributed Ledger"):
        new_entry = pd.DataFrame([{'Platform': inp_platform, 'Order_Value': inp_value, 'Discount': inp_discount, 'Operational_Day': inp_day}])
        st.session_state.orders_db = pd.concat([st.session_state.orders_db, new_entry], ignore_index=True)
        st.toast("Transaction successfully compiled to persistent session stream storage.")
        
    if not st.session_state.orders_db.empty:
        st.markdown("**Active Secure Data Vault Transactions**")
        st.dataframe(st.session_state.orders_db, use_container_width=True)
        if df is None:  
            df = st.session_state.orders_db.copy()
            df.columns = ['company', 'order_value', 'discount_applied', 'operational_day']





if df is not None:
    df.columns = [c.lower().strip() for c in df.columns]
    val_col = next((c for c in df.columns if c in ['order_value', 'amount', 'total_price', 'price', 'sales']), None)
    plat_col = next((c for c in df.columns if c in ['company', 'platform', 'app', 'store']), None)
    disc_col = next((c for c in df.columns if c in ['discount_applied', 'discount', 'promo', 'coupon']), None)
    day_col = next((c for c in df.columns if c in ['operational_day', 'day', 'time', 'date']), None)
    
    if val_col and plat_col:
        df[val_col] = pd.to_numeric(df[val_col], errors='coerce').fillna(0) * fx_factor
        
        if not day_col:
            df['operational_day'] = np.random.randint(1, 10, size=len(df))
            day_col = 'operational_day'
        else:
            df[day_col] = pd.to_numeric(df[day_col], errors='coerce').fillna(1)
            
        df = df.sort_values(by=[day_col])

        st.markdown("---")
        st.subheader("Key Performance Indicators Summary Matrix")
        
        rev_total = df[val_col].sum()
        orders_total = len(df)
        aov_metric = rev_total / orders_total if orders_total > 0 else 0
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Gross Reporting Revenue Volume", f"{currency_symbol}{rev_total:,.2f}")
        m2.metric("System Transaction Volume", f"{orders_total:,} Operational Actions")
        m3.metric("Calculated Average Order Value (AOV)", f"{currency_symbol}{aov_metric:,.2f}")
        
        st.markdown("### Interactive Graphical Evaluation Control Workspace")
        t_bar, t_pie, t_trend, t_hist, t_scatter = st.tabs([
            "Bar Chart Matrix", "Pie Distribution", "Trend Line Tracker", "Distribution Histogram", "Variable Scatter Map"
        ])
        
        with t_bar:
            st.markdown("#### Volumetric Revenue Contributions by Operating Channel")
            grp_platform = df.groupby([plat_col, day_col])[val_col].sum().reset_index()
            fig_bar = px.bar(
                grp_platform, x=plat_col, y=val_col, color=plat_col,
                animation_frame=day_col, range_y=[0, grp_platform[val_col].max() * 1.2],
                labels={plat_col: "Operating Channel", val_col: f"Gross Revenue ({currency})"},
                template="plotly_white"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with t_pie:
            if disc_col:
                st.markdown("#### System Marketing Incentive Yield Share Optimization")
                df[disc_col] = df[disc_col].astype(str).str.lower().replace({'1': 'yes', 'true': 'yes', 'applied': 'yes'})
                df['Promo Status'] = df[disc_col].apply(lambda x: 'Incentivized Order' if 'yes' in x or 'y' in x else 'Organic Full-Price')
                
                grp_discount = df.groupby('Promo Status')[val_col].sum().reset_index()
                fig_pie = px.pie(
                    grp_discount, values=val_col, names='Promo Status', 
                    color_discrete_sequence=px.colors.sequential.Plotly3, hole=0.4
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Incentive field variables missing from source parameters.")

        with t_trend:
            st.markdown("#### Longitudinal Metric Performance Trends and Statistical Forecast Projections")
            grp_trend = df.groupby(day_col)[val_col].sum().reset_index()
            if len(grp_trend) > 1:
                x = grp_trend[day_col].values
                y = grp_trend[val_col].values
                slope, intercept = np.polyfit(x, y, 1)
                forecast_steps = np.array(list(range(int(max(x)) + 1, int(max(x)) + 6)))
                forecast_vals = slope * forecast_steps + intercept
                
                hist_data = pd.DataFrame({day_col: x, 'Revenue Baseline': y, 'Data Type': 'Historical Matrix'})
                pred_data = pd.DataFrame({day_col: forecast_steps, 'Revenue Baseline': forecast_vals, 'Data Type': 'Statistical Forecast Model'})
                unified_trend = pd.concat([hist_data, pred_data], ignore_index=True)
                
                fig_line = px.line(
                    unified_trend, x=day_col, y='Revenue Baseline', color='Data Type',
                    line_dash='Data Type', labels={day_col: "Operational Day Index", 'Revenue Baseline': f"Value Volume ({currency})"},
                    template="plotly_white"
                )
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("Insufficient timeline tracking points found. Ensure multiple distinct values exist under the 'Operational Day' parameters to extrapolate regressions.")

        with t_hist:
            st.markdown("#### System Transaction Order Matrix Sizing Densities")
            fig_hist = px.histogram(
                df, x=val_col, nbins=20, color=plat_col,
                labels={val_col: f"Transaction Value Boundaries ({currency})"},
                template="plotly_white", barmode="overlay"
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with t_scatter:
            st.markdown("#### Dimensional Variance Analysis Vector Matrix Space")
            fig_scatter = px.scatter(
                df, x=day_col, y=val_col, color=plat_col, size=val_col,
                labels={day_col: "Temporal Day Axis", val_col: f"Revenue Coordinates ({currency})"},
                template="plotly_white"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("---")
        st.subheader("Corporate Export Controls Gateway")
        
        brief_text = f"""==================================================
      EXECUTIVE INTELLIGENCE MANAGEMENT BRIEF
==================================================
Reporting Run Currency Metric Space: {currency}
Total System Transactions Compiled: {orders_total}
Aggregated Enterprise Gross Capital Yield: {rev_total:,.2f}
Operational Unit Processing Efficiency Average (AOV): {aov_metric:,.2f}
=================================================="""
        
        st.download_button(
            label="Compile and Download Executive Analytical Summary Document",
            data=brief_text,
            file_name="executive_intelligence_brief.txt",
            mime="text/plain"
        )
    else:
        st.error("Structure Error: Unable to extract required analytics fields. Re-verify document layout maps correctly.")
else:
    st.info("System awaiting infrastructure payload execution. Deliver data matrices using upload grids or register specific line transactions.")
