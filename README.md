

# 📹 YouTube Notes Maker and Video Analyzer

Welcome to the **YouTube Notes Maker** project! This tool enables you to extract and summarize YouTube video transcripts, analyze sentiments, identify key topics, and highlight important moments from videos. It also provides downloadable summaries and visualizations for a comprehensive overview of the video content.

## 🛠️ Features

- **🎬 Video Transcript Extraction**: Retrieve the transcript of any YouTube video using its URL.
- **✍️ Summarization**: Get a detailed summary of the video transcript with customizable length (Short, Medium, Long).
- **📊 Sentiment Analysis**: Analyze the overall sentiment of the transcript to understand the tone of the video.
- **🗂️ Topic Modeling**: Identify and display the main topics discussed in the video.
- **⏰ Key Moments**: Highlight important timestamps and key moments from the video.
- **🔑 Keyword Extraction**: Extract and display significant keywords from the transcript.
- **🌟 Word Cloud Visualization**: Generate and visualize a word cloud from the transcript.
- **📄 PDF and Text Download**: Download the summary, word cloud, and other details in PDF and text formats.

## 🚀 Getting Started

### 📋 Prerequisites

Before running the application, ensure you have the following:

- Python 3.x installed
- Required Python packages (listed below)
- YouTube Data API v3 key
- Google Gemini API key

### 💻 Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/sriramkrish68/notes-from-youtube-video.git
   cd youtube-notes-maker
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables:**
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   YOUTUBE_API_KEY=your_youtube_api_key
   ```

### ⚙️ Usage

1. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

2. **Interact with the App:**
   - Enter a YouTube video link to get started.
   - Select the desired summary length.
   - Click "Get Detailed Notes" to generate and view the summary, sentiment analysis, topic modeling, key moments, keywords, and word cloud.

### 📝 Download Options

- **Download as PDF**: Get a detailed PDF summary of the video.
- **Download as Text**: Obtain a plain text summary.
- **Download Word Cloud**: Save the word cloud image.

## 📦 Dependencies

The application relies on the following Python packages:

- `streamlit` - For building the web interface
- `dotenv` - For loading environment variables
- `google-api-python-client` - For YouTube Data API integration
- `google-generativeai` - For Google Gemini API integration
- `youtube-transcript-api` - For extracting YouTube transcripts
- `textblob` - For sentiment analysis
- `sklearn` - For topic modeling and keyword extraction
- `wordcloud` - For generating word clouds
- `fpdf` - For PDF generation
- `matplotlib` - For word cloud visualization

### 🖥️ Example

Here’s how the summary and additional features might look:

![Page Screenshots](https://drive.google.com/file/d/1oeVFzROk3xODJ6upN8Xs5FToB5IDB_EX/view?usp=sharing)

## 🔧 Troubleshooting

- **Permission Error on Windows**: Ensure that files are properly closed before deletion. Restart the app or your system if you encounter file access issues.
- **Module Not Found**: Install missing packages using `pip install <package_name>`.
