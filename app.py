import streamlit as st
import pandas as pd
import plotly.express as px

# Configure enterprise page parameters
st.set_page_config(
    page_title="Q-Commerce Performance Analytics Suite", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Application Header and Context
st.title("Quick Commerce Business Intelligence Dashboard")
st.markdown("""
This analytics framework provides data aggregation and business performance visualization 
for hyper-local fulfillment applications. Upload consolidated files or input single transactions 
to generate real-time metrics.
""")

# Operational Workspace Segmentation
tab1, tab2 = st.tabs(["Bulk File Upload (CSV)", "Manual Order Ledger"])

# Instantiation of structural variable
df = None

# --- SECTION 1: BULK DATA INGESTION ---
with tab1:
    st.subheader("Automated Data Processing")
    uploaded_file = st.file_uploader(
        "Select target store transaction ledger (.csv format)", 
        type=["csv"],
        help="Ensure the source dataset contains categorical platform and numeric order value parameters."
    )
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("Dataset successfully ingested and parsed.")

# --- SECTION 2: TRANSACTION ENTRY CONTROL ---
with tab2:
    st.subheader("Granular Transaction Logging")
    
    # Structural Input Configuration
    col1, col2, col3 = st.columns(3)
    with col1:
        input_app = st.selectbox(
            "Fulfillment Platform", 
            ["Blinkit", "Swiggy Instamart", "Zepto", "BigBasket", "Other"]
        )
    with col2:
        input_val = st.number_input(
            "Gross Order Value (INR)", 
            min_value=0.0, 
            step=50.0, 
            value=250.0
        )
    with col3:
        input_disc = st.selectbox(
            "Marketing Incentive Applied", 
            ["Yes", "No"]
        )
        
    # Initialization of cache array for persistent session capture
    if 'manual_data' not in st.session_state:
        st.session_state.manual_data = pd.DataFrame(columns=['Platform', 'Order_Value', 'Discount'])
        
    if st.button("Commit Record to Session Log"):
        new_row = pd.DataFrame([{'Platform': input_app, 'Order_Value': input_val, 'Discount': input_disc}])
        st.session_state.manual_data = pd.concat([st.session_state.manual_data, new_row], ignore_index=True)
        st.toast("Transaction logged successfully.")
        
    if not st.session_state.manual_data.empty:
        st.markdown("**Active Session Transactions**")
        st.dataframe(st.session_state.manual_data, use_container_width=True)
        if df is None:  
            df = st.session_state.manual_data.copy()
            # Canonical key mapping for runtime safety
            df.columns = ['company', 'order_value', 'discount_applied']

# --- SECTION 3: CORE QUANTITATIVE METRICS & VISUALIZATIONS ---
if df is not None:
    # Key normalization to mitigate structural variances in customer schemas
    df.columns = [c.lower().strip() for c in df.columns]
    
    # Core Coordinate Identification
    val_col = next((c for c in df.columns if c in ['order_value', 'amount', 'total_price', 'price', 'sales']), None)
    plat_col = next((c for c in df.columns if c in ['company', 'platform', 'app', 'store']), None)
    disc_col = next((c for c in df.columns if c in ['discount_applied', 'discount', 'promo', 'coupon']), None)
    
    if val_col and plat_col:
        df[val_col] = pd.to_numeric(df[val_col], errors='coerce').fillna(0)
        
        st.markdown("---")
        st.subheader("Key Performance Indicators Summary")
        
        # Calculation Logic Execution
        total_rev = df[val_col].sum()
        total_orders = len(df)
        aov = total_rev / total_orders if total_orders > 0 else 0
        
        # KPI Metric Allocation Matrix
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Gross Processing Revenue", f"INR {total_rev:,.2f}")
        kpi2.metric("Total Order Volume", f"{total_orders:,} Transactions")
        kpi3.metric("Average Order Value (AOV)", f"INR {aov:,.2f}")
        
        # Layout splitting for adjacent visualization rendering
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown("#### Revenue Distribution by Platform")
            platform_summary = df.groupby(plat_col)[val_col].sum().reset_index()
            fig_bar = px.bar(
                platform_summary, 
                x=plat_col, 
                y=val_col, 
                labels={plat_col: "Channel / Platform", val_col: "Aggregated Gross Revenue (INR)"},
                color=plat_col, 
                template="plotly_white"
            )
            fig_bar.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with chart_col2:
            if disc_col:
                st.markdown("#### Incentive Optimization Analysis")
                df[disc_col] = df[disc_col].astype(str).str.lower().replace({'1': 'yes', 'true': 'yes', 'applied': 'yes'})
                df['Promo Status'] = df[disc_col].apply(lambda x: 'Incentivized Order' if 'yes' in x or 'y' in x else 'Organic Full-Price')
                
                discount_summary = df.groupby('Promo Status')[val_col].sum().reset_index()
                fig_pie = px.pie(
                    discount_summary, 
                    values=val_col, 
                    names='Promo Status', 
                    color_discrete_sequence=px.colors.sequential.Slate, 
                    hole=0.4
                )
                fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10))
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Discount parameters missing from current schema; skipping optimization view.")
    else:
        st.error("Execution Halted: Source columns could not be verified. Ensure structural labels match 'Platform' and 'Order Value'.")
else:
    st.info("System awaiting data injection. Please process a batch CSV document or establish a manual operational record tracking stream above.")
