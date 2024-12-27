# BookScape-Explorer
The BookScape Explorer project aims to facilitate users in discovering and analyzing book data through a web application. The application will extract data from online book APIs, store this information in a SQL database, and enable data analysis using SQL queries.

# Project Overview

The Books Explorer project is a web-based application built using Streamlit and MySQL. 
It allows users to:

1. Search for books using the Google Books API.
 
2. View detailed analytics on books stored in the database.
 
3. Answer frequently asked questions about books based on SQL queries.

# Project Objectives

Data Integration: Combine external API data with database analytics.

Data Storage: Create a SQL database with well-designed schema using appropriate data types and primary keys.

Interactive Visualization: Present results in an engaging and user-friendly format.

Scalability: Create a framework that supports additional queries and features.

# Setup Instructions

## Prerequisites

Python 3.7+

MySQL Server

Google Books API Key

## Required Python Libraries:

streamlit

pymysql

pandas

requests

# Installation Steps

1. Clone the Repository

 git clone https://github.com/your-repo/books-explorer.git
cd books-explorer

2. Install Dependencies

 pip install -r requirements.txt

3. Set Up MySQL Database
   
  Create a database named database2.

  Import the schema and data from database2.sql.

4. Add Google Books API Key
   
  Replace the api_key variable in the script with your API key.

5. Run the Application

  streamlit run app.py

6. Access the Application

  Open http://localhost:8501 in your browser.


