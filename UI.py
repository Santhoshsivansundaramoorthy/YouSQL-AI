import streamlit as st
from Database import create_table, insert_playlist
from Collecting import get_videos_from_playlist, get_Channel_data, get_channel_id_from_handle
from llm import get_gemini_response, read_sql_query

st.title("YouSQL-AI")
st.write("""This application allows users to retrieve and store YouTube channel data efficiently using the YouTube API V3. By simply providing a YouTube channel URL, the app collects and stores essential information including channel details, playlists, videos, and comments into an SQL database.

Once the data is stored, Google’s generative AI is used to process user queries. Users can ask questions in plain text, and the AI generates the corresponding SQL query. The query is then executed to fetch the data, perform various operations, and provide the desired output. This makes it easy to access and analyze YouTube data without needing to manually write SQL queries.""")
create_table()
st.write("\n")
st.write("\n")
with st.sidebar:
    st.header("Retrieve and Store the Channel Detail")
    url = st.text_input("Enter the Channel URL:")
    channelId = get_channel_id_from_handle(url)
    fetchChannelDetails = st.button("Fetch and Store")
    if fetchChannelDetails:
        with st.spinner('Retrieving and Storing Channel Data... '):
            Playlist_info = get_Channel_data(channelId)
        st.success("Channel Data - Retrieved and Saved, Proceeding with Playlist")
        with st.spinner('Retrieving and Storing Video and Comment Data... '):
            for name, playlist_id in Playlist_info['Playlist'].items():
                insert_playlist(playlist_id, name, channelId)
        st.success("Playlist Data - Retrieved and Saved, Proceeding with Video and Comments")
        playlist_ids = list(Playlist_info['Playlist'].values())
        with st.spinner('Retrieving and Storing Video and Comment Data... '):
            get_videos_from_playlist(playlist_ids)
        st.success(f"Video and Comment data - Retrieved and Saved - All Process for {channelId} is Complete")
    url_format = """
**URL Format**

The correct URL format should be:

`https://www.youtube.com/@xxxxx`

You can find this format in the URL bar when you visit the channel's landing page on YouTube.  
**Please note:** Any other format will not work."""
    st.markdown(url_format)

question = st.text_input("Enter the Question:")
ask = st.button("Ask")
if ask:
    with st.spinner('Processing...'):
        answer = get_gemini_response(question)
        data = read_sql_query(answer, "Data_Lake_Youtube.db")
        data = [row[0] for row in data]
        data = "\n".join(f"- {d}" for d in data)
        st.write("SQL Query:")
        st.markdown(f'{answer}',
                    unsafe_allow_html=True)
        st.markdown(f' Answer:\n{data}',
                    unsafe_allow_html=True)
