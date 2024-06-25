import logging
from typing import List, Tuple
from thought import Thought
from api_utils import make_api_call, AnthropicAPIError

logger = logging.getLogger(__name__)

class TreeOfThought:
    def __init__(self, max_depth: int = 2, branching_factor: int = 2):
        self.max_depth = max_depth
        self.branching_factor = branching_factor

    def generate_and_evaluate_thoughts(self, prompt: str, depth: int) -> List[Thought]:
        system_prompt = f"""Generate and evaluate {self.branching_factor} thoughts as next steps for the given prompt.
        For each thought, provide an evaluation of 'sure', 'maybe', or 'impossible'.
        Format your response as follows:
        Thought 1: [content] - Evaluation: [evaluation]
        Thought 2: [content] - Evaluation: [evaluation]
        Synthesis: [A brief synthesis of the thoughts, directly addressing the prompt]"""

        user_prompt = f"Depth: {depth}\nPrompt: {prompt}\n\nGenerate and evaluate {self.branching_factor} thoughts:"
        
        try:
            response = make_api_call(system=system_prompt, messages=[{"role": "user", "content": user_prompt}])
            thoughts = []
            for line in response.split('\