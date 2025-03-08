#!/usr/bin/env python
import sys
import warnings
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from rich.traceback import install as rich_install

from crew import CrewChat

rich_install()
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# warnings.filterwarnings("ignore", category=ResourceWarning)

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
    results = CrewChat().crew().kickoff(inputs=inputs)
    print("\n>>>>>>>>>>>>>>>>. FINAL RESULTS <<<<<<<<<<<<<<<<<<")
    print(results)


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


app = FastAPI()
crew_chat = CrewChat()
crew = crew_chat.crew()


class QueryInput(BaseModel):
    query: str


@app.post("/chat")
async def chat(input_data: QueryInput):
    try:
        inputs = {
            'query': input_data.query,
            'current_year': str(datetime.now().year)
        }

        results = crew.kickoff(inputs=inputs)
        print(results)
        results = json.loads(results.raw)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
