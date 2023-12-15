import pandas as pd
import plotly.express as px
import streamlit as st

# Function for the first page
def page_one():
    # Initialize the session state attributes
    if 'show_details' not in st.session_state:
        st.session_state.show_details = False

    # Create two columns for the logos
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image('https://github.com/bellaachang/FWV-Dashboard/blob/main/futureswithoutviolence-logo.png?raw=true', width=300)
    with col2:
        st.image('https://github.com/bellaachang/FWV-Dashboard/blob/main/dss%20logo%20copy.png?raw=true', width=100)

    # Title of the app with logo
    st.title('Lifetime Cost of IPV to a Firm')

    # Inputs for the number of male and female employees
    men = st.number_input('Enter number of male employees', min_value=0, value=0, step=1, key='men')
    women = st.number_input('Enter number of female employees', min_value=0, value=0, step=1, key='women')

    # Menu for selecting the type of graph
    graph_type = st.selectbox('Select Graph Type', ('Horizontal Bar', 'Stacked Vertical Bar', 'Area Chart'))

    # Create a DataFrame for the table data
    data = {
        'Category': ['Medical', 'Lost Productivity', 'Criminal Justice', 'Other', 'Total Cost ($)'],
        'Cost ($): Women': [women * 65165, women * 36065, women * 1376, women * 1161, women * (65165 + 36065 + 1376 + 1161)],
        'Cost ($): Men': [men * 4458, men * 14291, men * 2497, men * 2168, men * (4458 + 14291 + 2497 + 2168)]
    }
    df = pd.DataFrame(data)

    # Add a column for the total cost
    df['Total Cost ($)'] = df['Cost ($): Women'] + df['Cost ($): Men']

    # Check if there is valid input to perform calculations
    if men > 0 or women > 0:
        # Compute the lifetime cost
        lifetime_cost = round((28944.58 * 0.442 * men) + (128277.72 * 0.473 * women), 2)
        lifetime_cost_formatted = "{:,.2f}".format(lifetime_cost)
        cost_message = f"The estimated Lifetime Cost of IPV to a firm with {men} men and {women} women employees is: **${lifetime_cost_formatted}**"
        st.markdown(cost_message)

        # Reshape DataFrame for Plotly
        df_long = df.melt(id_vars='Category', value_vars=['Cost ($): Women', 'Cost ($): Men'], var_name='Gender', value_name='Value')

        # Create different types of graphs based on the user's selection
        if graph_type == 'Horizontal Bar':
            fig = px.bar(df_long, x='Value', y='Category', color='Gender', orientation='h', barmode='group',
                        color_discrete_map={'Cost ($): Women': '#9fcb3b', 'Cost ($): Men': '#f9c02d'})
            st.plotly_chart(fig, use_container_width=True)
        elif graph_type == 'Stacked Vertical Bar':
            fig = px.bar(df_long, x='Category', y='Value', color='Gender', barmode='stack',
                        color_discrete_map={'Cost ($): Women': '#9fcb3b', 'Cost ($): Men': '#f9c02d'})
            st.plotly_chart(fig, use_container_width=True)
        elif graph_type == 'Area Chart':
            fig = px.area(df_long, x='Category', y='Value', color='Gender',
                        color_discrete_map={'Cost ($): Women': '#9fcb3b', 'Cost ($): Men': '#f9c02d'})
            st.plotly_chart(fig, use_container_width=True)

        # Display DataFrame table after graphs
        st.write(df)

    # Button to show/hide details, placed after the DataFrame
    if st.button('Show Details'):
        st.session_state.show_details = not st.session_state.show_details

    # Display the details if the "Show Details" button has been clicked
    if st.session_state.show_details:
        st.markdown("""
        <p><strong>What is IPV?</strong> IPV, or Intimate Partner Violence, refers refers to any physical or sexual violence, stalking, and/or psychological aggression by a current or former dating partner or spouse. This form of violence can happen in all types of relationships, including among heterosexual and same-sex relationships, and can occur at multiple points throughout the lifespan. Intimate partner violence may also vary in severity or duration and does not require sexual intimacy.</p>
        <p><strong>"Medical"</strong> costs include all fees related to hospitalization and any related costs from mental or physical health conditions, and consultations with medical specialists.</p>
        <p><strong>"Lost Productivity"</strong> includes estimated costs related to victim's lost productivity caused by fatality, mental health (post-traumatic stress disorder and depression), substance abuse (alcohol, illicit drugs, smoking), and physical health conditions (asthma, joint conditions, sexually transmitted infections). Also includes cost of perpretator's lost productivity.</p>
        <p><strong>"Criminal Justice"</strong> costs accounted for in the criminal justice system include those incurred by both the perpetrator and the victim.</p>
        <p><strong>"Other"</strong> costs include damaged/lost property and other miscellaneous costs associated with injuries.</p>
        """, unsafe_allow_html=True)

# Function for the second page
def page_two():
    # Read the data
    men_tbl = pd.read_csv("https://github.com/bellaachang/FWV-Dashboard/blob/main/NISV_plotly/NISV%20Sexual%20identity%20-%20Cleaned_men%20(1).csv?raw=true").dropna()
    women_tbl = pd.read_csv("https://github.com/bellaachang/FWV-Dashboard/blob/main/NISV_plotly/cleaned_women.csv?raw=true")


    # Convert column to integer
    men_tbl['Estimated Number of Victims (Nearest Thousandth'] = men_tbl['Estimated Number of Victims (Nearest Thousandth'].str.replace(',', '').astype(int)
    women_tbl['Estimated Number of Victims (Nearest Thousandth)'] = women_tbl['Estimated Number of Victims (Nearest Thousandth)'].str.replace(',', '').astype(int)


    # Group by Sexual identity and sum the Estimated Number of Victims
    summed_men_tbl = men_tbl.groupby("Sexual identity").sum()['Estimated Number of Victims (Nearest Thousandth']
    summed_women_tbl = women_tbl.groupby("Sexual Identity").sum()['Estimated Number of Victims (Nearest Thousandth)']

    # Normalize the data
    men_tbl.loc[men_tbl['Sexual identity'] == 'Gay', 'Estimated Number of Victims (Nearest Thousandth'] = men_tbl.loc[men_tbl['Sexual identity'] == 'Gay', 'Estimated Number of Victims (Nearest Thousandth'] / summed_men_tbl.loc['Gay']
    men_tbl.loc[men_tbl['Sexual identity'] == 'Bisexual', 'Estimated Number of Victims (Nearest Thousandth'] = men_tbl.loc[men_tbl['Sexual identity'] == 'Bisexual', 'Estimated Number of Victims (Nearest Thousandth'] / summed_men_tbl.loc['Bisexual']
    men_tbl.loc[men_tbl['Sexual identity'] == 'Heterosexual', 'Estimated Number of Victims (Nearest Thousandth'] = men_tbl.loc[men_tbl['Sexual identity'] == 'Heterosexual', 'Estimated Number of Victims (Nearest Thousandth'] / summed_men_tbl.loc['Heterosexual']

    women_tbl.loc[women_tbl['Sexual Identity'] == 'Lesbian', 'Estimated Number of Victims (Nearest Thousandth)'] = women_tbl.loc[women_tbl['Sexual Identity'] == 'Lesbian', 'Estimated Number of Victims (Nearest Thousandth)'] / summed_women_tbl.loc['Lesbian']
    women_tbl.loc[women_tbl['Sexual Identity'] == 'Bisexual', 'Estimated Number of Victims (Nearest Thousandth)'] = women_tbl.loc[women_tbl['Sexual Identity'] == 'Bisexual', 'Estimated Number of Victims (Nearest Thousandth)'] / summed_women_tbl.loc['Bisexual']
    women_tbl.loc[women_tbl['Sexual Identity'] == 'Heterosexual', 'Estimated Number of Victims (Nearest Thousandth)'] = women_tbl.loc[women_tbl['Sexual Identity'] == 'Heterosexual', 'Estimated Number of Victims (Nearest Thousandth)'] / summed_women_tbl.loc['Heterosexual']

    # Create figures
    menfig1 = px.histogram(men_tbl, x="Act", y="Estimated Number of Victims (Nearest Thousandth", color="Sexual identity", barmode="group")
    # fig2 = px.pie(tbl, names="Sexual identity", values="Estimated Number of Victims (Nearest Thousandth")
    # fig3 = px.bar(tbl, x="Sexual identity", y="Estimated Number of Victims (Nearest Thousandth",
                # color="Act", hover_data=["Estimated Number of Victims (Nearest Thousandth"],
                # barmode = 'group')
    menfig1.update_layout( xaxis_title='Men: Act')

    womenfig1 = px.histogram(women_tbl, x = "Act", y = "Estimated Number of Victims (Nearest Thousandth)", color = "Sexual Identity", barmode = "group")
    womenfig1.update_layout( xaxis_title='Women: Act')


    # Streamlit app
    st.title("How Men of Varying Sexual Identities Experience IPV/Rape")

    # Display figures
    st.plotly_chart(menfig1)
    st.plotly_chart(womenfig1)

# Sidebar navigation for different pages
page = st.sidebar.selectbox('Go to', ('Cost of IPV to a Firm', 'IPV/Rape by Sexual Identities'))

# Display selected page
if page == 'Cost of IPV to a Firm':
    page_one()
elif page == 'IPV/Rape by Sexual Identities':
    page_two()