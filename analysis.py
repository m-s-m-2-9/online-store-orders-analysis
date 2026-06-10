import os

src_file = 'online_orders.csv'
out_report = 'business_report.txt'

if not os.path.exists(src_file):
    with open(out_report, 'w') as f:
        f.write("Error: 'online_orders.csv' not found in the repository.")
    exit()

print("Analyzing Q-Commerce order metrics...")
n_orders = 0
rev_total = 0
plat_stats = {}
promo_stats = {"Discounted": 0, "Full Price": 0}

with open(src_file, 'r', encoding='utf-8') as f:
    cols = [h.strip().lower() for h in f.readline().split(',')]
    
    idx_plat = next((i for i, h in enumerate(cols) if h in ['company', 'platform', 'app', 'store']), None)
    idx_val = next((i for i, h in enumerate(cols) if h in ['order_value', 'amount', 'total_price', 'price', 'order_amount', 'sales']), None)
    idx_disc = next((i for i, h in enumerate(cols) if h in ['discount_applied', 'discount', 'promo', 'coupon']), None)

    for line in f:
        if not line.strip():
            continue
        row = line.strip().split(',')
        
        try:
            val = float(row[idx_val]) if idx_val is not None else 0.0
            plat = row[idx_plat].strip() if idx_plat is not None else "Unknown App"
            
            n_orders += 1
            rev_total += val
            plat_stats[plat] = plat_stats.get(plat, 0) + val
            
            if idx_disc is not None:
                is_promo = row[idx_disc].strip().lower() in ['yes', '1', 'true', 'applied']
                status = "Discounted" if is_promo else "Full Price"
                promo_stats[status] += val
        except (ValueError, IndexError):
            continue

with open(out_report, 'w') as f:
    f.write("==================================================\n")
    f.write("      EXECUTIVE ONLINE STORE ORDERS REPORT       \n")
    f.write("==================================================\n\n")
    f.write(f"Total Completed Orders Analyzed: {n_orders}\n")
    f.write(f"Total Gross Revenue: INR {rev_total:,.2f}\n")
    
    if n_orders > 0:
        f.write(f"Average Order Value (AOV): INR {rev_total / n_orders:,.2f}\n\n")
    
    f.write("--- Revenue Breakdown by Platform ---\n")
    for plat, rev in plat_stats.items():
        f.write(f"* {plat}: INR {rev:,.2f}\n")
        
    f.write("\n--- Marketing Performance ---\n")
    for status, rev in promo_stats.items():
        f.write(f"* {status} Revenue: INR {rev:,.2f}\n")

print("Analysis complete. business_report.txt generated.")
