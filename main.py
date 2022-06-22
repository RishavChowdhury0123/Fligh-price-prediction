from matplotlib.pyplot import show
import pandas as pd
import streamlit as st
import numpy as np
import pickle

st. set_page_config(layout="wide")

# load model.pkl file
@st.cache(allow_output_mutation=True, show_spinner=False)
def load_data():
    path= r'C:\Users\DELL\Python files\Flight Price Prediction\pipe.pkl'
    with open(path, 'rb') as ref:
        pipe= pickle.load(ref)

    path= r'C:\Users\DELL\Python files\Flight Price Prediction\df.pkl'
    with open(path, 'rb') as ref:
        df= pickle.load(ref).drop('price', axis=1)

    return pipe, df

pipe, df= load_data()

with open('./style.css') as css:
    html= '<style>{}</style>'.format(css.read())

st.markdown(html,unsafe_allow_html=True)

flight_stops ={'one': 0, 'zero': 2, 'two_or_more': 1}
fl_class= {'Economy':1, 'Business':0}
cities= ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai']


def predict_price(airline, departure_time, flight_class , days_left, route):
    X= df.copy()
    X= X.append({'airline':airline,'departure_time':departure_time,
               'class':flight_class,'days_left': days_left, 'route':route}, ignore_index=True)
    predictors= pd.get_dummies(data= X, columns= ['class','route','departure_time','airline'], drop_first=True).iloc[-1:,:].values
    return (pipe.predict(predictors.reshape(1,-1))[0])

st.title('Flight Price Predictor for Metropolitan cities')

with st.container():
    cols= st.columns(4)
    box1= cols[0].selectbox('From', cities, key= 'box1')
    box2= cols[1].selectbox('To', [i for i in reversed(cities)], key= 'box2')
    box3= cols[2].selectbox('Choose Airline',df.airline.unique(), key= 'box3')
    box4= cols[3].radio('Choose Class', df['class'].unique(), key= 'box4')
    

with st.container():
    cols= st.columns(3)
    box5= cols[0].slider('Days before',value=30, min_value=1, max_value=50, key= 'box5')
    box6= cols[1].selectbox('Departure Time', df.departure_time.unique(), key= 'box6')
    cols[2].empty()


btn= st.button('Predict price', key='button')

if st.session_state['box1']== st.session_state['box2']:
        st.warning('Source and Destination cannot be same. Please try again.')

if st.session_state.button:
        predicted= predict_price(route= st.session_state['box1']+'_'+st.session_state['box2'], airline= box3,departure_time=box6, flight_class=box4, days_left=box5)
        st.markdown('Flight price would be approximately Rs.%0.2f'%predicted)
