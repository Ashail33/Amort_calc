# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 17:30:46 2021

@author: Ashail Maharaj
"""
#Import libraries
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import datetime as dt
from dateutil.relativedelta import *

#Setting the page title name
st.set_page_config(
    page_title="Homeloan Amortisation Calculator")

st.title("Homeloan Amortisation Calculator")



#create the header 
st.header("**Inputs**")

#create a to place for the input fields 
colAnnualSal, colTax = st.beta_columns(2)

#Creates a subheader for the bond price and an input box assigning the value to the variable bond_price
with colAnnualSal:
    st.subheader("Bond Price")
    bond_price = st.number_input("Enter your bond price: ", min_value=0.0, format='%f')

#Creates a subheader for the Repayment Value and an input box assigning the value to the variable monthly_repayment_value
with colAnnualSal:
    st.subheader("Repayment Value")
    monthly_repayment_value = st.number_input("Enter your monthly repayment value: ", min_value=0.0, format='%f')
    
with colAnnualSal:
    st.subheader("Extra Monthy Payment Amount")
    Extra_cont_payment_value = st.number_input("Enter the extra monthly payment value: ", min_value=0.0, format='%f')
    
with colAnnualSal:
    st.subheader("Start Date")
    start_date=st.date_input("Enter your bond start date")
    
with colAnnualSal:
    st.subheader("Interest Rate")
    interest_rate = st.number_input("Enter the interest rate (% annual)", min_value=0.0, format='%f')/100

#Init lists for the amort calcs
list_amounts = []
list_amounts.append(bond_price)
dates_list= []
dates_list.append(start_date)

#function for amortisation schedule, the value will start at the bond price at time 0 and reduce by the total repayment - interest 
# this will continue until the bond price is 0, each time it will add to the above lists.
# it assumes that interest is accrued and paid monthly and that the additional repayment is fixed.

def amort(bond_price,start_date,interest_rate=7,monthly_repayment_value=bond_price/30,Extra_cont_payment_value=0):
    while bond_price>0:
        
        #Calculates the amount owing on the bond and will append to the list
        bond_price=bond_price*(1+interest_rate/12)-monthly_repayment_value-Extra_cont_payment_value
        list_amounts.append([0 if bond_price < 0 else bond_price][0])
        
        #adds one month to the current date and then appends to the list
        start_date = start_date+ relativedelta(months=+1)#).strftime("%Y-%m-%d")
        dates_list.append(start_date)
        
    # converts the date and remaing bond into one dataframe  
    data=pd.DataFrame({'Amount_remaining':list_amounts,'repayment_date':dates_list},columns=['Amount_remaining','repayment_date'])
    return(data)
 
    
data= amort(bond_price,start_date,interest_rate,monthly_repayment_value,Extra_cont_payment_value)

st.header("**Home Loan Amount Owing **")
fig = px.line(data, x="repayment_date", y="Amount_remaining")

#creates a simple line chart showing the amortisation schedule over time
st.plotly_chart(fig, use_container_width=True)

