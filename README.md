# Gurgaon Real Estate Analytics App

A Streamlit application for Gurgaon real-estate analysis, apartment recommendations,
and property price prediction using a saved machine-learning pipeline.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Start the application:

   ```powershell
   streamlit run Home.py
   ```

The model and dataset files (`pipeline.pkl` and `df.pkl`) are included in the
repository and are loaded by the Streamlit pages at runtime.
