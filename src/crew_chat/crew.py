import os
import json

from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from crew_chat.tools.weaviate_tool import create_weaviate_tool
from typing import Dict, List
from pydantic import BaseModel, Field

load_dotenv(override=True)
os.environ["OTEL_SDK_DISABLED"] = "true"

llm = LLM(
    model=f"azure/{os.getenv('model')}",
    api_version=f"{os.getenv('AZURE_API_VERSION')}",
)

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class ResponseTaskOutput(BaseModel):
	summary: str = Field(..., description="A short, summarised, proper and meaningful response to the user query based on the available information.")
	products: List[Dict]

class SearchTaskOutput(BaseModel):
	products: List[Dict]

@CrewBase
class CrewChat():
	"""CrewChat crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools

	@agent
	def search_agent(self) -> Agent:
		'''
        This agent uses the WeaviateVectorSearchTool to search for
        semantically similar documents in a Weaviate vector database.
        '''
		WeaviateProductSearchTool = create_weaviate_tool()
		return Agent(
			config=self.agents_config["search_agent"],
			tools=[WeaviateProductSearchTool],
			llm=llm,
			verbose=True,
		)

	@agent
	def product_agent(self) -> Agent:
		'''
        This agent uses the information retrieved from search_agent
        to answer user queries using product information.
        '''
		return Agent(
			config=self.agents_config["product_agent"],
			llm=llm,
			verbose=True,
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task

	@task
	def search_task(self) -> Task:
		return Task(
			config=self.tasks_config['search_task'],
		)

	@task
	def response_task(self) -> Task:
		return Task(
			config=self.tasks_config['response_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CrewChat crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			llm=llm,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
