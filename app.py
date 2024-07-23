# import streamlit as st
# from dotenv import load_dotenv
# import base64
# load_dotenv() 
# import os
# import google.generativeai as genai

# from youtube_transcript_api import YouTubeTranscriptApi

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt="""You are Yotube video summarizer. You will be taking the transcript text
# and summarizing the entire video and providing the important summary in points
# within 250 words. Please provide the summary of the text given here:  """


# ## getting the transcript data from yt videos
# def extract_transcript_details(youtube_video_url):
#     try:
#         video_id=youtube_video_url.split("=")[1]
   
#         transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

#         transcript = ""
#         for i in transcript_text:
#             transcript += " " + i["text"]

#         return transcript

#     except Exception as e:
#         raise e
    
# ## getting the summary based on Prompt from Google 
# def generate_gemini_content(transcript_text,prompt):

#     model=genai.GenerativeModel("gemini-1.5-flash")
#     response=model.generate_content(prompt+transcript_text)
#     return response.text
# # def add_bg_from_local(image_file):
# #     with open(image_file, "rb") as f:
# #         data_uri = base64.b64encode(f.read()).decode("utf-8")
# #     st.markdown(
# #         f"""
# #         <style>
# #         .stApp {{
# #             background-image: url("data:image/jpeg;base64,{data_uri}");
# #             background-size: cover;
# #             background-repeat: no-repeat;
# #             background-attachment: fixed;
# #         }}
# #         </style>
# #         """,
# #         unsafe_allow_html=True
# #     )

# # Add the background image
# # add_bg_from_local('bg2.jpeg')
# st.title("YouTube Transcript to Detailed Notes Converter")
# # st.markdown("<h1 style='text-align: center; color: black; font-weight: bold;'>YouTube Transcript to Detailed Notes Converter</h1>", unsafe_allow_html=True)
# youtube_link = st.text_input("Enter YouTube Video Link:")

# if youtube_link:
#     video_id = youtube_link.split("=")[1]
#     print(video_id)
#     st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# if st.button("Get Detailed Notes"):
#     transcript_text=extract_transcript_details(youtube_link)

#     if transcript_text:
#         summary=generate_gemini_content(transcript_text,prompt)
#         st.markdown("## Detailed Notes:")
#         st.write(summary)


import streamlit as st
from dotenv import load_dotenv
import os
import base64
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import google.generativeai as genai
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
from fpdf import FPDF
import tempfile

# Load environment variables
load_dotenv()

# Configure API keys
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
youtube_api_key = os.getenv("YOUTUBE_API_KEY")

# Define the prompt for Google Gemini based on summary length
def get_prompt(summary_length):
    if summary_length == "Short":
        return """You are a YouTube video summarizer. Summarize the video transcript in a concise manner, providing a brief summary within 100 words."""
    elif summary_length == "Medium":
        return """You are a YouTube video summarizer. Summarize the video transcript, providing a summary within 250 words."""
    elif summary_length == "Long":
        return """You are a YouTube video summarizer. Provide a detailed summary of the video transcript, covering key points and insights within 500 words."""
    else:
        return """You are a YouTube video summarizer. Provide a summary of the video transcript."""

# Function to get YouTube video details
def get_video_details(video_id):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    return response["items"][0]["snippet"]

# Function to extract transcript details
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        timestamps = [(item['start'], item['text']) for item in transcript_text]
        return transcript, timestamps
    except Exception as e:
        st.error(f"Error: {e}")
        return None, None

# Function to generate summary using Google Gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Function to perform sentiment analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity

def sentiment_summary(polarity, subjectivity):
    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return (f"Sentiment: {sentiment}\n"
            f"Polarity: {polarity:.2f} (range: -1 to 1)\n"
            f"Subjectivity: {subjectivity:.2f} (range: 0 to 1)")

# Function to perform topic modeling
def perform_topic_modeling(text):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform([text])
    lda = LatentDirichletAllocation(n_components=3, random_state=0)
    lda.fit(X)
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        topics.append(f"Topic {topic_idx + 1}: " + ", ".join([feature_names[i] for i in topic.argsort()[:-6:-1]]))
    return topics

# Function to extract keywords
def extract_keywords(text, num_keywords=10):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
    word_count_vector = vectorizer.fit_transform([text])
    sum_words = word_count_vector.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return [word for word, freq in words_freq[:num_keywords]]

# Function to highlight key moments
def highlight_key_moments(timestamps):
    return [(start, text) for start, text in timestamps if len(text.split()) > 10]

# Function to generate word cloud
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

# Function to convert HTML to PDF using FPDF
def convert_html_to_pdf(html_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Adding HTML content to PDF (not directly supported by FPDF, so using a simple text approach)
    pdf.multi_cell(0, 10, html_content)
    
    # Write PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        pdf_output_path = temp_file.name
        pdf.output(pdf_output_path)
    
    # Read PDF into BytesIO
    with open(pdf_output_path, "rb") as f:
        pdf_bytes = f.read()
    
    # Remove the temporary file
    os.remove(pdf_output_path)
    
    return pdf_bytes

# Streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")

summary_length = st.selectbox("Select Summary Length", ["Short", "Medium", "Long"])

if youtube_link:
    video_id = youtube_link.split("=")[1]
    video_details = get_video_details(video_id)
    if video_details:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        st.write(f"**Title:** {video_details['title']}")
        st.write(f"**Channel:** {video_details['channelTitle']}")
        st.write(f"**Published on:** {video_details['publishedAt']}")
        st.write(f"**Description:** {video_details['description']}")

if st.button("Get Detailed Notes"):
    transcript_text, timestamps = extract_transcript_details(youtube_link)
    if transcript_text:
        prompt = get_prompt(summary_length)
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
        
        sentiment_polarity, sentiment_subjectivity = analyze_sentiment(transcript_text)
        st.markdown("## Sentiment Analysis:")
        st.write(sentiment_summary(sentiment_polarity, sentiment_subjectivity))
        
        topics = perform_topic_modeling(transcript_text)
        st.markdown("## Topics Discussed:")
        st.write("\n".join(topics))
        
        key_moments = highlight_key_moments(timestamps)
        st.markdown("## Key Moments:")
        for start, text in key_moments:
            st.write(f"**Timestamp:** {start:.2f} seconds - {text}")
        
        keywords = extract_keywords(transcript_text)
        st.markdown("## Keywords:")
        st.write(", ".join(keywords))
        
        wordcloud = generate_wordcloud(transcript_text)
        st.markdown("## Word Cloud:")
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        st.image(buf.getvalue())
        
        # Generate HTML content for PDF
        html_content = f"""
        <html>
        <head><title>YouTube Notes</title></head>
        <body>
        <h1>YouTube Video Notes</h1>
        <h2>Summary:</h2>
        <p>{summary}</p>
        <h2>Sentiment Analysis:</h2>
        <p>{sentiment_summary(sentiment_polarity, sentiment_subjectivity)}</p>
        <h2>Topics Discussed:</h2>
        <p>{"<br>".join(topics)}</p>
        <h2>Key Moments:</h2>
        <ul>
            {"<br>".join([f"<li>Timestamp: {start:.2f} seconds - {text}</li>" for start, text in key_moments])}
        </ul>
        <h2>Keywords:</h2>
        <p>{', '.join(keywords)}</p>
        <h2>Word Cloud:</h2>
        <img src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"/>
        </body>
        </html>
        """
        
        # Convert HTML to PDF
        pdf = convert_html_to_pdf(html_content)
        
        st.download_button(label="Download as PDF", data=pdf, file_name="summary.pdf", mime="application/pdf")
        st.download_button(label="Download as Text", data=summary, file_name="summary.txt", mime="text/plain")
        st.download_button(label="Download Word Cloud", data=buf.getvalue(), file_name="wordcloud.png", mime="image/png")
