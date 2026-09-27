# Parking Space Reservation Chatbot - Stage 1: RAG System

## 📌 Overview
This repository contains the implementation of **Stage 1** of the Intelligent Parking Space Reservation Chatbot. It features a Retrieval-Augmented Generation (RAG) architecture designed to interact with users, provide parking information, and collect reservation details while ensuring data privacy through NLP guardrails.

## 🏗️ Architecture
The system uses a hybrid data approach:
- **Static Data (Vector Database):** FAISS is used to store and retrieve general information, location, and booking processes.
- **Dynamic Data (SQL Database):** SQLite is used to store and retrieve real-time data such as working hours, prices, and space availability.
- **Guardrails:** Microsoft Presidio (NLP) is integrated to detect and mask sensitive user data (PII) before and after LLM processing.

## 📂 Project Structure
```text
├── app/                  # FastAPI application
├── core/                 # RAG Agent and Configuration
├── database/             # SQLite and FAISS implementations
├── guardrails/           # PII detection and masking
├── evaluation/           # RAG performance metrics (Recall@K, Precision)
├── tests/                # Unit tests for all modules
└── .github/workflows/    # CI/CD pipeline