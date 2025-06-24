import streamlit as st
from PyPDF2 import PdfReader
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from deep_translator import GoogleTranslator
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import tempfile
import os
import shutil

# Setup Streamlit Page
st.set_page_config(page_title="Multilingual PDF Chatbot", page_icon="💬", layout="wide")
st.title("💬 Multilingual PDF Chatbot with Voice Support")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False
if "persist_dir" not in st.session_state:
    st.session_state.persist_dir = None

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    
    # Language selection
    language = st.selectbox(
        "Response Language:",
        ["English", "Spanish", "French", "German", "Hindi", "Telugu", "Tamil"],
        index=0
    )
    
    # Voice input toggle
    voice_enabled = st.checkbox("Enable Voice Input")
    
    # File uploader in sidebar
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# Check if Ollama is running
try:
    test_llm = Ollama(model="tinyllama:latest")
    test_response = test_llm("test")  # Simple test query
    if not test_response:
        st.error("Ollama server responded with empty response")
        st.stop()
except Exception as e:
    st.error(f"Failed to connect to Ollama server. Please make sure Ollama is installed and running.\nError: {e}")
    st.info("To install Ollama, visit: https://ollama.ai/")
    st.info("After installation, run: `ollama serve` in your terminal")
    st.stop()

# Function to translate text
def translate_text(text, target_lang):
    lang_map = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Hindi": "hi",
        "Telugu": "te",
        "Tamil": "ta"
    }
    
    if target_lang == "English" or not text:
        return text
    
    try:
        translated = GoogleTranslator(source='auto', target=lang_map[target_lang]).translate(text)
        return translated
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return text

# Function to process PDF and create vector store
def process_pdf(uploaded_file):
    try:
        # Create persistent directory for ChromaDB
        if st.session_state.persist_dir:
            try:
                shutil.rmtree(st.session_state.persist_dir)
            except:
                pass
        
        st.session_state.persist_dir = tempfile.mkdtemp(prefix="chroma_")
        
        # Save uploaded file temporarily
        temp_pdf_path = os.path.join(st.session_state.persist_dir, "uploaded.pdf")
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Read PDF
        reader = PdfReader(temp_pdf_path)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        if not text.strip():
            st.error("The PDF appears to be empty or contains no extractable text")
            return None

        # Save text to temp file
        temp_txt_path = os.path.join(st.session_state.persist_dir, "extracted_text.txt")
        with open(temp_txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        # Load the text
        loader = TextLoader(temp_txt_path)
        documents = loader.load()

        # Embedding and VectorDB
        embeddings = OllamaEmbeddings(model="tinyllama:latest")
        vectordb = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=st.session_state.persist_dir
        )
        
        # Explicitly persist the database
        vectordb.persist()
        
        return vectordb
    
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

# Voice recording and transcription
def transcribe_audio(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
            tmp_audio.write(audio_bytes)
            audio_path = tmp_audio.name
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        
        os.unlink(audio_path)
        return text
    except sr.UnknownValueError:
        st.error("Could not understand audio. Please try again.")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return None

# Main application logic
if uploaded_file and not st.session_state.pdf_processed:
    with st.spinner("Processing PDF... This may take a moment depending on the file size."):
        st.session_state.vector_store = process_pdf(uploaded_file)
        if st.session_state.vector_store:
            st.session_state.pdf_processed = True
            st.success("PDF processed successfully! You can now ask questions.")
        else:
            st.session_state.pdf_processed = False

if st.session_state.pdf_processed and st.session_state.vector_store:
    try:
        # Verify the vector store is still accessible
        if not os.path.exists(st.session_state.persist_dir):
            raise Exception("Vector store database not found")
        
        # Setup Retriever and QA Chain
        retriever = st.session_state.vector_store.as_retriever()
        llm = Ollama(model="tinyllama:latest")
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff"
        )

        # Display previous chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Get user input (text or voice)
        user_input = ""
        
        if voice_enabled:
            st.write("Click the microphone to record your question (press stop when finished):")
            audio_bytes = audio_recorder(
                pause_threshold=3.0,
                text="",
                recording_color="#e8b62c",
                neutral_color="#6aa36f",
                icon_size="2x",
            )
            
            if audio_bytes:
                with st.spinner("Transcribing audio..."):
                    user_input = transcribe_audio(audio_bytes)
                    if user_input:
                        st.success(f"Transcribed: {user_input}")
        else:
            user_input = st.chat_input("Ask something about the PDF...")

        if user_input:
            # Save user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # Generate bot response
            with st.spinner("Generating response..."):
                try:
                    response = qa.run(user_input)
                    if not response:
                        response = "I couldn't generate a response. Please try again."
                    
                    translated_response = translate_text(response, language)
                    
                    # Format response with translation note if needed
                    if language != "English":
                        final_response = f"{translated_response}\n\n*(Translated from English to {language})*"
                    else:
                        final_response = response

                    # Save bot message
                    st.session_state.messages.append({"role": "assistant", "content": final_response})
                    with st.chat_message("assistant"):
                        st.markdown(final_response)
                        
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
    
    except Exception as e:
        st.error(f"Database access error: {str(e)}")
        st.session_state.pdf_processed = False
        st.session_state.vector_store = None
        if st.session_state.persist_dir and os.path.exists(st.session_state.persist_dir):
            try:
                shutil.rmtree(st.session_state.persist_dir)
            except:
                pass
        st.session_state.persist_dir = None
        st.info("Please upload the PDF again to restart the session.")

elif not uploaded_file:
    st.info("Please upload a PDF file to start chatting.")