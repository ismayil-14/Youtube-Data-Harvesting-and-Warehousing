# Youtube-Data-Harvesting-and-Warehousing
A simple streamlit application that allows to access and analyze data from multiple youtube channels.  This application uses google api  to extract information from youtube channels and then save those data on My SQL database. 

# Technology used 
Python
MySQL
Youtube api v3
Streamlit

# How to use

To use this project , follow these steps:

1. install streamlit packages: pip install streamlit
2. Run the Streamlit app: streamlit run app.py
3. It will automatically open the web browser and then you can access it.
4. If browser does'nt start then open your web browser. You can access it by opening a new tab and entering the following URL: http://localhost:8501
5. In the Extract tab , Enter the channel ID in the text box and click the store data. 
6. The channel details will be stored on the database.
7. In the views tab, Choose your questions according to your requirements.

# Current questions available:

1. What are the names of all the videos and their corresponding channels?
2. Which channels have the most number of videos, and how many videos do they have?
3. What are the top 10 most viewed videos and their respective channels?
4. How many comments were made on each video, and what are their corresponding video names?
5. Which videos have the highest number of likes, and what are their corresponding channel names?
6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?
7. What is the total number of views for each channel, and what are their corresponding channel names?
8. What are the names of all the channels that have published videos in the year 2022?
9. What is the average duration of all videos in each channel, and what are their corresponding channel names?
10. Which videos have the highest number of comments, and what are their corresponding channel names?

# Steps involved in this project:

1. Setting up Streamlit application.
2. Connect the Streamlit application with Youtube API v3.
3. Storing the retrived data in the My SQL database.
4. Utilize SQL queries to join tables within the SQL data warehouse and retrieve specific channel data based on user input.
5. Displaying retrieved data in the streamlit application.

# Screenshots

![Home Page](https://github.com/ismayil-14/Youtube-Data-Harvesting-and-Warehousing/assets/154823988/8d17c9bc-29bc-4185-b4bb-e8a801317099)

![Data Extraction](https://github.com/ismayil-14/Youtube-Data-Harvesting-and-Warehousing/assets/154823988/e1611469-cef5-430d-96d7-4a5a05aa3abd)

![View](https://github.com/ismayil-14/Youtube-Data-Harvesting-and-Warehousing/assets/154823988/6a964965-868e-4985-8e4d-26bf353cab19)

![Data Visualization](https://github.com/ismayil-14/Youtube-Data-Harvesting-and-Warehousing/assets/154823988/020abad4-3d42-4947-9ae3-5f571865d22b)

# Contact Information:
Email : mmismayil2003@gmail.com
If you have any more questions or need further information, please don't hesitate to get in touch. We're here to help and answer any inquiries you may have.
