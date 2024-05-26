import streamlit as st
import pandas as pd
import plotly.express as px

# Read the data
men_tbl = pd.read_csv("NISV Sexual identity - Cleaned_men (1).csv").dropna()
women_tbl = pd.read_csv("cleaned_women.csv")


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
# st.plotly_chart(fig2)
# st.plotly_chart(fig3)

