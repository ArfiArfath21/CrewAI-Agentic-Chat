# CrewChat Crew

Welcome to the CrewChat Crew project, powered by [crewAI](https://crewai.com). This is a multi-agent Conversational AI Chatbot, built by leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable the agents to collaborate effectively on user queries, maximizing their collective intelligence and capabilities to provide the best responses.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Set/Add the following entry in `/etc/hosts` to avoid the telemetry connection issue:
```txt
127.0.0.1       telemetry.crewai.com
```

## Running the Project
Navigate to your project directory and install the dependencies:
```bash
crewai install
uv add weaviate-client crewai[tools] fastapi uvicorn rich
cd src
```

> Note: The current code expects a 'Products' collection in the local Weaviate instance.

Now, kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:
```bash
uvicorn main:app --reload
```

This command initializes the crew-chat Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.