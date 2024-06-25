from typing import List, Dict
from agents import ChiefEditorAgent, NewsEditorAgent, JournalistAgent, ScriptAgent, WorkerAgent
import logging

logger = logging.getLogger(__name__)

class MixtureOfAgents:
    def __init__(self):
        self.chief_editor = ChiefEditorAgent()
        self.news_editor = NewsEditorAgent()
        self.journalist = JournalistAgent()
        self.script_agent = ScriptAgent()
        self.worker_agents = [WorkerAgent(f"Worker{i}") for i in range(1, 4)]

    def process(self, articles: List[Dict[str, str]]) -> str:
        try:
            # News Editor Agent process
            news_editor_output = self.news_editor.process(articles)
            
            # Worker Agents process for News Editor
            worker_outputs = self._process_worker_agents(news_editor_output)
            news_editor_refined = self.news_editor.refine(worker_outputs)
            
            # Journalist Agent process
            journalist_output = self.journalist.process(news_editor_refined)
            
            # Worker Agents process for Journalist
            worker_outputs = self._process_worker_agents(journalist_output)
            journalist_refined = self.journalist.refine(worker_outputs)
            
            # Script Agent process
            script_output = self.script_agent.process(journalist_refined)
            
            # Worker Agents process for Script Agent
            worker_outputs = self._process_worker_agents(script_output)
            script_refined = self.script_agent.refine(worker_outputs)
            
            # Chief Editor Agent final process
            final_output = self.chief_editor.process(script_refined)
            
            return final_output
        except Exception as e:
            logger.error(f"Error in MixtureOfAgents process: {str(e)}")
            raise

    def _process_worker_agents(self, input_data: str) -> List[str]:
        return [agent.process(input_data) for agent in self.worker_agents]
