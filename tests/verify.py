import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

try:
    from query_engine import StudentQueryEngine
    from adaptive_engine import AdaptiveLearningEngine
except ImportError:
    # Use fallback if relative import fails or running from root
    sys.path.append(os.path.join(os.getcwd(), 'src'))
    from query_engine import StudentQueryEngine
    from adaptive_engine import AdaptiveLearningEngine

def verify_query_engine():
    print("--- Verifying Student Query Engine ---")
    try:
        engine = StudentQueryEngine()
        query = "I don't understand backpropagation."
        print(f"Query: {query}")
        result = engine.analyze_query(query)
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # specific check
        if "backpropagation" in str(result).lower():
            print("SUCCESS: Topic detected.")
        else:
            print("WARNING: Topic might not be detected accurately.")
            
    except Exception as e:
        print(f"FAILED: {e}")

def verify_adaptive_engine():
    print("\n--- Verifying Adaptive Learning Engine (LLM-based) ---")
    try:
        engine = AdaptiveLearningEngine()
        
        # Case 1: Low Score -> Revision
        state1 = {"quiz_score": 40, "attempts": 1, "last_topic": "Linear Regression"}
        rec1 = engine.recommend_path(state1)
        print(f"State: {state1} -> {rec1}")
        
        # Relaxed check for LLM output, looking for key terms
        if "revision" in str(rec1.get('action', '')).lower():
            print("SUCCESS: Low score triggered Revision.")
        else:
            print(f"WARNING: Expected 'Revision' action, got '{rec1.get('action', '')}'")

        # Case 2: High Score -> Next Topic
        state2 = {"quiz_score": 90, "attempts": 1, "last_topic": "Linear Regression"}
        rec2 = engine.recommend_path(state2)
        print(f"State: {state2} -> {rec2}")
        
        if "next topic" in str(rec2.get('action', '')).lower() or "gradient descent" in str(rec2.get('next_topic', '')).lower():
            print("SUCCESS: High score triggered logical next step.")
        else:
             print(f"WARNING: Expected 'Next Topic' or 'Gradient Descent', got action='{rec2.get('action', '')}'")
             
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    verify_query_engine()
    verify_adaptive_engine()
