# import streamlit as st
# import pickle
# import pandas as pd
# import numpy as np

# st.set_page_config(page_title="Price Predictor", page_icon=":money_with_wings:", layout="wide")
# st.title('price predictor')



# with open('df.pkl','rb') as f:
#     df=pickle.load(f)

# with open('pipeline.pkl','rb') as f:
#     pipeline=pickle.load(f)


# st.header('enter your details ')

# # property type 
# property_type=st.selectbox('Property Type',['flat','house'])

# sector=st.selectbox('Sector',sorted(df['sector'].unique().tolist()))

# bedrooms=float(st.selectbox('Number of BedRooms',sorted(df['bedRoom'].unique().tolist())))

# bathrooms=float(st.selectbox('Number of BathRooms',sorted(df['bathroom'].unique().tolist())))

# balcony=st.selectbox('Number of Balconies',sorted(df['balcony'].unique().tolist()))

# property_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))

# built_up_area = float(st.number_input('Built Up Area'))

# servant_room = float(st.selectbox('Servant Room',[0.0, 1.0]))

# store_room = float(st.selectbox('Store Room',[0.0, 1.0]))

# furnishing_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))

# luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))

# floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))


# if st.button("Predict Price"):
#     # form dataframe
    
#     data = [[property_type, sector, bedrooms, bathrooms, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    
#     columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
#             'agePossession', 'built_up_area', 'servant room', 'store room',
#             'furnishing_type', 'luxury_category', 'floor_category']
    
#     one_df=pd.DataFrame(data,columns=columns)
#     # st.dataframe(one_df)

#     # predict 
#     base_price=np.expm1(pipeline.predict(one_df))[0]
#     mae = 0.1084
#     low=base_price-mae
#     high=base_price+mae

#     # display the predicted price
#     st.text(f'The Price of the Property is between: {low:.2f}Cr and {high:.2f}Cr')

import streamlit as st
import pickle
import pandas as pd
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Gurgaon Property Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA + MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    with open("pipeline.pkl", "rb") as f:
        model = pickle.load(f)
    return model


@st.cache_data
def load_data():
    with open("df.pkl", "rb") as f:
        data = pickle.load(f)
    return data


df = load_data()
pipeline = load_model()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🏠 Gurgaon Property Price Predictor")
st.write(
    "Enter the property details below to estimate the expected property price."
)

st.divider()


# --------------------------------------------------
# PROPERTY DETAILS
# --------------------------------------------------

st.subheader("🏢 Property Details")

col1, col2, col3 = st.columns(3)

with col1:

    property_type = st.selectbox(
        "Property Type",
        ["flat", "house"]
    )

    sector = st.selectbox(
        "Sector",
        sorted(df["sector"].unique().tolist())
    )

    bedrooms = float(
        st.selectbox(
            "Number of Bedrooms",
            sorted(df["bedRoom"].unique().tolist())
        )
    )

with col2:

    bathrooms = float(
        st.selectbox(
            "Number of Bathrooms",
            sorted(df["bathroom"].unique().tolist())
        )
    )

    balcony = st.selectbox(
        "Number of Balconies",
        sorted(df["balcony"].unique().tolist())
    )

    property_age = st.selectbox(
        "Property Age",
        sorted(df["agePossession"].unique().tolist())
    )

with col3:

    built_up_area = float(
        st.number_input(
            "Built-up Area (sq ft)",
            min_value=100.0,
            max_value=20000.0,
            value=1000.0,
            step=50.0
        )
    )

    furnishing_type = st.selectbox(
        "Furnishing Type",
        sorted(df["furnishing_type"].unique().tolist())
    )


st.divider()


# --------------------------------------------------
# ADDITIONAL FEATURES
# --------------------------------------------------

st.subheader("⚙️ Additional Features")

col1, col2, col3, col4 = st.columns(4)

with col1:
    servant_room = float(
        st.selectbox(
            "Servant Room",
            [0.0, 1.0],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )
    )

with col2:
    store_room = float(
        st.selectbox(
            "Store Room",
            [0.0, 1.0],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )
    )

with col3:
    luxury_category = st.selectbox(
        "Luxury Category",
        sorted(df["luxury_category"].unique().tolist())
    )

with col4:
    floor_category = st.selectbox(
        "Floor Category",
        sorted(df["floor_category"].unique().tolist())
    )


st.divider()


# --------------------------------------------------
# PREDICTION BUTTON
# --------------------------------------------------

col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    predict_button = st.button(
        "🔮 Predict Property Price",
        use_container_width=True
    )


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if predict_button:

    # Create dataframe

    data = [[
        property_type,
        sector,
        bedrooms,
        bathrooms,
        balcony,
        property_age,
        built_up_area,
        servant_room,
        store_room,
        furnishing_type,
        luxury_category,
        floor_category
    ]]

    columns = [
        "property_type",
        "sector",
        "bedRoom",
        "bathroom",
        "balcony",
        "agePossession",
        "built_up_area",
        "servant room",
        "store room",
        "furnishing_type",
        "luxury_category",
        "floor_category"
    ]

    one_df = pd.DataFrame(
        data,
        columns=columns
    )

    # Prediction

    prediction = pipeline.predict(one_df)

    base_price = np.expm1(prediction)[0]

    # Model MAE

    mae = 0.1084

    low = max(0, base_price - mae)
    high = base_price + mae


    # --------------------------------------------------
    # RESULT
    # --------------------------------------------------

    st.success("Prediction generated successfully!")

    st.subheader("💰 Estimated Property Price")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Estimated Price",
            f"₹{base_price:.2f} Cr"
        )

    with col2:
        st.metric(
            "Lower Estimate",
            f"₹{low:.2f} Cr"
        )

    with col3:
        st.metric(
            "Upper Estimate",
            f"₹{high:.2f} Cr"
        )


    st.info(
        f"🏠 Estimated price range: **₹{low:.2f} Cr - ₹{high:.2f} Cr**"
    )


    # --------------------------------------------------
    # INPUT SUMMARY
    # --------------------------------------------------

    with st.expander("📋 View Property Details"):

        st.dataframe(
            one_df,
            use_container_width=True,
            hide_index=True
        )