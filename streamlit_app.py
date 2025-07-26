
# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤Customize Your Smoothie!🥤")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
ingredients_list = st.multiselect('Choose up to 5 ingridients', max_selections=5, options = my_dataframe)

if ingredients_list:
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string+=fruit + ' '
    st.write(ingredients_string)

     
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(str(smoothiefroot_response).json())
# sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
