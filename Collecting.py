import isodate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
from urllib.parse import urlparse

from Database import insert_video, insert_channel, insert_comment
import streamlit as st

youtube_api_key = st.secrets["api_keys"]["youtube_api_key"]


def get_channel_id_from_handle(url):
    api_key = youtube_api_key
    # Extract the handle from the URL
    parsed_url = urlparse(url)
    handle = parsed_url.path.lstrip("/")  # Remove leading '/'

    if not handle.startswith("@"):
        print("Invalid handle-based URL.")
        return None

    # Use YouTube API search.list to retrieve channel ID by handle
    api_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": handle,  # Use handle for search
        "type": "channel",
        "key": api_key
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    # Check if a valid response with items is received
    if "items" in data and len(data["items"]) > 0:
        return data["items"][0]["snippet"]["channelId"]
    else:
        print("Channel not found or invalid handle.")
        return None

def get_Channel_data(channel_id):

    api_key = youtube_api_key
    # Build the YouTube service
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Fetch channel information
    channel_request = youtube.channels().list(
        part='snippet,statistics,contentDetails',
        id=channel_id
    )
    channel_response = channel_request.execute()

    channel_info = channel_response['items'][0]
    channel_name = channel_info['snippet']['title']
    channel_description = channel_info['snippet']['description']
    subscription_count = channel_info['statistics'].get('subscriberCount', 0)
    channel_views = channel_info['statistics'].get('viewCount', 0)

    insert_channel(channel_id,channel_name,subscription_count,channel_views,channel_description)

    # Get all playlist IDs of the channel
    playlist_request = youtube.playlists().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=3000  # Fetches up to 50 playlists
    )
    playlist_response = playlist_request.execute()

    if 'items' not in playlist_response or not playlist_response['items']:
        print("No playlists found for this channel.")
        playlists_dict = {}
    else:
        playlists_dict = {item['snippet'].get('title', 'No Title'): item.get('id', 'No ID')
                          for item in playlist_response.get('items', [])}

    playlist_information = {
        'Playlist': playlists_dict
    }

    return playlist_information


def get_videos_from_playlist(playlist_id):
    api_key = "AIzaSyDtDcr_6cc1ZUiCgy7OQ0DuT20iyqyQbjM"

    def convert_duration_to_hh_mm_ss(duration):
        parsed_duration = isodate.parse_duration(duration)
        total_seconds = int(parsed_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    youtube = build('youtube', 'v3', developerKey=api_key)


    for pid in playlist_id:
        next_page_token = None
        while True:
            request = youtube.playlistItems().list(
                part="snippet",
                maxResults=50,
                playlistId=pid,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_request = youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=video_id
                )
                video_response = video_request.execute()
                if 'items' in video_response and len(video_response['items']) > 0:
                    video_data = video_response['items'][0]
                    duration = convert_duration_to_hh_mm_ss(video_data['contentDetails']['duration'])
                    Video_Name = video_data['snippet']['title']
                    Video_Description = video_data['snippet']['description']
                    PublishedAt = video_data['snippet']['publishedAt']
                    View_Count = int(video_data['statistics'].get('viewCount', 0))
                    Like_Count = int(video_data['statistics'].get('likeCount', 0))
                    Comment_Count = int(video_data['statistics'].get('commentCount', 0))
                    Duration = duration
                    insert_video(video_id,Video_Name,Video_Description,PublishedAt,View_Count,Like_Count,Comment_Count,Duration,pid)
                    print(video_id)

                    try:
                        # Fetch comments for the video
                        comment_request = youtube.commentThreads().list(
                            part='snippet',
                            videoId=video_id,
                            maxResults=50
                        )
                        comments = {}
                        while comment_request:
                            comment_response = comment_request.execute()
                            for item in comment_response['items']:
                                comment_id = item['snippet']['topLevelComment']['id']
                                comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                                author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                                published_at = item['snippet']['topLevelComment']['snippet']['publishedAt']
                                insert_comment(comment_id, comment_text, author, published_at, video_id)
                            comment_request = youtube.commentThreads().list_next(comment_request, comment_response)
                    except HttpError as e:
                        if e.resp.status == 403 and 'commentsDisabled' in str(e):
                            print(f"Comments disabled for video {video_id}")
                            continue


            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break




