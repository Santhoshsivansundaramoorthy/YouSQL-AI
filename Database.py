import sqlite3


def create_table():
    # Connecting and Creating if not exist to SQLite Database
    conn = sqlite3.connect('Data_Lake_Youtube.db')
    # Creating a Custom Cursor Object
    cursor = conn.cursor()
    # Enable foreign key support in SQLite (required for some versions)
    cursor.execute('PRAGMA foreign_keys = ON')
    # Create a table (if it doesn't exist)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Channel (
        Channel_ID VARCHAR(255) PRIMARY KEY,
        Channel_name VARCHAR(255),
        Subscription_Count INT,
        Channel_Views INT,
        Channel_Description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Playlist (
        Playlist_ID VARCHAR(255) PRIMARY KEY,
        Playlist_Name VARCHAR(255),
        Channel_ID VARCHAR(255),
        FOREIGN KEY (Channel_ID) REFERENCES Channel (Channel_ID) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Video (
        Video_ID VARCHAR(255) PRIMARY KEY,
        Video_Name VARCHAR(255),
        Video_Description TEXT,
        Published_Date DATETIME,
        View_count INT,
        Like_count INT,
        Comment_count INT,
        Duration INT,
        Playlist_ID VARCHAR(255),
        FOREIGN KEY (Playlist_ID) REFERENCES Playlist (Playlist_ID) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Comment (
        Comment_ID VARCHAR(255) PRIMARY KEY,
        Comment_Text TEXT,
        Comment_Author VARCHAR(255),
        Comment_Published_Date DATETIME,
        Video_ID VARCHAR(255),
        FOREIGN KEY (Video_ID) REFERENCES Video (Video_ID) ON DELETE CASCADE

    )
    ''')

    conn.commit()
    conn.close()


def insert_channel(channel_id, channel_name, subscription_count, channel_views, channel_description):
    conn = sqlite3.connect('Data_Lake_Youtube.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO Channel (Channel_ID, Channel_name, Subscription_Count, Channel_Views, Channel_Description)
        VALUES (?, ?, ?, ?, ?)
    ''', (channel_id, channel_name, subscription_count, channel_views, channel_description))
    conn.commit()
    conn.close()


def insert_playlist(playlist_id, playlist_name, channel_id):
    conn = sqlite3.connect('Data_Lake_Youtube.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO Playlist (Playlist_ID, Playlist_Name, Channel_ID)
        VALUES (?, ?, ?)
    ''', (playlist_id, playlist_name, channel_id))
    conn.commit()
    conn.close()


def insert_video(video_id, video_name, video_description, published_date, view_count, like_count, comment_count,
                 duration, playlist_id):
    conn = sqlite3.connect('Data_Lake_Youtube.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO Video (Video_ID, Video_Name, Video_Description, Published_Date, View_count, Like_count, Comment_count, Duration, Playlist_ID)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (video_id, video_name, video_description, published_date, view_count, like_count, comment_count, duration,
          playlist_id))
    conn.commit()
    conn.close()


def insert_comment(comment_id, comment_text, comment_author, comment_published_date, video_id):
    conn = sqlite3.connect('Data_Lake_Youtube.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO Comment (Comment_ID, Comment_Text, Comment_Author, Comment_Published_Date, Video_ID)
        VALUES (?, ?, ?, ?, ?)
    ''', (comment_id, comment_text, comment_author, comment_published_date, video_id))
    conn.commit()
    conn.close()
