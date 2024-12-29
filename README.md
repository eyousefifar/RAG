# FastAPI-Based RAG System for Document Indexing and Query Answering

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** system that enables efficient document indexing and querying. The system is built using FastAPI, leveraging the capabilities of the Qwen 2.5 instruct model, hosted via Ollama. Users can index documents or plain text, query them with natural language, and receive AI-generated answers augmented by the indexed content.

---

## Prerequisites

1. **Install Ollama**  
   Ensure Ollama is installed on your system to serve the Qwen 2.5 instruct model.  

2. **Download the Model**  
   Obtain and host the `qwen2.5b-instruct-fp16` model. Use Ollama's CLI to download and set it up.

---

## Setup and Usage

### Using Docker Compose  
Run the following command to start the project using Docker Compose:  
```bash
docker-compose -f docker-compose.yaml up
```

### Manual Setup  
Alternatively, you can manually install the requirements and run the application:  
1. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```  
2. **Run the FastAPI app**  
   ```bash
   fastapi dev app/main,py
   ```

---

## API Endpoints

- **Swagger Documentation**: Accessible at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).  
  It provides a user-friendly interface for testing the API.  

### Key Endpoints
1. **Document Indexing**:
   - **POST** `/index-doc`: Upload a document file for indexing.
   - **POST** `/index-text`: Submit plain text for indexing.

2. **Query Answering**:
   - **POST** `/query`: Submit a query and receive an AI-generated answer using the indexed documents.

3. **Logs**:
   - **GET** `/logs`: Fetch logs of queries and responses.

4. **Health Check**:
   - **GET** `/health`: Verify API health and status.

---

## Explanation of Key Features

### Document Indexing  
Document pre processing is the main way of improving RAG result. 
For PDf files I have tested ColPoli and got the best result ( but not the best performance )
For text I used Qdrant and BM25 and Colbert 
in this test I implemented a simple embedding search due to time constraints

### Retrieval-Augmented Generation Evaluation (RAG)  
These will be the steps to evaluate RAG application, when you don't have the dataset

1. Gather corpus.
2. Use LLM to create a QA pairs on the data and answer the question based on the data
 2.1. Create a question on the data chunk
 2.2 answer that question using the chunk
 2.3 reflect on accuracy
3. once the QA is generated and we have a data set as ground truth, we can generate question and use the RAG system to answer them
4. use similarity and LLM as Judge to score the rag system
