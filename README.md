# online-store-orders-analysis


# Quick Commerce (Q-Commerce) Store Performance Analysis

An automated cloud data pipeline built to analyze business metrics and revenue performance across quick commerce platforms (Blinkit, Swiggy Instamart, Zepto, BigBasket).

## 🚀 Core Business Metrics Tracked
* **Average Order Value (AOV)**: Evaluates user purchasing patterns across different ordering instances.
* **Platform Revenue Distribution**: Compares market share and total processing volume between applications.
* **Marketing Promotion Impact**: Identifies gross revenue performance driven by promotional discount campaigns versus native organic full-price transactions.

## 🛠️ Technology Stack
* **Dataset Management**: Truncated massive Kaggle transactional data using Python core dataframes down to 10,000 entries to optimize lightweight storage.
* **Cloud Infrastructure**: Configured **GitHub Actions** (`ubuntu-latest`) to build an on-demand virtual server, execute code processing, and securely bundle reporting outputs via cloud artifact delivery systems upon repository push actions.
