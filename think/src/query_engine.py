import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class StudentQueryEngine:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        self.client = Groq(api_key=api_key)

    def analyze_query(self, query: str) -> dict:
        """
        Analyzes the student's query to determine intent, topic, and difficulty.
        """
        prompt = f"""
        Analyze the following student query and classify it into:
        1. Intent type (Explanation, Example, Doubt clarification, Revision)
        2. Topic (e.g., Optimization, Neural Networks, Backpropagation, etc.)
        3. Difficulty level (Beginner, Intermediate, Advanced)

        Query: "{query}"

        Return the result strictly as a valid JSON object with keys: "intent", "topic", "difficulty_level".
        Do not include markdown formatting or extra text.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant that classifies student queries in an EdTech context. Output only JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile", # Using a supported model
                response_format={"type": "json_object"},
            )
            
            result = chat_completion.choices[0].message.content
            return json.loads(result)
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    # Test
    engine = StudentQueryEngine()
    print(engine.analyze_query("I don't understand backpropagation."))
