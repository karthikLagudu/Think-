# AI-Powered Teaching Assistant

**Problem Statement 1 (AU Campus Recruitment 2026)**

This project implements an AI-powered teaching assistant focusing on **Student Query Understanding** and **Adaptive Learning Path Recommendation**. It simulates how an EdTech platform adapts learning based on student interactions.

## Features

### 1. Student Query Understanding (Q1)
*   **Input:** Natural language student questions (e.g., "I don't understand backpropagation").
*   **Output:** Structured JSON containing:
    *   **Intent:** (Explanation, Example, Doubt clarification, Revision)
    *   **Topic:** (e.g., Optimization, Neural Networks)
    *   **Difficulty:** (Beginner, Intermediate, Advanced)
*   **Technique:** Uses LLM (Llama-3.3-70b via Groq) for advanced semantic understanding and intent classification.

### 2. Adaptive Learning Path Recommendation (Q2)
*   **Input:** Student performance state (Quiz scores, Attempts, Time spent).
*   **Output:** Recommendation for the next step:
    *   **Next Topic:** Logical progression or revision.
    *   **Action:** (Revision, Practice, Next Topic).
    *   **Difficulty Adjustment:** (Increase, Decrease, Same).
*   **Technique:** Hybrid logic combining curriculum rules with LLM reasoning to simulate a personalized tutor.

## Project Structure

```
├── data/
│   └── synthetic_data_generator.py  # Generates realistic student interaction logs
├── src/
│   ├── query_engine.py              # Logic for intent & topic classification
│   └── adaptive_engine.py           # Logic for personalized recommendations
├── main.py                          # CLI interface to run the assistant
├── requirements.txt                 # Python dependencies
└── video_script.md                  # Script for the submission demo video
```

## Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Setup:**
    *   Create a `.env` file in the root directory.
    *   Add your Groq API Key:
        ```
        GROQ_API_KEY=your_api_key_here
        ```

## Usage

### Run the Web Interface (Interactive Mode)

To launch the interactive Streamlit dashboard:

```bash
streamlit run app.py
```

### Run the CLI (Command Line Mode)

Run the main application:

```bash
python main.py
```

### Options:
1.  **Test Student Query Understanding:** Enter a custom question to see the classification.
2.  **Test Adaptive Learning Path:** Manually input student metrics (score, attempts) to receive a recommendation.
3.  **Simulate Batch Recommendations:** Process the synthetic dataset (`data/student_interactions.csv`) to see the system handling multiple students.

## Approach & Design

*   **Modular Architecture:** Separation of concerns between query understanding and adaptive logic.
*   **Data-Driven:** Includes a synthetic data generator to simulate realistic student behaviors for testing.
*   **Explainable AI:** The system provides structured, human-readable reasons for every decision (via the `action` and `difficulty_adjustment` fields).

## License
MIT
