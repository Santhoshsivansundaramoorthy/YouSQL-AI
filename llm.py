import sqlite3
import google.generativeai as genai
import toml

# Load the config file
config = toml.load("config.toml")

genai_api_key = config["api_keys"]["genai_api_key"]

genai.configure(api_key=genai_api_key)


def get_gemini_response(question):
    prompt = [
        """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name Channel and has the following columns - Channel_ID VARCHAR(255) PRIMARY KEY, Channel_name VARCHAR(255), Subscription_Count INT, Channel_Views INT, Channel_Description TEXT. 
    The SQL database has the name Playlist and has the following columns - Playlist_ID VARCHAR(255) PRIMARY KEY, Playlist_Name VARCHAR(255), Channel_ID VARCHAR(255) a foreign key linking to Channel_ID of the Channel Tables.
    The SQL database has the name Video and has the following columns - Video_ID VARCHAR(255) PRIMARY KEY, Video_Name VARCHAR(255), Video_Description TEXT, Published_Date DATETIME, View_count INT, Like_count INT, Comment_count INT, Duration INT, Playlist_ID VARCHAR(255) a foreign key linking to Playlist_ID of the Playlist Tables.
    The SQL database has the name Comment and has the following columns - Comment_ID VARCHAR(255) PRIMARY KEY, Comment_Text TEXT, Comment_Author VARCHAR(255), Comment_Published_Date DATETIME, Video_ID VARCHAR(255) a foreign key linking to Video_ID of the Video Tables.

    For Example,

    Example 1 - How many entries of records are present in Channel?, the SQL command will be something like this SELECT COUNT(*) FROM Channel ;
    Example 2 - Tell me all the channel name?, the SQL command will be something like this SELECT Channel_name FROM Channel;

    also the sql code should not have ``` in beginning or end and sql word in output.
    Use appropriate joins based on foreign key relationships where necessary.
    Please do not make up things, All data should only be retrieved from the given Table.

        """

    ]
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    response_data = response.candidates
    output = response_data[0].content.parts[0].text

    return output

def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

