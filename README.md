# Gurgaon Real Estate Analytics

A Streamlit dashboard for Gurgaon property analysis, price prediction, apartment
recommendations, and SHAP-based model explanations.

## Features

- **Price Predictor** — estimate a property price from its details.
- **Analysis App** — explore sectors, prices, listings, and locations.
- **Recommend Apartments** — find nearby and similar properties.
- **Model Insights** — understand the features behind predictions.

The repository includes the trained model and supporting data, so retraining is
not required.

## Run locally

```powershell
git clone https://github.com/omkarhole/real-estate-project.git
cd real-estate-project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run Home.py
```

## Pages

| Page | Purpose |
| --- | --- |
| Home | Project overview and navigation |
| Price Predictor | Estimate a Gurgaon property price |
| Analysis App | Explore market and location insights |
| Recommend Apartments | Search nearby and similar apartments |
| Model Insights | Explain model predictions with SHAP |

**Stack:** Python, Streamlit, Pandas, NumPy, Scikit-learn, XGBoost, Plotly,
Matplotlib, and SHAP.

## Author

**Omkar Hole**

- GitHub: [omkarhole/real-estate-project](https://github.com/omkarhole/real-estate-project)
- LinkedIn: [omkar-hole-c0der](https://www.linkedin.com/in/omkar-hole-c0der)
