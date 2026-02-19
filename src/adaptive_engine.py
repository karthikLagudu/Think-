import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AdaptiveLearningEngine:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        self.client = Groq(api_key=api_key)

    def recommend_path(self, student_state: dict) -> dict:
        """
        Recommends the learning path based on student performance using an LLM.
        
        Args:
            student_state (dict): Contains 'quiz_score', 'attempts', 'time_spent', 'last_topic'.
            
        Returns:
            dict: { "next_topic": str, "action": str, "difficulty_adjustment": str }
        """
        prompt = f"""
        Analyze the following student state and recommend the next learning step.
        
        Student State:
        - Last Topic: {student_state.get('last_topic', 'Unknown')}
        - Quiz Score: {student_state.get('quiz_score', 0)}
        - Attempts: {student_state.get('attempts', 1)}
        - Time Spent: {student_state.get('time_spent_minutes', 'Unknown')} minutes

        Available Topics (Curriculum Order):
        1. Linear Regression
        2. Gradient Descent
        3. Neural Networks
        4. Backpropagation
        5. Optimization Algorithms
        6. CNNs
        7. RNNs

        Rules:
        - If Score < 50: Action=Revision, Difficulty=Decrease, Next Topic=Same as Last Topic
        - If 50 <= Score < 80: Action=Practice, Difficulty=Same, Next Topic=Same as Last Topic or Advanced Concepts
        - If Score >= 80: Action=Next Topic, Difficulty=Increase, Next Topic=Next logical topic in curriculum

        Return the result strictly as a valid JSON object with keys: "next_topic", "action", "difficulty_adjustment".
        Do not include markdown formatting or extra text.
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI academic advisor. Output only JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
            )
            
            result = chat_completion.choices[0].message.content
            return json.loads(result)
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    engine = AdaptiveLearningEngine()
    state = {
        "quiz_score": 45,
        "attempts": 3,
        "last_topic": "Backpropagation"
    }
    print(engine.recommend_path(state))
