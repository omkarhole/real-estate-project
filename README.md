# Gurgaon Real Estate Analytics

A Streamlit dashboard for exploring Gurgaon’s real-estate market through
interactive analysis, machine-learning price prediction, and apartment
recommendations.

## What this project offers

- **Price prediction** — estimate a property’s expected price from its location,
  area, rooms, furnishing, amenities, and other characteristics.
- **Market analysis** — explore listing volume, sector-level prices, property mix,
  location trends, and visual insights.
- **Apartment recommendations** — search for apartments within a selected radius
  and discover similar properties using similarity-based recommendations.

## Dataset

The project uses a Gurgaon real-estate dataset covering **100+ sectors**. It
includes information such as:

- Property type and location
- BHK and bathroom count
- Built-up area
- Furnishing and floor details
- Balcony, servant room, and store room availability
- Luxury category, pricing, and other property characteristics

The saved model and supporting files are included in the repository so the app
can be run locally without retraining the pipeline.

## Tech stack

- Python
- Streamlit
- Pandas and NumPy
- Scikit-learn
- XGBoost
- Plotly
- Matplotlib and WordCloud

## Run locally

### 1. Clone the repository

```powershell
git clone https://github.com/omkarhole/real-estate-project.git
cd real-estate-project
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start the application

```powershell
streamlit run Home.py
```

The application opens in your browser at the local Streamlit address shown in
the terminal.

## Application pages

| Page | Purpose |
| --- | --- |
| Home | Project overview and navigation |
| Price Predictor | Estimate a Gurgaon property price |
| Analysis App | Explore market and location insights |
| Recommend Apartments | Search nearby and similar apartments |

## Project structure

```text
.
├── Home.py
├── app_style.py
├── pages/
│   ├── 1_Price Predictor.py
│   ├── 2_Analysis App.py
│   └── 3_Recommend Appartments.py
├── datasets/
├── df.pkl
├── pipeline.pkl
└── requirements.txt
```

## Author

**Omkar Hole**

- GitHub: [omkarhole/real-estate-project](https://github.com/omkarhole/real-estate-project)
- LinkedIn: [omkar-hole-c0der](https://www.linkedin.com/in/omkar-hole-c0der)
