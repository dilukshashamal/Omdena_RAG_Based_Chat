# Omdena RAG-Based Chatbot

This repository contains a FastAPI-based backend for a Retrieval-Augmented Generation (RAG) chatbot. The application allows users to interact with AI, upload documents for indexing, and manage indexed documents.

---

## **Overview**

The application includes the following features:

1. **Chat Functionality**: Processes user queries, retrieves relevant documents, and provides AI-generated responses using a retrieval-augmented generation (RAG) chain.
2. **Document Uploading and Indexing**: Allows users to upload documents in `.pdf`, `.docx`, and `.html` formats. These documents are indexed for efficient retrieval during chats.
3. **Document Management**: Supports listing all uploaded documents and deleting specific documents by file ID.
4. **Logging**: Logs all user interactions, responses, and system events into `app.log`.

---

## **API Setup Instructions**

### **Clone the Repository**
```bash
git clone https://github.com/dilukshashamal/Omdena_RAG_Based_Chat.git
cd Omdena_RAG_Based_Chat/api
```

### **Configure Environment Variables**

Rename example.env to .env:
```bash
mv example.env .env
Open .env and add your OpenAI API key:
```
set open ai api
```bash
OPENAI_API_KEY=your_openai_api_key
```

### **Install Dependencies**
Ensure you have Python 3.8 or above installed, then run:

```bash
pip install -r requirements.txt
```

### **Run the Application**
Start the FastAPI application:

```bash
python main.py
```

## **APP Setup Instructions**

### **Change Directory**
```bash
cd Omdena_RAG_Based_Chat/app
```
### **Run the Application**

```bash
python streamlit_app.py
```

## **Functions**

### **1. `/chat`**
- **Method**: POST  
- **Purpose**: Handles user chat queries.  
- **Parameters**:  
  - `QueryInput` (Pydantic model): Includes the session ID, user question, and the AI model to use.  
- **Steps**:  
  1. Retrieves the chat history for the session.  
  2. Initializes a RAG chain using the selected model.  
  3. Invokes the chain with the query and chat history to get the AI's response.  
  4. Logs the session details, query, and response.  
  5. Returns the AI's response along with the session ID and model used.  

---

### **2. `/upload-doc`**
- **Method**: POST  
- **Purpose**: Allows users to upload a document for indexing.  
- **Parameters**:  
  - `file`: The uploaded document.  
- **Steps**:  
  1. Validates the file type (only `.pdf`, `.docx`, `.html` are allowed).  
  2. Saves the file temporarily.  
  3. Inserts a record for the document in the database and indexes the document using ChromaDB.  
  4. If indexing fails, removes the document record from the database.  
- **Response**: Success or failure message with the document’s file ID.  

---

### **3. `/list-docs`**
- **Method**: GET  
- **Purpose**: Lists all documents indexed in the system.  
- **Response**:  
  - A list of `DocumentInfo` objects (Pydantic model) containing document metadata.  

---

### **4. `/delete-doc`**
- **Method**: POST  
- **Purpose**: Deletes a document from the system.  
- **Parameters**:  
  - `DeleteFileRequest` (Pydantic model): Contains the file ID of the document to delete.  
- **Steps**:  
  1. Attempts to delete the document from ChromaDB.  
  2. If successful, deletes the document from the database.  
  3. Returns a success or error message.  


