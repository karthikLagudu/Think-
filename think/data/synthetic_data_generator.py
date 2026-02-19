import pandas as pd
import numpy as np
import random

def generate_student_data(num_students=100):
    topics = ["Linear Regression", "Gradient Descent", "Neural Networks", "Backpropagation", "Optimization Algorithms", "CNNs", "RNNs"]
    intents = ["Explanation", "Example", "Doubt clarification", "Revision"]
    
    data = []
    
    for student_id in range(1, num_students + 1):
        # Simulate a sequence of interactions
        num_interactions = random.randint(5, 20)
        
        for _ in range(num_interactions):
            topic = random.choice(topics)
            score = np.random.normal(loc=70, scale=15) # Mean 70, SD 15
            score = max(0, min(100, score)) # Clip to 0-100
            
            attempts = 1
            if score < 60:
                attempts = random.randint(1, 4)
                
            time_spent = random.randint(5, 60) # Minutes
            
            data.append({
                "student_id": student_id,
                "topic": topic,
                "quiz_score": round(score, 2),
                "attempts": attempts,
                "time_spent_minutes": time_spent,
                "last_asked_intent": random.choice(intents)
            })
            
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating synthetic dataset...")
    df = generate_student_data()
    file_path = "data/student_interactions.csv"
    df.to_csv(file_path, index=False)
    print(f"Dataset saved to {file_path}")
    print(df.head())
