# import streamlit as st
# import pickle
# import pandas as pd
# import numpy as np

# st.set_page_config(page_title="Recommend Appartments")

# location_df = pickle.load(open('datasets/location_distance.pkl','rb'))

# cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl','rb'))
# cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl','rb'))
# cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl','rb'))


# def recommend_properties_with_scores(property_name, top_n=5):
#     cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
#     # cosine_sim_matrix = cosine_sim3

#     # Get the similarity scores for the property using its name as the index
#     sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

#     # Sort properties based on the similarity scores
#     sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

#     # Get the indices and scores of the top_n most similar properties
#     top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
#     top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

#     # Retrieve the names of the top properties using the indices
#     top_properties = location_df.index[top_indices].tolist()

#     # Create a dataframe with the results
#     recommendations_df = pd.DataFrame({
#         'PropertyName': top_properties,
#         'SimilarityScore': top_scores
#     })

#     return recommendations_df


# # Test the recommender function using a property name
# recommend_properties_with_scores('DLF The Camellias')


# st.title('Select Location and Radius')

# selected_location = st.selectbox('Location',sorted(location_df.columns.to_list()))

# radius = st.number_input('Radius in Kms')

# if st.button('Search'):
#     result_ser = location_df[location_df[selected_location] < radius*1000][selected_location].sort_values()

#     for key, value in result_ser.items():
#         st.text(str(key) + " " + str(round(value/1000)) + ' kms')

# st.title('Recommend Appartments')
# selected_appartment = st.selectbox('Select an appartment',sorted(location_df.index.to_list()))

# if st.button('Recommend'):
#     recommendation_df = recommend_properties_with_scores(selected_appartment)

#     st.dataframe(recommendation_df)

import pickle

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Recommend Apartments", page_icon="🏠", layout="wide")
st.title("🏠 Apartment Recommendation System")


@st.cache_resource
def load_data():
    with open("datasets/location_distance.pkl", "rb") as f:
        location_df = pickle.load(f)

    with open("datasets/cosine_sim1.pkl", "rb") as f:
        cosine_sim1 = pickle.load(f)

    with open("datasets/cosine_sim2.pkl", "rb") as f:
        cosine_sim2 = pickle.load(f)

    with open("datasets/cosine_sim3.pkl", "rb") as f:
        cosine_sim3 = pickle.load(f)

    return location_df, cosine_sim1, cosine_sim2, cosine_sim3


location_df, cosine_sim1, cosine_sim2, cosine_sim3 = load_data()
cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1.0 * cosine_sim3


def recommend_properties(property_name, top_n=5):
    property_index = location_df.index.get_loc(property_name)
    sim_scores = sorted(
        enumerate(cosine_sim_matrix[property_index]),
        key=lambda x: x[1],
        reverse=True,
    )[1 : top_n + 1]

    return pd.DataFrame(
        {
            "Apartment": location_df.index[[idx for idx, _ in sim_scores]],
            "Similarity Score": [score for _, score in sim_scores],
        }
    ).round({"Similarity Score": 3})


st.header("📍 Find Apartments by Location")

col1, col2 = st.columns(2)

with col1:
    selected_location = st.selectbox("Select Location", sorted(location_df.columns.tolist()))

with col2:
    radius = st.number_input("Radius (in km)", min_value=0.1, max_value=100.0, value=5.0, step=0.5)

if st.button("🔍 Search Apartments", use_container_width=True):
    distances = (location_df[selected_location].abs() / 1000).sort_values()
    result = distances[distances <= radius]

    if result.empty:
        st.warning(f"No apartments found within {radius:.1f} km.")
    else:
        st.success(f"{len(result)} apartments found within {radius:.1f} km.")
        st.dataframe(
            pd.DataFrame({
                "Apartment": result.index,
                "Distance (km)": result.values.round(2),
            }),
            use_container_width=True,
            hide_index=True,
        )


st.header("🤖 Recommend Similar Apartments")
selected_apartment = st.selectbox("Select an Apartment", sorted(location_df.index.tolist()))
top_n = st.slider("Number of Recommendations", min_value=1, max_value=20, value=5)

if st.button("✨ Recommend Apartments", use_container_width=True):
    recommendation_df = recommend_properties(selected_apartment, top_n)
    st.subheader(f"Recommended Apartments for {selected_apartment}")
    st.dataframe(recommendation_df, use_container_width=True, hide_index=True)
