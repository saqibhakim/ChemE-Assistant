# 🧪 ChemE Assistant

An AI-powered Chemical Engineering assistant built using LangChain, OpenRouter, FAISS, and Streamlit.

## Features

- 📄 Upload Chemical Engineering PDFs
- 🔍 Semantic search using FAISS embeddings
- 🤖 AI-powered question answering
- 💬 Context-aware conversations
- 🧮 LaTeX support for equations
- 📚 Supports research papers, notes, and textbooks

## Tech Stack

- Python
- Streamlit
- LangChain
- OpenRouter
- OpenAI Embeddings
- FAISS
- Unstructured API

## Project Structure

```
ChemE_Assistant/
│
├── frontend.py
├── main.py
├── Ingest.py
├── prompts.py
├── st.py
├── README.md
├── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/saqibhakim/ChemE-Assistant.git
cd ChemE-Assistant
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
OPENROUTER_API_KEY=your_key
UNSTRUCTURED_API_KEY=your_key
```

Run the app:

```bash
streamlit run frontend.py
```

## Future Improvements

- OCR support
- Image understanding
- Multiple document collections
- Better citations
- Cloud deployment

## Author

**Saqib Hakim**