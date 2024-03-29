import streamlit as st
import pandas as pd
import os
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError
import pymysql
from googleapiclient.discovery import build

myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='12345678',database = "youtube")
def datetimeformatter(datetime):
    datetime = datetime[:10]+ " "+ datetime[11:-1]
    return datetime
def channel(api_key, c_id):
    print("Channel function is called")
    api_service_name = "youtube"
    api_version = "v3"
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = api_key)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=c_id
    )
    chan_dict = request.execute()
    if 'items' in chan_dict:
        upload_id = chan_dict['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        channel_name = chan_dict['items'][0]['snippet']['localized']['title']
        channel_type = 'fun'
        channel_views = chan_dict['items'][0]['statistics']['viewCount']
        channel_video = chan_dict['items'][0]['statistics']['videoCount']
        channel_subs = chan_dict['items'][0]['statistics']['subscriberCount']
        channel_description = chan_dict['items'][0]['snippet']['localized']['description']
        channel_start = datetimeformatter(chan_dict['items'][0]['snippet']['publishedAt'])
        channel_status = 'Active'
        sql = "insert into youtube.channel values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (c_id, channel_name,upload_id,channel_type,channel_views,channel_description,channel_status,channel_start,channel_subs, channel_video)
        myconnection.cursor().execute(sql,values)
        myconnection.commit()
    else:
        print("'items' key not found in chan_dict")
    if c_id:
        print("inner function in channel ")
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Retrieve all videos from the channel
        video_ids = []
        next_page_token = None
        while True:
            search_response = youtube.search().list(
                channelId=c_id,
                part='id',
                maxResults=50,
                type='video',
                pageToken=next_page_token
            ).execute()

            for item in search_response.get('items', []):
                video_ids.append(item['id']['videoId'])

            next_page_token = search_response.get('nextPageToken')
            if not next_page_token:
                break
        return video_ids
    else:
        return []

    
def playlist_id(api_key, channel_id):
    print("playlist is callled")
    youtube = build('youtube', 'v3', developerKey=api_key)
    all_playlists = []

    next_page_token = None
    while True:
        try:
            playlists_request = youtube.playlists().list(
                part='snippet,contentDetails',
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            )
            playlists_response = playlists_request.execute()

            all_playlists.extend(playlists_response['items'])

            next_page_token = playlists_response.get('nextPageToken')
            if not next_page_token:
                break  

        except HttpError as e:
            print('An HTTP error occurred:', e)
            break

    playlist_data = []
    for playlist in all_playlists:
        playlist_id = playlist['id']
        playlist_title = playlist['snippet']['title']
        video_count = int(playlist['contentDetails']['itemCount'])


        playlist_items_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=1,
        )
        playlist_items_response = playlist_items_request.execute()

        if playlist_items_response['items']:
            first_upload_date = datetimeformatter(playlist_items_response['items'][0]['snippet']['publishedAt'])
        else:
            first_upload_date = datetimeformatter("9999:12:31T23:59:59Z" )
    
        sql = "insert into youtube.playlist values (%s,%s,%s,%s,%s)"
        values = (channel_id,playlist_id,playlist_title,video_count,first_upload_date)
        myconnection.cursor().execute(sql,values)
        myconnection.commit()
def video(v_id,api_key):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = api_key)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=v_id
    )
    response = request.execute()

    return response

def time_convert(duration_str):
    hours = 0
    minutes = 0
    seconds = 0
    

    duration_str = duration_str[2:]
    

    if 'H' in duration_str:
        hours_index = duration_str.index('H')
        hours = int(duration_str[:hours_index])
        duration_str = duration_str[hours_index + 1:] 
    
    if 'M' in duration_str:
        minutes_index = duration_str.index('M')
        minutes = int(duration_str[:minutes_index])
        duration_str = duration_str[minutes_index + 1:] 
    
    if 'S' in duration_str:
        seconds_index = duration_str.index('S')
        seconds = int(duration_str[:seconds_index])
    
    total_seconds = hours * 3600 + minutes * 60 + seconds
    
    formatted_duration = "{:02d}:{:02d}:{:02d}".format(total_seconds // 3600, (total_seconds % 3600) // 60, total_seconds % 60)
    
    return formatted_duration

def save_comment_to_database(comment_id, video_id, commenter_name, comment_text, commented_time):
    sql = "INSERT INTO youtube.comment (comment_id, video_id, commenter_name, comment_text, commented_time) VALUES (%s, %s, %s, %s, %s)"
    values = (comment_id, video_id, commenter_name, comment_text, commented_time)
    myconnection.cursor().execute(sql, values)
    myconnection.commit()

def fetch_comments_and_save_to_database(api_key, video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    comments = []
    next_page_token = None
    total_comments = 0

    try:
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get('items', []):
                comment_snippet = item['snippet']['topLevelComment']['snippet']
                comment_id = item['id']
                comment_text = comment_snippet['textDisplay']
                commenter_name = comment_snippet['authorDisplayName']
                commented_time = datetimeformatter(comment_snippet['publishedAt'])

                # Save the comment to the database
                save_comment_to_database(comment_id, video_id, commenter_name, comment_text, commented_time)
                total_comments += 1

            next_page_token = response.get('nextPageToken')
            if not next_page_token or total_comments >= 50:  # Adjust the condition as needed
                break

    except HttpError as e:
        if e.resp.status == 403:
            print("Comments are disabled for this video.")
        else:
            raise e
    

def channel_table(channel_id , chan_dict):
    upload_id = chan_dict['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    channel_name = chan_dict['items'][0]['snippet']['localized']['title']
    channel_type = chan_dict['items'][0]['kind']
    channel_views = chan_dict['items'][0]['statistics']['viewCount']
    channel_video = chan_dict['items'][0]['statistics']['videoCount']
    channel_subs = chan_dict['items'][0]['statistics']['subscriberCount']
    channel_description = chan_dict['items'][0]['snippet']['localized']['description']
    channel_start = datetimeformatter(chan_dict['items'][0]['snippet']['publishedAt'])
    channel_status = 'Active'
    
    sql = "insert into youtube.channel values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (channel_id, channel_name,upload_id,channel_type,channel_views,channel_description,channel_status,channel_start,channel_subs, channel_video)
    myconnection.cursor().execute(sql,values)
    myconnection.commit()

def vid_id(v_id,api_key):
    
    video_data = video(v_id,api_key)
    video_id = video_data['items'][0] ['id']
    channel_id = video_data['items'][0] ['snippet']["channelId"]
    channel_title = video_data['items'][0] ['snippet']["channelTitle"]
    video_name = video_data['items'][0] ['snippet']['title']
    video_description = video_data['items'][0] ['snippet']['description']
    published_date = datetimeformatter(video_data['items'][0] ['snippet']['publishedAt'])
    view_count = video_data['items'][0] ['statistics'].get('viewCount',0) 
    like_count = video_data['items'][0] ['statistics'].get('likeCount',0) 
    dislike_count = 0
    favorite_count = video_data['items'][0] ['statistics'].get('favoriteCount',0) 
    comment_count = video_data['items'][0]['statistics'].get('commentCount', 0)

    duration = time_convert(video_data['items'][0] ['contentDetails']['duration'])
    thumbnail = video_data['items'][0] ['snippet']['thumbnails']['high']['url']
    if video_data['items'][0] ['contentDetails']['caption']:
        caption_status= "Enabled"
    else:
        caption_status = "Disabled"
    
    
    sql = "insert into youtube.video_table values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values = (channel_id, video_id, video_name, video_description, published_date, view_count, like_count,dislike_count, favorite_count, comment_count, duration, thumbnail, caption_status)
    myconnection.cursor().execute(sql,values)
    myconnection.commit()


def youtube(c_id):
    api_key = "AIzaSyCdb_ttkfMTa9s74_x41wfkBO9EX1InpBQ"
    video_ids = channel(api_key, c_id)
    playlist_id(api_key, c_id)

    for i in video_ids:
        vid_id(i,api_key)
        fetch_comments_and_save_to_database(api_key, i )

 




# Page layout
st.title("YOUTUBE DATA HARVESTING AND WAREHOUSING USING MYSQL AND STREAMLIT")

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["HOME", "EXTRACTION", "VIEW"])
# Render pages based on tab selection
with tab1:
    st.write("## About the Project")
    st.write("A simple streamlit application that allows to access and analyze data from multiple youtube channels. \n This application uses google api  to extract information from youtube channels and then save those data on My SQL database. ")
    #st.write("Developed by: [Your Name]")

with tab2:
    st.write("## Data Extraction")
    user_input = st.text_input("Enter Channel ID:")
    if st.button("Store Data"):
        youtube(user_input)
        st.success("Data stored successfully!")

with tab3:
    st.write("## View Data")
    st.subheader("Select a question:")
    question = st.selectbox("Choose a question", [" ","What are the names of all the videos and their corresponding channels?",
"Which channels have the most number of videos, and how many videos do they have?",
"What are the top 10 most viewed videos and their respective channels?",
"How many comments were made on each video, and what are their corresponding video names?",
"Which videos have the highest number of likes, and what are their corresponding channel names?",
"What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
"What is the total number of views for each channel, and what are their corresponding channel names?",
"What are the names of all the channels that have published videos in the year 2022?",
"What is the average duration of all videos in each channel, and what are their corresponding channel names?",
"Which videos have the highest number of comments, and what are their corresponding channel names?"
])

    if question == "What are the names of all the videos and their corresponding channels?":
        query = """Select v.video_name as "Video name", c.channel_name as "Channel name" from video_table as v left join channel as c on c.channel_id =v.channel_id; """
        dataFrame = pd.read_sql_query(query,myconnection)
    elif question == "Which channels have the most number of videos, and how many videos do they have?":
        query = """Select channel_name as "Channel name" , video_count as "Number of videos" from channel order by video_count desc;"""
        dataFrame = pd.read_sql_query(query,myconnection)
    elif question ==  "What are the top 10 most viewed videos and their respective channels?":
        query = """Select c.channel_name as "Channel name" , v.video_name as "Video name" , v.video_views as "Number of views" from video_table as v left join channel as c on v.channel_id = c.channel_id order by v.video_views desc limit 10;"""
        dataFrame = pd.read_sql_query(query,myconnection)
    elif question ==  "How many comments were made on each video, and what are their corresponding video names?":
        query = """ Select video_name as "Video Name" , video_comments as "Number of comments" from video_table; """
        dataFrame = pd.read_sql_query(query,myconnection)
    elif question ==  "Which videos have the highest number of likes, and what are their corresponding channel names?":
        query = """ Select c.channel_name as "Channel name" , v.video_name as "Video name" , v.video_likes as "Number of likes" from video_table as v left join channel as c on c.channel_id = v.channel_id order by video_likes desc limit 10; """
        dataFrame = pd.read_sql_query(query,myconnection)
    elif question ==  "What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
        query = """Select video_name as "Video name" , video_likes as "Number of likes" from video_table;"""
        dataFrame = pd.read_sql_query(query,myconnection)
    elif question ==  "What is the total number of views for each channel, and what are their corresponding channel names?":
        query = """ Select channel_name as "Channel name" , channel_views as "Number of views" from channel; """
        dataFrame = pd.read_sql_query(query,myconnection)
    elif question ==  "What are the names of all the channels that have published videos in the year 2022?":
        query = """ select c.channel_name as "Channel name" , count(v.video_id) as "Video count" from video_table as v left join channel as c on v.channel_id = c.channel_id where year(video_published_on) = 2022 group by c.channel_name;"""
        dataFrame = pd.read_sql_query(query,myconnection)
    elif question ==  "What is the average duration of all videos in each channel, and what are their corresponding channel names?":
        query = """ Select c.channel_name as "Channel name", sec_to_time(avg( time_to_sec (v.duration) )) as "Average duration"  from video_table as v left join channel as c on v.channel_id = c.channel_id group by v.channel_id, c.channel_name; """
        dataFrame = pd.read_sql_query(query,myconnection)
    elif question ==  "Which videos have the highest number of comments, and what are their corresponding channel names?":
        query = """Select c.channel_name as "Channel name" , v.video_name as "Video name" , v.video_comments as "No. of comments" from video_table as v left join channel as c on c.channel_id= v.channel_id order by v.video_comments desc limit 10;"""
        dataFrame = pd.read_sql_query(query,myconnection)
    if question != " ":
        st.dataframe(dataFrame)
