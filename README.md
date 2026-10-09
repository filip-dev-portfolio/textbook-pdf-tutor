# 📚 PDF Tutor — Local AI-Powered Textbook Assistant

A local AI-powered application that lets you upload textbooks in PDF format and ask questions about their contents. Built with Python, Streamlit, FAISS, Sentence Transformers, and Ollama.

The project combines Retrieval-Augmented Generation (RAG) with locally running language models to answer questions using retrieved textbook passages, with source-page references to help users verify the answers.

Beyond building a useful application, this project is my hands-on journey into machine learning, LLM engineering, semantic search, and evaluation of AI systems.

## ✨ Features

### Currently implemented
 - **PDF ingestion** — Extract text and page numbers from PDF files using PyMuPDF.
 - **Text chunking** — Split extracted text into manageable chunks while preserving page metadata and filtering repeated headers and footers.
 - **Semantic embeddings** — Convert textbook chunks into numerical vector representations using Sentence Transformers.
 - **Vector search** — Retrieve relevant passages using FAISS.
 - **Local LLM inference** — Generate answers using Qwen3 8B through Ollama.
 - **Grounded question answering** — Prompt the LLM to answer using retrieved textbook context rather than outside knowledge.
 - **Source references** — Provide source labels and page references to help users trace answers back to the textbook.
 - **Persistent textbook library** — Store uploaded PDFs and their processed data locally for reuse.
 - **Interactive web interface** — Upload textbooks, select existing books, ask questions, configure retrieval depth, and inspect retrieved sources.
### Planned features
 - Improved citation accuracy and answer-grounding evaluation.
 - Quantitative retrieval evaluation using Recall@k, Precision@k, and Mean Reciprocal Rank (MRR).
 - Experiments with embedding models, similarity metrics, chunk sizes, and retrieval strategies.
 - Token-aware and structure-aware chunking.
 - Automatic question generation from textbook content.
 - Interactive quizzes with explanations and source references.
 - Interview-preparation mode with follow-up questions, hints, and feedback.
 - Performance experiments involving GPU inference, batching, quantization, and memory usage.

## 🏗️ Architecture

The application follows a modular Retrieval-Augmented Generation architecture.
 ```text
                   TEXTBOOK INGESTION

PDF textbook
     |
     v
PyMuPDF extraction
     |
     v
Page text + metadata
     |
     v
Text cleaning and chunking
     |
     v
Sentence Transformers
(all-MiniLM-L6-v2)
     |
     v
Vector embeddings
     |
     v
FAISS + persisted data


                    QUESTION ANSWERING

User question
     |
     v
Embed the question
     |
     v
FAISS similarity search
     |
     v
Retrieve top-k chunks
     |
     v
Construct prompt with context
     |
     v
Qwen3 8B via Ollama
     |
     v
Generated answer + source references
 ```

## How RAG works in this project

**1. Retrieval**

The embedding model converts the question into a vector. FAISS searches the stored textbook vectors and returns the nearest chunks.

**2. Context construction**

The retrieved passages are formatted with source labels and page numbers, then combined into a context string.

**3. Generation**

The question, retrieved context, and instructions are passed to Qwen3 8B through Ollama.

**4. Answer and sources**

The application displays the generated answer alongside the retrieved source pages.

The retriever finds candidate evidence; the LLM interprets that evidence and generates the response. The current implementation uses prompt instructions to encourage grounded answers, but factual correctness and citation accuracy still need systematic evaluation.

## 🧰 Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language | Python | Application logic |
| Web Interface | Streamlit | Interactive user interface |
| PDF Processing | PyMuPDF | Text extraction and page metadata |
| Embeddings | Sentence Transformers | Semantic vector representations |
| Embedding Model | `all-MiniLM-L6-v2` | Text and query embeddings |
| Vector Search | FAISS (`IndexFlatL2`) | Nearest-neighbor retrieval |
| Local LLM Runtime | Ollama | Local model inference |
| Generation Model | `qwen3:8b` | Textbook question answering |
| Numerical Processing | NumPy | Embedding arrays |
| Testing | pytest | Automated testing |


The project currently uses normalized embeddings and L2-distance search. The retrieval configuration will be evaluated experimentally rather than assumed to be optimal.

## 💻 Hardware and Local Execution

The project is developed and tested on the following setup:

 - **Operating system:** Windows
 - **RAM:** 64 GB
 - **GPU:** NVIDIA RTX 5070 with 8 GB VRAM
 - **Python environment:** .venv
 - **LLM runtime:** Ollama

The goal is to keep the application local and minimize external service dependencies.

Actual GPU utilization depends on model size, quantization, context length, and the available VRAM. Some workloads may use system RAM or CPU resources as well.

Copy this directly into your `README.md` file:

markdown
````

## 🚀 Getting Started

### Prerequisites

Install the following tools before getting started:

- **Python**
- **Git**
- **Ollama**

An NVIDIA GPU is optional but useful for accelerating supported workloads.

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd pdf-tutor
```

Replace `<YOUR_REPOSITORY_URL>` with your Git repository URL.

### 2. Create and Activate a Virtual Environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

Upgrade `pip` and install the required packages:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Note:** PyTorch and CUDA compatibility depends on the installed Python version, GPU drivers, and package versions. If GPU support is unavailable, follow the appropriate [PyTorch installation instructions](https://pytorch.org/get-started/locally/).

### 4. Download the Language Model

Make sure Ollama is installed and running, then download the required model:

```bash
ollama pull qwen3:8b
```

Verify that the model is available:

```bash
ollama list
```

### 5. Start the Application

From the project root directory, run:

```bash
streamlit run app/main.py
```

Open the local URL displayed in the terminal, usually:

**http://localhost:8501**
````

6. Upload a textbook
Select Upload new textbook.
Choose a PDF file.
Wait for text extraction, chunking, embedding generation, and persistence to complete.
Select an existing textbook from the library when needed.
Enter a question and click Ask.
Inspect the answer and its source references.

The first ingestion of a textbook generates its embeddings. Previously processed textbooks are intended to reuse their saved data instead of being embedded again every time the application starts.

📂 Project Structure
pdf-tutor/
│
├── app/
│   ├── main.py             # Streamlit interface and orchestration
│   ├── pdf_processor.py    # PDF text extraction
│   ├── chunker.py           # Text cleaning and chunking
│   ├── embeddings.py        # Embedding generation
│   ├── retriever.py         # Similarity search and retrieval
│   ├── vector_store.py      # Embedding and chunk persistence
│   ├── llm.py               # Ollama LLM interface
│   ├── rag.py               # RAG prompt construction and answering
│   ├── ingestion.py         # PDF ingestion pipeline
│   ├── textbook_store.py    # Textbook library management
│   └── quiz.py              # Quiz functionality and experiments
│
├── tests/
│   └── test_pdf_processor.py
│
├── scripts/
│   └── inspect_pdf.py
│
├── notebooks/               # Experiments and exploration
│
├── data/
│   └── textbooks/           # Local textbook data
│
├── requirements.txt
├── README.md
└── .gitignore

🗃️ Local Data Storage

Each textbook is stored in its own directory under data/textbooks/.

A typical textbook directory contains:

data/textbooks/
└── educational_psychology/
    ├── textbook.pdf
    ├── chunks.json
    └── embeddings.npy

textbook.pdf — the original uploaded PDF.
chunks.json — extracted chunks and their metadata.
embeddings.npy — the numerical vector representations of the chunks.

The relationship between embeddings and chunks must remain consistent:

embeddings[317]  <---->  chunks[317]


If embeddings are regenerated, the associated vector data must be updated consistently.

Embedding model compatibility: all chunks and user queries for a given textbook must use the same embedding model. Changing the embedding model requires regenerating that textbook's embeddings and rebuilding its search index, even if the new model outputs vectors with the same dimensions.

Textbook data is local application data and should be backed up separately if needed.

🧠 Key Engineering Concepts

This project is also a practical learning environment for understanding the internals of modern AI applications.

Embeddings and semantic search

Text is converted into vectors so semantically related passages can be retrieved even when the query and source passage use different wording.

Vector similarity

FAISS currently uses IndexFlatL2, which performs exact nearest-neighbor search using squared L2 distance. Because embeddings are normalized, the relationship between L2 distance and cosine similarity can be investigated experimentally.

Retrieval-Augmented Generation

RAG supplies retrieved external context to an LLM at inference time. This can improve the relevance and traceability of answers, but it does not guarantee that every generated claim is correct.

Chunking and context windows

Chunk size and boundaries influence what information is available during retrieval and generation. The current chunker uses character-based limits, which leaves room for future experiments with token-aware and document-structure-aware strategies.

Evaluation

A working demonstration is not sufficient to establish retrieval or answer quality. The next stage is to build a benchmark of questions, expected answers, and expected source chunks or pages, then compare configurations using repeatable measurements.

🧪 Development Roadmap

The project is being developed incrementally, prioritizing understanding and measurable improvements.

PDF text extraction with page metadata
Initial text cleaning and chunking
Embedding generation and persistence
FAISS vector retrieval
Local LLM integration with Ollama
Basic RAG question answering
Source labels and page references
Local textbook storage and selection
Basic Streamlit upload and question-answering workflow
Improve citation reliability and inspect prompts
Build a small retrieval evaluation dataset
Measure Recall@k, Precision@k, and MRR
Compare cosine similarity and L2-distance retrieval
Experiment with chunk size, overlap, and chunk boundaries
Compare embedding models using the same evaluation dataset
Evaluate answer correctness and groundedness
Build textbook-based question generation
Add interactive quizzes and scoring
Develop an interview-preparation mode
Measure GPU memory usage, inference latency, and quantization trade-offs
🎯 Project Goals

The main goals are to:

Build a useful local AI application from understandable components.
Learn the fundamentals of embeddings, vector search, RAG, and LLM inference.
Understand GPU inference, memory constraints, batching, and quantization.
Evaluate retrieval and generation with repeatable experiments.
Develop practical ML/AI engineering skills and a portfolio project suitable for technical discussions and interviews.
🔒 Privacy and Limitations
The application is designed for local processing through its current components.
Uploaded textbooks and generated embedding files are stored locally.
Ollama runs the language model locally; the application does not require a hosted LLM API for its current generation pipeline.
Model downloads and Python package installation require internet access initially.
Answers may contain incorrect claims or citations, even when the prompt requests textbook-only responses.
Retrieval quality depends on PDF text quality, chunking, the embedding model, and the search configuration.
Scanned PDFs may require OCR, which is not currently guaranteed by the text-extraction pipeline.

Use textbooks and other documents only when you have the appropriate rights to process and store them.

📖 Learning Philosophy

The project deliberately starts with simple Python implementations rather than relying on a large RAG framework.

Each improvement should follow this cycle:

Understand → Implement → Experiment → Evaluate → Improve

The aim is not only to build an application that works, but to understand why it works, where it fails, and how to improve it based on evidence.

Built as a hands-on learning project in local LLMs, machine learning, and AI engineering.
