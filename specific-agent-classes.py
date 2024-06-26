from base_agent import Agent, Thought, AgentError
from typing import List, Dict
import anthropic
import logging
from config import Config

logger = logging.getLogger(__name__)

class ChiefEditorAgent(Agent):
    def __init__(self, name: str, tavily_api_key: str):
        super().__init__(name, Config.CHIEF_EDITOR_MODEL, tavily_api_key)
        try:
            self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {str(e)}")
            raise AgentError(f"Failed to initialize Anthropic client: {str(e)}")

    def process(self, inputs: List[str]) -> str:
        try:
            prompt = f"As the Chief Editor, review and synthesize the following inputs into a final podcast script:\n\n"
            prompt += "\n\n".join(inputs)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content
        except Exception as e:
            logger.error(f"Error in ChiefEditorAgent processing: {str(e)}")
            raise AgentError(f"Error in ChiefEditorAgent processing: {str(e)}")

class ManagerAgent(Agent):
    def __init__(self, name: str, agent_type: str, tavily_api_key: str):
        super().__init__(name, Config.MANAGER_MODEL, tavily_api_key)
        self.agent_type = agent_type
        try:
            self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {str(e)}")
            raise AgentError(f"Failed to initialize Anthropic client: {str(e)}")

    def process(self, input: str) -> str:
        try:
            thoughts = self.tree_of_thought(input)
            
            prompt = f"As the {self.agent_type}, synthesize the following thoughts into a coherent output:\n\n"
            prompt += "\n\n".join([t.content for t in thoughts])
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content
        except Exception as e:
            logger.error(f"Error in ManagerAgent processing: {str(e)}")
            raise AgentError(f"Error in ManagerAgent processing: {str(e)}")

    def generate_thoughts(self, prompt: str, depth: int) -> List[Thought]:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.9,
                messages=[
                    {"role": "user", "content": f"Generate {self.branching_factor} diverse thoughts on the following prompt:\n\n{prompt}"}
                ]
            )
            
            thoughts = [Thought(content) for content in response.content.split('\n') if content.strip()]
            return thoughts[:self.branching_factor]
        except Exception as e:
            logger.error(f"Error generating thoughts: {str(e)}")
            raise AgentError(f"Error generating thoughts: {str(e)}")

    def evaluate_thoughts(self, thoughts: List[Thought]) -> List[Thought]:
        try:
            for thought in thoughts:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=100,
                    temperature=0.5,
                    messages=[
                        {"role": "user", "content": f"Evaluate the following thought as 'sure', 'maybe', or 'impossible':\n\n{thought.content}"}
                    ]
                )
                thought.evaluation = response.content.strip().lower()
            return thoughts
        except Exception as e:
            logger.error(f"Error evaluating thoughts: {str(e)}")
            raise AgentError(f"Error evaluating thoughts: {str(e)}")

class WorkerAgent(Agent):
    def __init__(self, name: str, tavily_api_key: str):
        super().__init__(name, Config.WORKER_MODEL, tavily_api_key)
        try:
            self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {str(e)}")
            raise AgentError(f"Failed to initialize Anthropic client: {str(e)}")

    def process(self, input: str) -> str:
        try:
            thoughts = self.tree_of_thought(input)
            
            prompt = f"Synthesize the following thoughts into a concise output:\n\n"
            prompt += "\n\n".join([t.content for t in thoughts])
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content
        except Exception as e:
            logger.error(f"Error in WorkerAgent processing: {str(e)}")
            raise AgentError(f"Error in WorkerAgent processing: {str(e)}")

    def generate_thoughts(self, prompt: str, depth: int) -> List[Thought]:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.9,
                messages=[
                    {"role": "user", "content": f"Generate {self.branching_factor} brief thoughts on:\n\n{prompt}"}
                ]
            )
            
            thoughts = [Thought(content) for content in response.content.split('\n') if content.strip()]
            return thoughts[:self.branching_factor]
        except Exception as e:
            logger.error(f"Error generating thoughts: {str(e)}")
            raise AgentError(f"Error generating thoughts: {str(e)}")

    def evaluate_thoughts(self, thoughts: List[Thought]) -> List[Thought]:
        try:
            for thought in thoughts:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=50,
                    temperature=0.5,
                    messages=[
                        {"role": "user", "content": f"Quickly evaluate as 'sure', 'maybe', or 'impossible':\n\n{thought.content}"}
                    ]
                )
                thought.evaluation = response.content.strip().lower()
            return thoughts
        except Exception as e:
            logger.error(f"Error evaluating thoughts: {str(e)}")
            raise AgentError(f"Error evaluating thoughts: {str(e)}")

