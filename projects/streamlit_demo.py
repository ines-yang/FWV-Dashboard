import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize the session state attribute
if 'df_shown' not in st.session_state:
    st.session_state.df_shown = False

#Importing data 
raceM = pd.read_csv("raceM.csv")
raceMP = pd.read_csv("raceMP.csv")
raceF = pd.read_csv("raceF.csv")
raceFP = pd.read_csv("raceFP.csv")
race = pd.read_csv("Race.csv")
IPV = pd.read_csv('Sexual_Violence_by_Sex.csv')
age = pd.read_csv('Age.csv')

# Title of the app with logo
st.title('Lifetime Cost of IPV to a Firm')

# Inputs for the number of male and female employees
with st.form(key='columns_in_form'):
    c1, c2 = st.columns(2)
    with c1:
        men = st.number_input('Enter number of male employees', min_value=0, value=0, step=1, key='men')
        MULTm = st.number_input('Enter percentage of male employees with multiple ethnicities', min_value=0.0, value=51.5, step=1.0, key='MULTm')
        AIANm = st.number_input('Enter percentage of American Indian / Alaskan Native male employees', min_value=0.0, value=51.1, step=1.0, key='AI/ANm')
        BLKm = st.number_input('Enter percentage of black male employees', min_value=0.0, value=57.6, step=1.0, key='BLKm')
        WHTm = st.number_input('Enter percentage of white male employees', min_value=0.0, value=44.0, step=1.0, key='WHTm')
        HISm = st.number_input('Enter percentage of hispanic male employees', min_value=0.0, value=40.3, step=1.0, key='HISm')
        APIm = st.number_input('Enter percentage of asian male employees', min_value=0.0, value=24.8, step=1.0, key='APIm')

    with c2:
        women = st.number_input('Enter number of female employees', min_value=0, value=0, step=1, key='women')
        MULTf = st.number_input('Enter percentage of female employees with multiple ethnicities', min_value=0.0, value=63.8, step=1.0, key='MULTf')
        AIANf = st.number_input('Enter percentage of American Indian / Alaskan Native female employees', min_value=0.0, value=57.7, step=1.0, key='AI/ANf')
        BLKf = st.number_input('Enter percentage of black female employees', min_value=0.0, value=53.6, step=1.0, key='BLKf')
        WHTf = st.number_input('Enter percentage of white female employees', min_value=0.0, value=48.4, step=1.0, key='WHTf')
        HISf = st.number_input('Enter percentage of hispanic female employees', min_value=0.0, value=42.1, step=1.0, key='HISf')
        APIf = st.number_input('Enter percentage of asian female employees', min_value=0.0, value=27.2, step=1.0, key='APIf')

    submitButton = st.form_submit_button(label = 'Calculate')


# Menu for selecting the type of graph
graph_type = st.selectbox('Select Graph Type', ('Horizontal Bar', 'Stacked Vertical Bar', 'Area Chart'))

# Create a DataFrame for the table data
data = {
    'Category': ['Medical', 'Lost Productivity', 'Criminal Justice', 'Other', 'Total (By Gender)'],
    'Cost ($): Women': [women * 65165, women * 36065, women * 1376, women * 1161, women * (65165 + 36065 + 1376 + 1161)],
    'Cost ($): Men': [men * 4458, men * 14291, men * 2497, men * 2168, men * (4458 + 14291 + 2497 + 2168)]
}
df = pd.DataFrame(data)

# Add a column for the total cost
df['Total Cost ($)'] = df['Cost ($): Women'] + df['Cost ($): Men']

# Button to calculate cost
if men == 0 and women == 0:
    st.warning('Please enter at least 1 employee!')
else:
    if st.button('Calculate Cost'):
        st.session_state.df_shown = False

        # Compute the lifetime cost
        lifetime_cost = round((28944.58 * 0.442 * men) + (128277.72 * 0.473 * women), 2)
        lifetime_cost_formatted = "{:,.2f}".format(lifetime_cost)
        cost_message = f'The Lifetime Cost of IPV to a firm with {men} men and {women} women employees is: ${lifetime_cost_formatted}'
        st.write(cost_message)

        # Create different types of graphs based on the user's selection
        if graph_type == 'Horizontal Bar':
            fig4 = px.histogram(age, x="Age", y="Percentage IPV Reported",
             color='Sex', barmode='group')
            fig4.update_xaxes(title_text='Age at first IPV')  # Rename x-axis
            fig4.update_layout(height=600)
            st.plotly_chart(fig4, use_container_width=True)
        elif graph_type == 'Stacked Vertical Bar':
            fig = px.histogram(raceFP, x='Race/Ethnicity', y='Lifetime Weighted %', color='Race/Ethnicity', barmode='group')
            fig.update_yaxes(title_text='Race/Ethnicity')  # Rename y-axis
            fig.update_layout(height=600, bargap=0.001)
            st.plotly_chart(fig, use_container_width=True)
        elif graph_type == 'Area Chart':
            fig = px.area(df, x='Category', y=['Cost ($): Women', 'Cost ($): Men'])
            fig.update_yaxes(title_text='Cost ($)')  # Rename y-axis
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)

        st.session_state.df_shown = True

# Display the dataframe along with the graphs
if st.session_state.df_shown:
    st.write(df)