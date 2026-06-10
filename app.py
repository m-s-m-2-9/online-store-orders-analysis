import streamlit as sns
import streamlit as st
import pandas as pd
import plotly.express

 as px

# Set up clean professional page layout
st.set_page_config(page_title="Q-Commerce Analytics Dashboard", layout="wide")

st.title("📊 Quick Commerce Business Performance Analytics")
st.markdown("Easily evaluate your store metrics. Upload a transactional file or manually input daily data below.")

# Create Two Tabs: One for File Upload, One for Manual Input
tab1, tab2 = st.tabs(["📁 Bulk File Upload (CSV)", "✍️ Manual Order Entry"])

# Global variable to hold dataframe for analysis
df = None

# --- TAB 1: FILE UPLOAD ---
with tab1:
    uploaded_file = st.file_uploader("Upload your store orders file (CSV format)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")

# --- TAB 2: MANUAL ENTRY ---
with tab2:
    st.subheader("Add a New Transaction Record")
    
    # Form layout columns
    col1, col2, col3 = st.columns(3)
    with col1:
        input_app = st.selectbox("Platform/App Name", ["Blinkit", "Swiggy Instamart", "Zepto", "BigBasket", "Other"])
    with col2:
        input_val = st.number_input("Order Bill Amount (INR)", min_value=0.0, step=10.0, value=250.0)
    with col3:
        input_disc = st.selectbox("Discount Applied?", ["Yes", "No"])
        
    # Temporary mock database structure for manual entry demonstration
    if 'manual_data' not in st.session_state:
        st.session_state.manual_data = pd.DataFrame(columns=['Platform', 'Order_Value', 'Discount'])
        
    if st.button("➕ Add Order to Session"):
        new_row = pd.DataFrame([{'Platform': input_app, 'Order_Value': input_val, 'Discount': input_disc}])
        st.session_state.manual_data = pd.concat([st.session_state.manual_data, new_row], ignore_index=True)
        st.toast("Order added to manual log!")
        
    if not st.session_state.manual_data.empty:
        st.write("### Current Logged Manual Orders")
        st.dataframe(st.session_state.manual_data, use_container_width=True)
        if df is None:  # Use manual data if no file is uploaded
            df = st.session_state.manual_data.copy()
            # Standardize names for unified calculations
            df.columns = ['company', 'order_value', 'discount_applied']

# --- UNIFIED ANALYTICS & VISUAL TREND CHARTS ---
if df is not None:
    # Standardize column headers to lowercase to handle varying upload formats
    df.columns = [c.lower().strip() for c in df.columns]
    
    # Identify key metric data coordinates
    val_col = next((c for c in df.columns if c in ['order_value', 'amount', 'total_price', 'price', 'sales']), None)
    plat_col = next((c for c in df.columns if c in ['company', 'platform', 'app', 'store']), None)
    disc_col = next((c for c in df.columns if c in ['discount_applied', 'discount', 'promo']), None)
    
    if val_col and plat_col:
        df[val_col] = pd.to_numeric(df[val_col], errors='coerce').fillna(0)
        
        st.markdown("---")
        st.subheader("📈 Core Business Metrics Summary")
        
        # Calculation KPIs
        total_rev = df[val_col].sum()
        total_orders = len(df)
        aov = total_rev / total_orders if total_orders > 0 else 0
        
        # Display KPIs side-by-side
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Processing Revenue", f"INR {total_rev:,.2f}")
        kpi2.metric("Total Order Volume", f"{total_orders:,} orders")
        kpi3.metric("Average Order Value (AOV)", f"INR {aov:,.2f}")
        
        # VISUAL CHART 1: Bar Chart of Sales Distribution
        st.write("### 🏪 Platform Revenue Performance Split")
        platform_summary = df.groupby(plat_col)[val_col].sum().reset_index()
        fig_bar = px.bar(platform_summary, x=plat_col, y=val_col, 
                         labels={plat_col: "App Platform", val_col: "Total Revenue (INR)"},
                         color=plat_col, template="plotly_white")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # VISUAL CHART 2: Marketing Margin Distribution (Pie Chart)
        if disc_col:
            st.write("### 📣 Promotional Discount vs Full-Price Native Revenue")
            # Map values to a cleaner boolean mask string for display
            df[disc_col] = df[disc_col].astype(str).str.lower().replace({'1': 'yes', 'true': 'yes', 'applied': 'yes'})
            df['Promo Status'] = df[disc_col].apply(lambda x: 'Discounted Order' if 'yes' in x or 'y' in x else 'Organic Full-Price')
            
            discount_summary = df.groupby('Promo Status')[val_col].sum().reset_index()
            fig_pie = px.pie(discount_summary, values=val_col, names='Promo Status', 
                             color_discrete_sequence=px.colors.sequential.RdBu, hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("⚠️ Uploaded file data columns must include variations of 'Platform' and 'Order Value' labels.")
else:
    st.info("💡 Data visualization dashboard will populate here automatically as soon as data file is uploaded or entries are added manually.")
