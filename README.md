# YouSQL-AI

YouSQL-AI is a Streamlit application that allows users to efficiently retrieve and store YouTube channel data using the YouTube API V3. By providing a YouTube channel URL, the app collects essential information including channel details, playlists, videos, and comments into an SQL database. 

Once the data is stored, Google's generative AI processes user queries. Users can ask questions in plain text, and the AI generates corresponding SQL queries. These queries are then executed on the SQL database to fetch the relevant data, perform various operations, and provide the desired output. This makes accessing and analyzing YouTube data simpler, without needing to manually write SQL queries.

## Features
- Retrieve and store YouTube channel details.
- Fetch playlists, videos, and comments from the YouTube API.
- Use Google's generative AI to convert plain text questions into SQL queries.
- Execute the queries and display the results.

## Getting Started

### Prerequisites

1. Python 3.x
2. Google API Key for YouTube API V3 and Google's generative AI API

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Santhoshsivansundaramoorthy/YouSQL-AI.git
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google API key for the YouTube API and Gemini (Google's generative AI):
   - Replace the `api_key` variables in `Collecting.py` and `llm.py` with your API keys.

### Usage

1. Run the Streamlit app:
   ```bash
   streamlit run ui.py
   ```

2. Enter the YouTube channel URL in the input field to retrieve and store channel data.
3. Ask questions in plain text about the data, and the AI will generate and execute the corresponding SQL query.

### Example Usage

- **Retrieve channel data**: 
   Provide a YouTube channel URL (e.g., `https://www.youtube.com/@somechannel`), and the app will fetch channel details, playlists, videos, and comments.

- **Ask questions**: 
   Ask questions like "What is the most popular video?" or "How many comments does the channel have?" and the app will convert these to SQL queries and display the results.

## Project Structure
```
YouSQL-AI/
│
├── ui.py              # Main Streamlit UI file
├── Database.py        # Contains functions to create and interact with the SQL database
├── Collecting.py      # Functions to interact with the YouTube API and collect data
├── llm.py             # Functions to interact with Google's generative AI and convert questions to SQL
├── Data_Lake_Youtube.db  # SQLite database file for storing YouTube data
└── requirements.txt   # List of required Python packages
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
