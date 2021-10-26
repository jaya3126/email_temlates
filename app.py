#!/usr/bin/env python
# coding: utf-8

# Libraries
import pandas as pd
import base64
from pickle import load
import streamlit as st
import docx
import time
import clipboard
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import base64

# Trained models
vectorizer_model = load(open("Vectorizer_model_BOW.sav", "rb"))
classification_model = load(open("Classification_model.sav", "rb"))

# Email class dictionary
class_dict = {0: "Bank Services application", 1: 'Bank loan application', 2: 'Cancellation of services',
              3: 'College admission application', 4: 'Compliants of defective products', 5: 'Job application',
              6: 'Leave request', 7: 'Refund query', 8: 'Resignation'}


# ---------------Header---------------------------------------------------------------------------------

st.title('''Email Template Suggestion''')
st.image("header_image.jpg", width=500)

# ---------------Navigation Buttons---------------------------------------------------------------------------------

rad = st.sidebar.radio("Select", ["Home", "Application Description"])

# -------------Navigation - Home------------------
if rad == "Home":
    keywords = st.text_input(
        "Enter the Keywords and Click on Search")  # Input from user
    keyword_button = st.button("Search")
    if keyword_button == True:

        if keywords == "":
            st.subheader("Template")
            st.error("Please enter some keywords and click on search")
        else:
            my_bar = st.progress(0)  # Progress bar
            for p in range(100):
                time.sleep(0.001)
                my_bar.progress(p + 1)
            # Vectorization and class prediction
            array = vectorizer_model.transform(pd.Series(keywords))
            class_probability = classification_model.predict_proba(array)

            probability = "bad"
            for prob_val in class_probability[0]:
                if prob_val > 0.30:
                    probability = "Good"

            if probability != "Good":
                st.error(
                    "Keywords are not suffiecient, please try adding few more and click on search")
            else:
                email_class = classification_model.predict(array)
                teamplate_name = class_dict.get(email_class[0])

                st.subheader("Template")
                st.write("Subject: ", teamplate_name)

                # Output template display
                st.markdown(
                    "# ------------------------------------------------", True)
                template_conetnt = docx.Document(teamplate_name+".docx")
                template = f"""Subject: {teamplate_name}"""
                for para in template_conetnt.paragraphs:
                    st.markdown(para.text)
                    template = template + "\n" + para.text
                st.markdown(
                    "# ------------------------------------------------", True)
#                 clipboard.copy(template)
#                 st.success("NOTE: Template is copied to clipboard")

    if keyword_button == False:
        st.write("Waiting for user to enter the Keywords...............!!!!")

# -------------Navigation - Application Description------------------
if rad == "Application Description":
    st.header("Purpose")
    st.markdown("**Email Template Suggestion API is developed to suggest email template to the users based on the keywords provided by them.**", True)
    st.header("Adavantages")
    st.markdown(
        """> * Quick suggestion of template based on the keywords.""", True)
    st.markdown("""> * Easy to use.""", True)
    st.markdown("""> * User friendly with simple interface.""", True)
    st.markdown("""> * Time saving.""", True)
    st.header("How to Use")
    st.markdown("""**This section describes API user interface.**""", True)
    st.markdown("""> 1. Go to Home.""", True)
    st.image("Home page.PNG", width=500)
    st.markdown("""> 2. Enter the relavnt keywords and click on Search button.<br>
        *Some of the valid keywords are as follows: Leave request, Resignation, Job application, Request for credit card, Complaints of defective products, Request for passbook, Cancellation of internet services, Request for refund, College admission application, Loan application, Sick leave etc.*  """, True)
    st.image("keyword and search button.PNG", width=500)
    st.markdown("""> 3. A template will be diplayed on the screen.""", True)
    st.image("template display.PNG", width=500)


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Devloped by Jaya Gupta <a style='display: block; text-align: center;' href="https://github.com/jaya3126" target="_blank">Jaya Gupta</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)




