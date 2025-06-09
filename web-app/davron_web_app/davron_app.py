import streamlit as st
import pickle
import datetime
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor

model_file_path = 'web-app/davron_web_app/davron_model'
county_encoder_file_path = 'web-app/davron_web_app/davron_county_encoder'

with open(county_encoder_file_path, 'rb') as read_file:
    county_encoder = pickle.load(read_file)

with open(model_file_path, 'rb') as read_file:
    model = pickle.load(read_file)

# Function to get house level
level_zero = 0
level_two = 0
level_three = 0

# Season posted
season_spring = 0
season_summer = 0
season_winter = 0

# Home type and Level
# Initialize session state for home types
if 'single_family' not in st.session_state:
    st.session_state.single_family = 1
if 'townhouse' not in st.session_state:
    st.session_state.townhouse = 0
if 'house_level_label' not in st.session_state:
    st.session_state.house_level_label = 'How many levels does the house have?'
if 'is_location_level' not in st.session_state:
    st.session_state.is_location_level = 0
st.session_state.prediction_price = None


def yes_or_no_view(label):
    value = st.radio(label, ['Yes', 'No'], index=1)

    return 1 if value == 'Yes' else 0


def get_area_group():
    area = st.number_input('Enter the area of the house in sqft: ', min_value=0, max_value=None, value=300, step=10)
    if area < 1001:
        return 1
    elif area < 2001:
        return 2
    elif area < 3001:
        return 3
    else:
        return 4


def get_age_group():
    current_year = datetime.datetime.now().year
    year_built = st.number_input('Enter the year when the house was built: ', min_value=0, max_value=current_year,
                                 value=current_year, step=1)
    age = current_year - year_built
    if age < 6:
        return 1
    elif age < 16:
        return 2
    elif age < 31:
        return 3
    elif age < 51:
        return 4
    else:
        return 5


# Function to update the label based on home type
def change_house_level_label():
    if st.session_state.single_family == 0 and st.session_state.townhouse == 0:
        st.session_state.house_level_label = 'Which level is the house located in?'
        st.session_state.is_location_level = 1
    else:
        st.session_state.house_level_label = 'How many levels does the house have?'
        st.session_state.is_location_level = 0


# Function to get home type
def get_home_type():
    home_type = st.radio('What\'s the home type?', ['Single Family', 'Condo', 'Townhouse'], index=0)

    if home_type == 'Single Family':
        st.session_state.single_family = 1
        st.session_state.townhouse = 0
    elif home_type == 'Condo':
        st.session_state.single_family = 0
        st.session_state.townhouse = 0
    elif home_type == 'Townhouse':
        st.session_state.single_family = 0
        st.session_state.townhouse = 1

    change_house_level_label()


def get_house_level():
    level = st.radio(st.session_state.house_level_label, ['Zero', 'One', 'Two', 'Three or more'], index=1)
    if level == 'Zero':
        return 1, 0, 0
    elif level == 'One':
        return 0, 0, 0
    elif level == 'Two':
        return 0, 1, 0
    elif level == 'Three or more':
        return 0, 0, 1


def get_season_posted():
    current_month = datetime.datetime.now().month
    season_index = 0
    if current_month in [12, 1, 2]:
        season_index = 0
    elif current_month in [3, 4, 5]:
        season_index = 1
    elif current_month in [6, 7, 8]:
        season_index = 2
    elif current_month in [9, 10, 11]:
        season_index = 3
    season_posted = st.radio('In which season are you going to put the house up for sale?', ['Winter', 'Spring', 'Summer', 'Fall'],
                             index=season_index)
    if season_posted == 'Winter':
        return 1, 0, 0
    elif season_posted == 'Spring':
        return 0, 1, 0
    elif season_posted == 'Summer':
        return 0, 0, 1
    else:
        return 0, 0, 0




tab1, tab2 = st.tabs(["Main", "Credits"])

with st.sidebar:
    st.logo("web-app/davron_web_app/GitHub 2.png", link='https://github.com/davron2004-tech/SDS-CP006-california-housing-prediction.git')
    st.header('Specify the house details', divider=True)

    with st.container(border=True):
        # Age
        age_group = get_age_group()
        # IsNewConstruction
        is_new_construction = yes_or_no_view('Is the house new?')

    with st.container(border=True):
        # Area
        area_group = get_area_group()
        # Home type
        get_home_type()
        # Display the home type and house level widgets
        level_zero, level_two, level_three = get_house_level()
        # Multi/split
        multi_split = yes_or_no_view('Is the type of the house multi/split?')

    with st.container(border=True):
        # Bathroom
        bathrooms = st.number_input('Bathrooms', min_value=0, max_value=None, value=1, step=1,
                                    placeholder='Number of Bathrooms')
        # Bedroom
        bedrooms = st.number_input('Bedrooms', min_value=0, max_value=None, value=1, step=1,
                                   placeholder='Number of Bedrooms')

    with st.container(border=True):
        # Garage Spaces
        garage_spaces = st.number_input('How many garage spaces are there in the house?', min_value=0,
                                        max_value=None,
                                        value=1, step=1, placeholder='Number of garage spaces')
        # Parking
        is_parking = yes_or_no_view('Is there a parking in the house?')

    with st.container(border=True):
        # County
        county = st.selectbox(label='County:',
                              options=['Contra Costa County', 'Los Angeles County', 'Santa Clara County',
                                       'Monterey County', 'San Diego County', 'Stanislaus County',
                                       'Kern County', 'Sacramento County', 'San Mateo County',
                                       'Shasta County', 'El Dorado County', 'Placer County',
                                       'Tehama County', 'Tulare County', 'Yolo County',
                                       'Santa Barbara County', 'San Bernardino County', 'Yuba County',
                                       'Orange County', 'Sonoma County', 'Humboldt County',
                                       'San Francisco County', 'Alameda County', 'Riverside County',
                                       'Santa Cruz County', 'Fresno County', 'Marin County',
                                       'Imperial County', 'Ventura County', 'Amador County',
                                       'Mendocino County', 'Sierra County', 'Calaveras County',
                                       'San Joaquin County', 'Butte County', 'Madera County',
                                       'Tuolumne County', 'Lake County', 'Nevada County',
                                       'San Luis Obispo County', 'Mariposa County', 'Kings County',
                                       'San Benito County', 'Sutter County', 'Merced County',
                                       'Napa County', 'Solano County', 'Trinity County', 'Lassen County',
                                       'Modoc County', 'Siskiyou County', 'Plumas County', 'Glenn County',
                                       'Alpine County', 'Del Norte County', 'Mono County', 'Inyo County',
                                       'Colusa County'],
                              index=0)
        county_int = int(county_encoder.transform([county])[0])
        # Zipcode
        zipcode = st.number_input('Zipcode', min_value=90001, max_value=96161, value=95000, step=1,
                                  placeholder='90001-96161')

    with st.container(border=True):
        # Pool
        pool = yes_or_no_view('Is there a pool in the house?')
        # Spa
        spa = yes_or_no_view('Is there a spa in the house?')
        # hasPetsAllowed
        has_pets_allowed = yes_or_no_view('Are the pets allowed in the house?')
    with st.container(border=True):
        season_winter, season_spring, season_summer = get_season_posted()


with tab1:
    st.title(':house: California Housing Price Prediction')

    st.image("web-app/davron_web_app/Thumbnail.png", width=400)
    st.divider()
    @st.dialog('🏡 The predicted price of the house is: ')
    def show_price(price):
        st.header('💰 $ {:.2f}'.format(price))

    if st.button(label='Predict Price',type='primary'):
        user_input = [[
            zipcode, bathrooms, bedrooms, is_parking, garage_spaces, pool, spa, is_new_construction,
            has_pets_allowed, county_int, multi_split,
            st.session_state.is_location_level, st.session_state.single_family, st.session_state.townhouse,
            season_spring, season_summer, season_winter,
            level_three, level_two, level_zero,
            age_group, area_group
        ]]
        input_columns = ['zipcode', 'bathrooms', 'bedrooms', 'parking', 'garageSpaces',
       'pool', 'spa', 'isNewConstruction', 'hasPetsAllowed', 'county',
       'multi/split', 'is_location_level', 'homeType_SINGLE_FAMILY',
       'homeType_TOWNHOUSE', 'season_posted_spring', 'season_posted_summer',
       'season_posted_winter', 'level_three+', 'level_two', 'level_zero',
       'age_group', 'area_group']
        input_df = pd.DataFrame(user_input,columns=input_columns)
        st.session_state.prediction_price = model.predict(input_df)
        show_price(st.session_state.prediction_price[0])
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
                This is the #6 Collaborative Project of the [Super Data Science](https://www.superdatascience.com) community.
            """)
    with col2:
        st.image('web-app/davron_web_app/SDS logo 2.jpg', width=100)
    st.divider()
    st.subheader('Project leader:')
    st.write('🇺🇸 [Syed-Imtiaz Mir](https://www.linkedin.com/in/syed-imtiaz-mir/)')
    st.divider()
    st.subheader('Project mentor:')
    st.markdown('🇦🇪 [Shaheer Airaj Ahmed](https://www.linkedin.com/in/shaheerairaj/)')
    st.divider()
    st.subheader('Project members:')
    st.markdown('🇯🇴 [Mohammad M Zakarneh](https://www.linkedin.com/in/mohamed-zakarneh/)')
    st.markdown('🇺🇿 [Davron Abdukhakimov](https://www.linkedin.com/in/davron-abdukhakimov-90aab4264/)')


