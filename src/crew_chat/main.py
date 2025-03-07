#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew_chat.crew import CrewChat

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'query': 'Samsung Galaxy Smart Phone',
        'current_year': str(datetime.now().year)
    }
    
    try:
        crew = CrewChat().crew()
        results = crew.kickoff(inputs=inputs)
        print(">>>>>>>>>>>>>>>>. FINAL RESULTS <<<<<<<<<<<<<<<<<<")
        print(results)
    except Exception as e:
        results = {}
        raise Exception(f"An error occurred while running the crew: {e}")
    return results

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CrewChat().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewChat().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")




def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "query": "smart phone",
        "topic": "AI LLMs"
    }

    try:
        # print("Testing the crew...", sys.argv[1]))
        CrewChat().crew().test(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
