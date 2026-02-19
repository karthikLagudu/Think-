# AI-Powered Teaching Assistant - Technical Documentation

**Submitted by:** [Karthik Lagudu]
**Problem Statement:** 1 (AI-Powered Teaching Assistant)

---

## 1. Approach Explanation

The solution is designed as a modular system with two primary engines:

1.  **Student Query Understanding (Q1):**
    *   **Goal:** To interpret natural language questions and extract intent, topic, and difficulty.
    *   **Method:** We utilize a Large Language Model (LLM) prompts engineered to act as an educational classifier. Instead of relying solely on keyword matching or separate BERT embeddings, the LLM provides contextual understanding, able to differentiate between a student asking for an "Explanation" vs. an "Example".

2.  **Adaptive Learning Path Recommendation (Q2):**
    *   **Goal:** To recommend the next logical step based on student performance.
    *   **Method:** A hybrid approach combining rule-based logic (curriculum sequencing) with LLM reasoning. The system evaluates metrics (Score, Attempts, Time) against pedagogical rules to determine if a student needs revision or advancement.

---

## 2. Dataset Source & Generation

**Source:** Synthetic Data Generation (Self-generated)
**Reason:** No public dataset was provided that perfectly matched the multi-turn interaction required for adaptive learning paths.

**Generation Logic:**
*   A Python script (`data/synthetic_data_generator.py`) simulates student interactions.
*   **Fields:** `student_id`, `topic`, `quiz_score` (Normal distribution centered at 70), `attempts` (correlated inversely with score), `time_spent`, `last_asked_intent`.
*   **Volume:** Configurable, defaulting to 100 students with 5-20 interactions each.
*   **Privacy:** The data is entirely synthetic and contains no PII (Personally Identifiable Information).

---

## 3. Model Architecture

**Core Model:** Llama-3.3-70b-versatile (via Groq API)

### Schema:
*   **Input:** Natural Language Query OR Student State Dictionary.
*   **Processing:**
    *   **System Prompt:** Defines the persona (e.g., "You are an AI academic advisor").
    *   **User Prompt:** Wraps the input with specific constraints (e.g., "Output only JSON", "Classify into...").
*   **Output:** Structured JSON.

### Flow:
1.  User Input -> `main.py`
2.  `main.py` -> `StudentQueryEngine.analyze_query()` -> LLM -> JSON
3.  `main.py` -> `AdaptiveLearningEngine.recommend_path()` -> LLM -> JSON

---

## 4. Assumptions and Limitations

**Assumptions:**
*   The student is studying a fixed curriculum (Linear Regression -> ... -> RNNs).
*   Quiz scores are the primary metric for understanding.
*   The API availability is constant.

**Limitations:**
*   **Dependency on LLM:** The system requires an active internet connection to query the Groq API.
*   **Statelessness:** The current implementation processes each request independently (though the batch processor simulates history). A production version would require a persistent database.
*   **Curriculum Scope:** The current topic list is hardcoded for the demo.

---

## 5. Sample Outputs

### Q1: Student Query Understanding
**Input:** "I don't understand backpropagation."
**Output:**
```json
{
  "intent": "Explanation",
  "topic": "Backpropagation",
  "difficulty_level": "Intermediate"
}
```

### Q2: Adaptive Learning Path
**Input:**
*   Score: 45
*   Attempts: 3
*   Last Topic: "Backpropagation"

**Output:**
```json
{
  "next_topic": "Backpropagation",
  "action": "Revision",
  "difficulty_adjustment": "Decrease"
}
```

---

## 6. System Design

*   **Modular Codebase:**
    *   `src/`: Contains the intelligence engines.
    *   `data/`: Handles data generation.
    *   `main.py`: Entry point.
*   **Scalability:** The use of class-based engines allows for easy integration into a web backend (Flask/FastAPI) in future iterations.
