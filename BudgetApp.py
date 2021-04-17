# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 17:30:46 2021

@author: Ashail Maharaj
"""

import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import datetime as dt
from dateutil.relativedelta import *

st.set_page_config(
    page_title="Financial Planning Calculator")

st.title("Homeloan Amortisation Calculator")

#Create an income section 

#create the header 
st.header("**Inputs**")

#create 2 columns to place the input fields for salary and tax rate
colAnnualSal, colTax = st.beta_columns(2)


with colAnnualSal:
    st.subheader("Bond Price")
    bond_price = st.number_input("Enter your bond price: ", min_value=0.0, format='%f')
    
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

list_amounts = []
list_amounts.append(bond_price)
dates_list= []
#dates_list.append(dt.datetime.strptime(start_date, "%Y/%m/%d"))
dates_list.append(start_date)

def amort(bond_price,start_date,interest_rate=7,monthly_repayment_value=bond_price/30,Extra_cont_payment_value=0):
    while bond_price>0:
        bond_price=bond_price*(1+interest_rate/12)-monthly_repayment_value-Extra_cont_payment_value
        list_amounts.append([0 if bond_price < 0 else bond_price][0])
        start_date = start_date+ relativedelta(months=+1)#).strftime("%Y-%m-%d")
        dates_list.append(start_date)
    data=pd.DataFrame({'Amount_remaining':list_amounts,'repayment_date':dates_list},columns=['Amount_remaining','repayment_date'])
    return(data)
 
    
data= amort(bond_price,start_date,interest_rate,monthly_repayment_value,Extra_cont_payment_value)

st.header("**Home Loan Amount Owing **")
fig = px.line(data, x="repayment_date", y="Amount_remaining")


st.plotly_chart(fig, use_container_width=True)









