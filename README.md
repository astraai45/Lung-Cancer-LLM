# Lung-Cancer-LLM

Sure! Here's a similar GitHub README tailored for your "Lung Disease Multilingual PDF Chatbot with Voice Support" project.

````markdown
# Lung Disease Multilingual Chatbot with Voice Support 💬

This project provides a multilingual chatbot that helps users understand and interact with PDF documents related to lung diseases. With support for voice input, the chatbot processes the uploaded PDFs, retrieves relevant information, and delivers it in a user-friendly, multilingual format.

## Features
- **Voice Input Support:** Users can record and speak their queries to interact with the chatbot.
- **Multilingual Responses:** The chatbot can respond in various languages, including English, Spanish, French, German, Hindi, Telugu, and Tamil.
- **PDF Document Processing:** The chatbot processes and extracts text from uploaded PDF documents, allowing users to ask questions based on the content of the document.
- **Customizable User Interaction:** Choose the language for the chatbot responses and enable/disable voice input.

## Technologies Used
- **Streamlit** for building the web interface.
- **Langchain** for handling NLP tasks and querying vector-based embeddings.
- **Ollama** for embeddings and LLM (Language Model).
- **Chroma** for vector storage and retrieval.
- **PyPDF2** for extracting text from PDFs.
- **Deep Translator (Google Translate)** for language translation support.
- **SpeechRecognition** for transcribing voice input to text.
- **audio_recorder_streamlit** for recording voice input directly in the browser.
- **Python's Temporary Files** for processing and storing data during the session.

## Installation

### Clone the Repository
```bash
git clone https://github.com/yourusername/lung-disease-chatbot.git
cd lung-disease-chatbot
````

### Install Dependencies

Make sure you have Python 3.8+ installed. Install the necessary libraries using:

```bash
pip install -r requirements.txt
```

### Setup Ollama LLM (Language Model)

1. Install [Ollama](https://ollama.ai/) and make sure the model (`tinyllama`) is running locally.
2. To install Ollama, visit [ollama.ai](https://ollama.ai/), download the tool, and follow the installation instructions.
3. After installation, run the following command to start the server:

   ```bash
   ollama serve
   ```

### Set up the PDF Loader

Ensure your PDF files are accessible when uploading to the web app.

## Usage

### Running the Application

To start the chatbot, run the following command:

```bash
streamlit run app.py
```

This will open the web application at `http://localhost:8501`, where you can upload your PDF files and interact with the chatbot.

### Uploading PDF Document

* You can upload any PDF file related to lung diseases (e.g., research papers, medical history, etc.).
* The chatbot will process the document and allow you to ask questions about its content.

### Voice Input

* Enable voice input via the checkbox in the sidebar and speak your queries.
* The system will transcribe your voice into text and process it.

### Language Selection

* The chatbot supports multiple languages: English, Spanish, French, German, Hindi, Telugu, and Tamil.
* You can select the desired language for the response in the sidebar.

### Chat Interaction

* You can type or speak your queries, and the chatbot will respond with information extracted from the PDF.
* The chatbot will translate responses to your selected language (if necessary) using Google Translate.

## Contribution

Feel free to fork the repository and submit a pull request if you want to contribute to the project. Contributions, suggestions, and improvements are always welcome!

### Contributors
* [Pavan Balaji](https://github.com/pavanbalaji45)
* [Balaji Kartheek](https://github.com/Balaji-Kartheek)



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

### Notes for the README:
1. Replace `yourusername`, `contributor1`, and `contributor2` with the actual GitHub usernames of the contributors.
2. Include a `requirements.txt` file that contains all the required Python libraries for the project.

The rest of the content in the README explains how to set up and use the application, including uploading PDFs, enabling voice input, and choosing a language for responses. Let me know if you need any other specific changes!
```
