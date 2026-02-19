import sys
import os
import pandas as pd
from dotenv import load_dotenv

# Ensure the src directory is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.query_engine import StudentQueryEngine
    from src.adaptive_engine import AdaptiveLearningEngine
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Ensure you are running this from the project root.")
    sys.exit(1)

def main():
    load_dotenv()
    
    # Initialize Engines
    try:
        query_engine = StudentQueryEngine()
        adaptive_engine = AdaptiveLearningEngine()
    except Exception as e:
        print(f"Failed to initialize engines: {e}")
        return

    while True:
        print("\n=== AI Teaching Assistant Demo ===")
        print("1. Test Student Query Understanding")
        print("2. Test Adaptive Learning Path")
        print("3. Simulate Batch Recommendations (Synthetic Data)")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")
        
        if choice == '1':
            query = input("Enter a student question (e.g., 'I don't understand backpropagation'): ")
            if query:
                print("\nAnalyzing...")
                result = query_engine.analyze_query(query)
                print(f"Result: {result}")
        
        elif choice == '2':
            print("Enter student state details:")
            try:
                score = float(input("Quiz Score (0-100): "))
                attempts = int(input("Number of Attempts: "))
                topic = input("Last Topic (e.g., Backpropagation): ")
                
                state = {
                    "quiz_score": score,
                    "attempts": attempts,
                    "last_topic": topic
                }
                
                recommendation = adaptive_engine.recommend_path(state)
                print(f"\nRecommendation: {recommendation}")
            except ValueError:
                print("Invalid input. Please enter numbers for score and attempts.")

        elif choice == '3':
            data_path = "data/student_interactions.csv"
            if not os.path.exists(data_path):
                print(f"Data file not found at {data_path}. Please run synthetic_data_generator.py first.")
                continue
                
            print(f"Loading data from {data_path}...")
            df = pd.read_csv(data_path)
            sample = df.head(5) # Take first 5 for demo
            
            print("\nProcessing first 5 records:")
            for index, row in sample.iterrows():
                state = {
                    "quiz_score": row['quiz_score'],
                    "attempts": row['attempts'],
                    "last_topic": row['topic']
                }
                rec = adaptive_engine.recommend_path(state)
                print(f"Student {row['student_id']} (Score: {row['quiz_score']}, Topic: {row['topic']}) -> {rec['action']}, Next: {rec['next_topic']}")

        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
