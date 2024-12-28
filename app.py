import requests
import streamlit as st
import pandas as pd
import pymysql
# Your Google Books API key
api_key = "api_key"

# Function to fetch books from Google Books API
def fetch_books(query, api_key, max_results=50):
    books = []
    url = "https://www.googleapis.com/books/v1/volumes"
    start_index = 0
    max_per_request = 40

    while start_index < max_results:
        params = {
            "q": query,
            "key": api_key,
            "startIndex": start_index,
            "maxResults": min(max_per_request, max_results - start_index),
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            st.error(f"Error: {response.status_code} - {response.text}")
            return []

        data = response.json()
        items = data.get("items", [])
        if not items:
            break

        for item in items:
            volume_info = item.get("volumeInfo", {})
            sale_info = item.get("saleInfo", {})
            books.append({
                "book_id": item.get("id", ""),
                "book_title": volume_info.get("title", ""),
                "book_subtitle": volume_info.get("subtitle", "NA"),
                "book_authors": ", ".join(volume_info.get("authors", [])),
                "book_description": volume_info.get("description", ""),
                "categories": ", ".join(volume_info.get("categories", [])),
                "published_year": volume_info.get("publishedDate", "")[:4],
                "saleability": sale_info.get("saleability", ""),
                "list_price": sale_info.get("listPrice", {}).get("amount", 0.0),
                "currencyCode_listPrice": sale_info.get("listPrice", {}).get("currencyCode", ""),
                "retail_price": sale_info.get("retailPrice", {}).get("amount", 0.0),
                "currencyCode_retailPrice": sale_info.get("retailPrice", {}).get("currencyCode", ""),
                "average_rating": volume_info.get("averageRating", None),
                "ratings_count": volume_info.get("ratingsCount", 0),
                "page_count": volume_info.get("pageCount", 0),
                "language": volume_info.get("language", ""),
                "is_ebook": sale_info.get("isEbook", False),
                "buy_link": sale_info.get("buyLink", ""),
            })

        start_index += max_per_request

    return books

# MySQL connection function
def get_mysql_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="D8g11U77",
        database="database2"
    )

# Streamlit Application
st.title("Books Explorer 📚")

# Tabs for navigation
tab1, tab2 = st.tabs(["Home", "Books Analysis"])

# Search Tab
with tab1:
    st.header("Books Table")
    search_query = st.text_input("Enter your search query:", "")
    if search_query:
        st.write(f"Searching for: **{search_query}**")
        books_data = fetch_books(search_query, api_key)
        if books_data:
            books_df = pd.DataFrame(books_data)
            st.dataframe(books_df)
        else:
            st.warning("No books found. Please try a different query.")

# Analysis Tab
# Analysis Tab
with tab2:
    st.header("Frequently Asked Questions")
    conn = get_mysql_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # SQL queries
    query0 = """
        SELECT 
            book_title, 
            book_authors, 
            ratingsCount, 
            averageRating 
        FROM books_table
        WHERE ratingsCount > (SELECT AVG(ratingsCount) FROM books_table)
        ORDER BY ratingsCount DESC;
    """
    query1 = """
        SELECT 
            book_publisher, 
            AVG(averageRating) AS avg_rating 
        FROM database2.books_table 
        WHERE averageRating IS NOT NULL 
        GROUP BY book_publisher 
        ORDER BY avg_rating DESC 
        LIMIT 1
    """
    query2 = """
        SELECT 
            isEbook, 
            COUNT(*) AS count 
        FROM books_table
        GROUP BY isEbook
    """
    query3 = """
        SELECT 
            book_title, 
            book_authors, 
            amount_retailPrice 
        FROM books_table
        WHERE amount_retailPrice IS NOT NULL
        ORDER BY amount_retailPrice DESC
        LIMIT 5
    """
    query4 = """
        SELECT 
            book_title, 
            book_authors, 
            year, 
            pageCount 
        FROM books_table
        WHERE CAST(year AS UNSIGNED) > 2010 AND pageCount >= 500
    """
    query5 = """
        SELECT 
            book_title, 
            book_authors, 
            amount_listPrice, 
            amount_retailPrice, 
            ROUND(((amount_listPrice - amount_retailPrice) / amount_listPrice) * 100, 2) AS discount_percentage
        FROM books_table
        WHERE amount_listPrice IS NOT NULL AND 
              amount_retailPrice IS NOT NULL AND 
              ((amount_listPrice - amount_retailPrice) / amount_listPrice) > 0.20
    """
    query6 = """
        SELECT 
            isEbook, 
            AVG(pageCount) AS average_page_count 
        FROM books_table
        WHERE pageCount IS NOT NULL
        GROUP BY isEbook
    """
    query7 = """
        SELECT 
            book_authors, 
            COUNT(*) AS total_books 
        FROM books_table
        WHERE book_authors IS NOT NULL
        GROUP BY book_authors
        ORDER BY total_books DESC
        LIMIT 3
    """
    query8 = """
        SELECT 
            book_publisher, 
            COUNT(*) AS total_books 
        FROM books_table
        WHERE book_publisher IS NOT NULL
        GROUP BY book_publisher
        HAVING total_books > 10
    """
    query9 = """
        SELECT 
            categories, 
            AVG(pageCount) AS average_page_count 
        FROM books_table
        WHERE pageCount IS NOT NULL AND 
              categories IS NOT NULL
        GROUP BY categories
    """
    
    # Execute queries and fetch data
    cursor.execute(query0)
    data0 = cursor.fetchall()

    cursor.execute(query1)
    data1 = cursor.fetchone()

    cursor.execute(query2)
    data2 = cursor.fetchall()

    cursor.execute(query3)
    data3 = cursor.fetchall()

    cursor.execute(query4)
    data4 = cursor.fetchall()

    cursor.execute(query5)
    data5 = cursor.fetchall()

    cursor.execute(query6)
    data6 = cursor.fetchall()

    cursor.execute(query7)
    data7 = cursor.fetchall()

    cursor.execute(query8)
    data8 = cursor.fetchall()

    cursor.execute(query9)
    data9 = cursor.fetchall()

    conn.close()

    # Display results using expanders
    with st.expander("List of Books with Ratings Count Greater Than the Average"):
        if data0:
            for row in data0:
                st.write(f"**Title:** {row['book_title']}, **Author(s):** {row['book_authors']}, **Ratings Count:** {row['ratingsCount']}, **Average Rating:** {row['averageRating']:.2f}")
        else:
            st.warning("No data available.")

    with st.expander("Find the Publisher with the Highest Average Rating"):
        if data1:
            st.markdown(f"**Publisher:** {data1['book_publisher']} <br> **Average Rating:** {data1['avg_rating']:.2f}", unsafe_allow_html=True)
        else:
            st.warning("No data available.")

    with st.expander("Check Availability of eBooks vs Physical Books"):
        if data2:
            for row in data2:
                book_type = "eBooks" if row["isEbook"] == 1 else "Physical Books"
                st.write(f"{book_type}: {row['count']} books")
        else:
            st.warning("No data available.")

    with st.expander("Get the Top 5 Most Expensive Books by Retail Price"):
        if data3:
            for row in data3:
                st.write(f"**Title:** {row['book_title']}, **Author(s):** {row['book_authors']}, **Price:** ${row['amount_retailPrice']}")
        else:
            st.warning("No data available.")

    with st.expander("Find Books Published After 2010 with at Least 500 Pages"):
        if data4:
            for row in data4:
                st.write(f"**Title:** {row['book_title']}, **Author(s):** {row['book_authors']}, **Year:** {row['year']}, **Pages:** {row['pageCount']}")
        else:
            st.warning("No data available.")

    with st.expander("List Books with Discounts Greater than 20%"):
        if data5:
            for row in data5:
                st.write(f"**Title:** {row['book_title']}, **Author(s):** {row['book_authors']}, **Discount:** {row['discount_percentage']}%")
        else:
            st.warning("No data available.")

    with st.expander("Find the Average Page Count for eBooks vs Physical Books"):
        if data6:
            for row in data6:
                book_type = "eBooks" if row["isEbook"] == 1 else "Physical Books"
                st.write(f"{book_type}: {row['average_page_count']:.2f} pages (average)")
        else:
            st.warning("No data available.")

    with st.expander("Find the Top 3 Authors with the Most Books"):
        if data7:
            for row in data7:
                st.write(f"**Author(s):** {row['book_authors']}, **Total Books:** {row['total_books']}")
        else:
            st.warning("No data available.")

    with st.expander("List Publishers with More than 10 Books"):
        if data8:
            for row in data8:
                st.write(f"**Publisher:** {row['book_publisher']}, **Total Books:** {row['total_books']}")
        else:
            st.warning("No data available.")

    with st.expander("Find the Average Page Count for Each Category"):
        if data9:
            for row in data9:
                st.write(f"**Category:** {row['categories']}, **Average Pages:** {row['average_page_count']:.2f}")
        else:
            st.warning("No data available.")

