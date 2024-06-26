import unittest
from unittest.mock import patch, MagicMock
from specific_agent_classes import ChiefEditorAgent, ManagerAgent, WorkerAgent
from base_agent import Thought, AgentError
from config import Config

class TestChiefEditorAgent(unittest.TestCase):
    @patch('specific_agent_classes.Anthropic')
    def setUp(self, mock_anthropic):
        self.mock_client = MagicMock()
        mock_anthropic.return_value = self.mock_client
        self.agent = ChiefEditorAgent("TestChiefEditor", "fake_tavily_key")

    def test_process(self):
        self.mock_client.messages.create.return_value.content = "Processed content"
        result = self.agent.process(["Input 1", "Input 2"])
        self.assertEqual(result, "Processed content")

    def test_process_error(self):
        self.mock_client.messages.create.side_effect = Exception("API Error")
        with self.assertRaises(AgentError):
            self.agent.process(["Input 1", "Input 2"])

class TestManagerAgent(unittest.TestCase):
    @patch('specific_agent_classes.Anthropic')
    def setUp(self, mock_anthropic):
        self.mock_client = MagicMock()
        mock_anthropic.return_value = self.mock_client
        self.agent = ManagerAgent("TestManager", "TestType", "fake_tavily_key")

    def test_process(self):
        self.mock_client.messages.create.return_value.content = "Processed content"
        with patch.object(self.agent, 'tree_of_thought', return_value=[Thought("Test thought")]):
            result = self.agent.process("Test input")
            self.assertEqual(result, "Processed content")

    def test_generate_thoughts(self):
        self.mock_client.messages.create.return_value.content = "Thought 1\nThought 2"
        thoughts = self.agent.generate_thoughts("Test prompt", 1)
        self.assertEqual(len(thoughts), 2)
        self.assertEqual(thoughts[0].content, "Thought 1")

    def test_evaluate_thoughts(self):
        self.mock_client.messages.create.return_value.content = "sure"
        thoughts = [Thought("Test thought")]
        evaluated_thoughts = self.agent.evaluate_thoughts(thoughts)
        self.assertEqual(evaluated_thoughts[0].evaluation, "sure")

class TestWorkerAgent(unittest.TestCase):
    @patch('specific_agent_classes.Anthropic')
    def setUp(self, mock_anthropic):
        self.mock_client = MagicMock()
        mock_anthropic.return_value = self.mock_client
        self.agent = WorkerAgent("TestWorker", "fake_tavily_key")

    def test_process(self):
        self.mock_client.messages.create.return_value.content = "Processed content"
        with patch.object(self.agent, 'tree_of_thought', return_value=[Thought("Test thought")]):
            result = self.agent.process("Test input")
            self.assertEqual(result, "Processed content")

    def test_generate_thoughts(self):
        self.mock_client.messages.create.return_value.content = "Thought 1\nThought 2"
        thoughts = self.agent.generate_thoughts("Test prompt", 1)
        self.assertEqual(len(thoughts), 2)
        self.assertEqual(thoughts[0].content, "Thought 1")

    def test_evaluate_thoughts(self):
        self.mock_client.messages.create.return_value.content = "sure"
        thoughts = [Thought("Test thought")]
        evaluated_thoughts = self.agent.evaluate_thoughts(thoughts)
        self.assertEqual(evaluated_thoughts[0].evaluation, "sure")

if __name__ == '__main__':
    unittest.main()