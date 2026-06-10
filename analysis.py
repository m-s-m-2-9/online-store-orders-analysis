import os

data_file = 'online_orders.csv'
report_file = 'business_report.txt'

if not os.path.exists(data_file):
    with open(report_file, 'w') as f:
        f.write("Error: 'online_orders.csv' not found in the repository.")
    exit()

print("Analyzing Q-Commerce order metrics...")
orders_count = 0
total_revenue = 0
platform_sales = {}
discount_sales = {"Discounted": 0, "Full Price": 0}

with open(data_file, 'r', encoding='utf-8') as f:
    headers = [h.strip().lower() for h in f.readline().split(',')]
    
    # Intelligently find column index positions based on common names
    idx_platform = next((i for i, h in enumerate(headers) if h in ['company', 'platform', 'app', 'store']), None)
    idx_value = next((i for i, h in enumerate(headers) if h in ['order_value', 'amount', 'total_price', 'price', 'order_amount', 'sales']), None)
    idx_discount = next((i for i, h in enumerate(headers) if h in ['discount_applied', 'discount', 'promo', 'coupon']), None)

    for line in f:
        if not line.strip():
            continue
        row = line.strip().split(',')
        
        try:
            val = float(row[idx_value]) if idx_value is not None else 0.0
            plat = row[idx_platform].strip() if idx_platform is not None else "Unknown App"
            
            orders_count += 1
            total_revenue += val
            platform_sales[plat] = platform_sales.get(plat, 0) + val
            
            if idx_discount is not None:
                has_discount = row[idx_discount].strip().lower() in ['yes', '1', 'true', 'applied']
                status = "Discounted" if has_discount else "Full Price"
                discount_sales[status] += val
        except (ValueError, IndexError):
            continue

# Generate the plain-text Business Report
with open(report_file, 'w') as f:
    f.write("==================================================\n")
    f.write("      EXECUTIVE ONLINE STORE ORDERS REPORT       \n")
    f.write("==================================================\n\n")
    f.write(f"Total Completed Orders Analyzed: {orders_count}\n")
    f.write(f"Total Gross Revenue: INR {total_revenue:,.2f}\n")
    
    if orders_count > 0:
        f.write(f"Average Order Value (AOV): INR {total_revenue/orders_count:,.2f}\n\n")
    
    f.write("--- Revenue Breakdown by Platform ---\n")
    for plat, rev in platform_sales.items():
        f.write(f"* {plat}: INR {rev:,.2f}\n")
        
    f.write("\n--- Marketing Performance ---\n")
    for status, rev in discount_sales.items():
        f.write(f"* {status} Revenue: INR {rev:,.2f}\n")

print("Analysis complete. business_report.txt generated.")
