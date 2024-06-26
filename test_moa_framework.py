import unittest
from unittest.mock import patch, MagicMock
from moa_framework import MoAFramework
from config import Config

class TestMoAFramework(unittest.TestCase):
    @patch('moa_framework.RSSFeedParser')
    @patch('moa_framework.ChiefEditorAgent')
    @patch('moa_framework.ManagerAgent')
    @patch('moa_framework.WorkerAgent')
    def setUp(self, mock_worker, mock_manager, mock_chief_editor, mock_rss_parser):
        self.mock_rss_parser = mock_rss_parser.return_value
        self.mock_chief_editor = mock_chief_editor.return_value
        self.mock_manager = mock_manager.return_value
        self.mock_worker = mock_worker.return_value

        self.framework = MoAFramework("fake_rss_url", "fake_tavily_key")
        self.framework.worker_agents = {
            "news_editor": [self.mock_worker],
            "journalist": [self.mock_worker],
            "script_writer": [self.mock_worker]
        }
        self.framework.manager_agents = {
            "news_editor": self.mock_manager,
            "journalist": self.mock_manager,
            "script_writer": self.mock_manager
        }

    def test_process_worker_layer(self):
        self.mock_worker.process.return_value = "Processed worker output"
        self.mock_manager.process.return_value = "Processed manager output"
        result = self.framework.process_worker_layer("news_editor", "Test input")
        self.assertEqual(result, "Processed manager output")

    def test_process_worker_layer_unknown_worker_type(self):
        with self.assertRaises(ValueError) as context:
            self.framework.process_worker_layer("unknown_type", "Test input")
        self.assertIn("Unknown worker agent type", str(context.exception))

    def test_process_worker_layer_unknown_manager_type(self):
        self.framework.worker_agents["test_type"] = [self.mock_worker]
        with self.assertRaises(ValueError) as context:
            self.framework.process_worker_layer("test_type", "Test input")
        self.assertIn("Unknown manager agent type", str(context.exception))

    def test_generate_podcast_script(self):
        self.mock_rss_parser.get_top_stories.return_value = [
            {"title": "Test Title", "summary": "Test Summary"}
        ]
        self.mock_worker.process.return_value = "Processed worker output"
        self.mock_manager.process.return_value = "Processed manager output"
        self.mock_chief_editor.process.return_value = "Final script"

        result = self.framework.generate_podcast_script()
        self.assertEqual(result, "Final script")

    def test_generate_podcast_script_error(self):
        self.mock_rss_parser.get_top_stories.side_effect = Exception("RSS Error")
        with self.assertRaises(Exception) as context:
            self.framework.generate_podcast_script()
        self.assertIn("RSS Error", str(context.exception))

if __name__ == '__main__':
    unittest.main()