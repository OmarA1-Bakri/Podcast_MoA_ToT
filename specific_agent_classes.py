from base_agent import Agent, Thought, AgentError
from typing import List, Dict
import logging
from config import Config
from ratelimit import limits, sleep_and_retry
from api_utils import make_api_call, AnthropicAPIError

logger = logging.getLogger(__name__)

class ChiefEditorAgent(Agent):
    def __init__(self, name: str, tavily_api_key: str):
        super().__init__(name, Config.CHIEF_EDITOR_MODEL, tavily_api_key)

    @sleep_and_retry
    @limits(calls=20, period=60)
    def process(self, inputs: List[str]) -> str:
        try:
            prompt = f"As the Chief Editor, review and synthesize the following inputs into a final podcast script:\n\n"
            prompt += "\n\n".join(inputs)
            
            return make_api_call(
                system="You are the Chief Editor AI, tasked with synthesizing inputs into a coherent podcast script.",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000
            )
        except AnthropicAPIError as e:
            logger.error(f"Error in ChiefEditorAgent processing: {str(e)}")
            raise AgentError(f"Error in ChiefEditorAgent processing: {str(e)}")

class ManagerAgent(Agent):
    def __init__(self, name: str, agent_type: str, tavily_api_key: str):
        super().__init__(name, Config.MANAGER_MODEL, tavily_api_key)
        self.agent_type = agent_type

    @sleep_and_retry
    @limits(calls=20, period=60)
    def process(self, input: str) -> str:
        try:
            thoughts = self.tree_of_thought(input)
            
            prompt = f"As the {self.agent_type}, synthesize the following thoughts into a coherent output:\n\n"
            prompt += "\n\n".join([t.content for t in thoughts])
            
            return make_api_call(
                system=f"You are the {self.agent_type} AI, tasked with synthesizing thoughts into a coherent output.",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
        except AnthropicAPIError as e:
            logger.error(f"Error in ManagerAgent processing: {str(e)}")
            raise AgentError(f"Error in ManagerAgent processing: {str(e)}")

    @sleep_and_retry
    @limits(calls=20, period=60)
    def generate_thoughts(self, prompt: str, depth: int) -> List[Thought]:
        try:
            full_prompt = f"Generate {self.branching_factor} diverse thoughts on the following prompt:\n\n{prompt}"
            
            response = make_api_call(
                system="You are an AI tasked with generating diverse thoughts on a given prompt.",
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=1000
            )
            
            thoughts = [Thought(t.strip()) for t in response.split('\n') if t.strip()]
            return thoughts[:self.branching_factor]
        except AnthropicAPIError as e:
            logger.error(f"Error generating thoughts: {str(e)}")
            raise AgentError(f"Error generating thoughts: {str(e)}")

    @sleep_and_retry
    @limits(calls=20, period=60)
    def evaluate_thoughts(self, thoughts: List[Thought]) -> List[Thought]:
        try:
            for thought in thoughts:
                prompt = f"Quickly evaluate as 'sure', 'maybe', or 'impossible':\n\n{thought.content}"
                
                evaluation = make_api_call(
                    system="You are an AI tasked with evaluating thoughts as 'sure', 'maybe', or 'impossible'.",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=50
                )
                thought.evaluation = evaluation.strip().lower()
            return thoughts
        except AnthropicAPIError as e:
            logger.error(f"Error evaluating thoughts: {str(e)}")
            raise AgentError(f"Error evaluating thoughts: {str(e)}")

class WorkerAgent(ManagerAgent):
    def __init__(self, name: str, tavily_api_key: str):
        super().__init__(name, "Worker", tavily_api_key)

    @sleep_and_retry
    @limits(calls=20, period=60)
    def process(self, input: str) -> str:
        try:
            thoughts = self.tree_of_thought(input)
            
            prompt = f"Synthesize the following thoughts into a concise output:\n\n"
            prompt += "\n\n".join([t.content for t in thoughts])
            
            return make_api_call(
                system="You are a Worker AI, tasked with synthesizing thoughts into a concise output.",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
        except AnthropicAPIError as e:
            logger.error(f"Error in WorkerAgent processing: {str(e)}")
            raise AgentError(f"Error in WorkerAgent processing: {str(e)}")
