import logging
from tree_of_thought import TreeOfThought
from api_utils import make_api_call, AnthropicAPIError
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

class Agent:
    def __init__(self, name: str, model: str, tot_depth: int = 2, tot_branching: int = 2):
        self.name = name
        self.model = model
        self.tot = TreeOfThought(max_depth=tot_depth, branching_factor=tot_branching)
        self.tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

    def process(self, input_data: str) -> str:
        raise NotImplementedError("Subclasses must implement this method")

    def search_internet(self, query: str) -> str:
        try:
            search_result = self.tavily_client.get_search_context(
                query=query,
                search_depth="advanced",
                max_results=3,
            )
            return str(search_result)
        except Exception as e:
            logger.error(f"Error searching the internet: {str(e)}")
            return f"Error: {str(e)}"

class ChiefEditorAgent(Agent):
    def __init__(self):
        super().__init__("ChiefEditor", "claude-3.5-sonnet")

    def process(self, input_data: str) -> str:
        system_prompt = f"You are the Chief Editor Agent. Your task is to review and refine the podcast script, ensuring it meets the highest standards of quality and engagement."
        user_prompt = f"Review and refine the following podcast script:\n\n{input_data}"
        
        try:
            return make_api_call(system=system_prompt, messages=[{"role": "user", "content": user_prompt}], model=self.model)
        except AnthropicAPIError as e:
            logger.error(f"Error in ChiefEditorAgent process: {str(e)}")
            raise

class NewsEditorAgent(Agent):
    def __init__(self):
        super().__init__("NewsEditor", "claude-3.5-sonnet")

    def process(self, articles: List[Dict[str, str]]) -> str:
        system_prompt = f"You are the News Editor Agent. Your task is to analyze the top AI stories and create a summary that will be used to guide the podcast script creation."
        user_prompt = f"Analyze the following top AI stories and create a summary:\n\n{articles}"
        
        try:
            return make_api_call(system=system_prompt, messages=[{"role": "user", "content": user_prompt}], model=self.model)
        except AnthropicAPIError as e:
            logger.error(f"Error in NewsEditorAgent process: {str(e)}")
            raise

    def refine(self, worker_outputs: List[str]) -> str:
        system_prompt = f"You are the News Editor Agent. Your task is to refine and synthesize the outputs from the worker agents into a cohesive summary."
        user_prompt = f"Refine and synthesize the following worker agent outputs:\n\n{worker_outputs}"
        
        try:
            return make_api_call(system=system_prompt, messages=[{"role": "user", "content": user_prompt}], model=self.model)
        except AnthropicAPIError as e:
            logger.error(f"Error in NewsEditorAgent refine: {str(e)}")
            raise

class JournalistAgent(Agent):
    def __init__(self):
        super().__init__("Journalist", "claude-3.5-sonnet")

    def process(self, input_data: str) -> str:
        system_prompt = f"You are the Journalist Agent. Your task is to take the news summary and create detailed content for the podcast script."
        user_prompt = f"Create detailed content for the podcast script based on this news summary:\n\n{input_data}"
        
        try:
            return make_api_call(system=system_prompt, messages=[{"role": "user", "content": user_prompt}], model=self.model)
        except AnthropicAPIError as e:
            logger.error(f"Error in JournalistAgent process: {str(e)}")
            raise

    def refine(self, worker_outputs: List[str]) -> str:
        system_prompt = f"You are the Journalist Agent. Your task is to refine and synthesize the outputs from the worker agents into cohesive detailed content."
        user_prompt = f"Refine and synthesize the following worker agent outputs:\n\n{worker_outputs}"
        
        try:
            return make_api_call(system=system_prompt, messages=[{"role": "user", "content": user_prompt}], model=self.model)
        except AnthropicAPIError as e:
            logger.error(f"Error in JournalistAgent refine: {str(e)}")
            raise

class ScriptAgent(Agent):
    def __init__(self):
        super().__init__("Script", "claude-3.5-sonnet")

    def process(self, input_data: str) -> str:
        system_prompt = f"You are the Script Agent. Your task is to take the detailed content and format it into a cohesive podcast script."
        user_prompt = f"Format the following content into a podcast script:\n\n{input_data}"
        
        try:
            return make_api_call(system=system_prompt, messages=[{"role": "user", "content": user_prompt}], model=self.model)
        except AnthropicAPIError as e:
            logger.error(f"Error in ScriptAgent process: {str(e)}")
            raise

    def refine(self, worker_outputs: List[str]) -> str:
        system_prompt = f"You are the Script Agent. Your task is to refine and synthesize the outputs from the worker agents into a final cohesive podcast script."
        user_prompt = f"Refine and synthesize the following worker agent outputs into a final podcast script:\n\n{worker_outputs}"
        
        try:
            return make_api_call(system=system_prompt, messages=[{"role": "user", "content": user_prompt}], model=self.model)
        except AnthropicAPIError as e:
            logger.error(f"Error in ScriptAgent refine: {str(e)}")
            raise

class WorkerAgent(Agent):
    def __init__(self, name: str):
        super().__init__(name, "claude-3.0-haiku")

    def process(self, input_data: str) -> str:
        thoughts, synthesis = self.tot.process(input_data)
        return synthesis
