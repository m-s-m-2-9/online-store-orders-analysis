# Quick Commerce Performance Analytics Suite

An automated business intelligence framework and cloud data pipeline built to evaluate operational revenue metrics and channel distribution performance across hyper-local delivery networks including Blinkit, Swiggy Instamart, Zepto, and BigBasket.

## Interactive Analytics Dashboard
The data processing architecture has been scaled into a live, interactive web application. Stakeholders can upload batch transaction logs or manually input discrete ledger entries to generate dynamic visualizations and statistical evaluations on demand.

* **Live Deployment Workspace:** [online-store-analysis.streamlit.app](https://online-store-analysis.streamlit.app/#automated-dataset-parsing-matrix)

## Core Analytical Capabilities
* **Average Order Value Tracking:** Aggregates and monitors transactional transaction size variances to gauge purchasing frequency and basket value characteristics.
* **Fulfillment Platform Benchmarking:** Evaluates transactional volume trends to break down platform market share and gross revenue processing velocity.
* **Incentive Yield Optimization:** Segregates promotional campaign conversions from native, full-price organic orders to evaluate the financial efficiency of marketing margin structures.

## System Architecture and Engineering
* **Data Volume Standardization:** Implemented an ingestion module to parse raw multi-gigabyte transactional records down to a structural 10,000-entry volume, optimizing local file input constraints.
* **Continuous Integration Data Pipeline:** Configured a GitHub Actions virtualization runner (`ubuntu-latest`) to build an on-demand container runtime environment, execute data pipeline checks, and compile structured operational summary artifacts upon every main branch validation.
* **Interactive Visualization Engine:** Structured an isolated workspace layout using a multi-tab interface built on Streamlit and unified dynamic rendering layers to allow deep metric drill-downs without interface reload delays.

## Technical Specifications

### Project Directory Structure
```text
├── .github/
│   └── workflows/
│       └── run_analysis.yml     # Cloud virtualization execution runner
├── analysis.py                  # Core backend dataset validation pipeline
├── app.py                       # Main Streamlit web application engine
├── requirements.txt             # Managed software library dependencies
├── online_orders.csv            # Structured 10,000-entry operational dataset
└── .gitignore                   # Version control system file configuration
```

### Software Dependencies
The system utilizes a lightweight, open-source Python stack configured to deploy seamlessly inside virtualization runtimes:
* **Streamlit**: Web interface and interface frame layout abstraction.
* **Pandas**: Structural programmatic matrix array manipulation.
* **Plotly**: Client-side interactive graphical calculation compilation.
* **Numpy**: Baseline algebraic calculations for future projection models.

## Operational Deployment Protocol

### Local Workstation Setup
To run the server instance locally on a development machine:
1. Clone the version-controlled directory tree.
2. Initialize a secure sandbox runtime container environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the specific managed dependencies via pip:
   ```bash
   pip install -r requirements.txt
   ```
4. Initiate the runtime compilation command to map the browser stream link:
   ```bash
   streamlit run app.py
   ```
