import unittest
from unittest.mock import patch
from src.memory.summarizer import summarize_and_normalize

class TestSummarizer(unittest.TestCase):
    @patch("src.memory.summarizer.summarize_output")
    def test_summarize_and_normalize(self, mock_summarize_output):
        """
        Test the summarize_and_normalize function with mocked summarize_output.
        """
        # Mock the output of summarize_output
        mock_summarize_output.return_value = {
            "summary": "This is a test summary.",
            "context": {"purpose": "test"}
        }

        # Input data
        agent_output = "This is the agent's output."
        task_meta = {"purpose": "test"}

        # Call the function
        result = summarize_and_normalize(agent_output, task_meta)

        # Assert the mocked function was called with the correct arguments
        mock_summarize_output.assert_called_once_with(
            output=agent_output,
            context=task_meta,
            use_llm=True,
            trace_enabled=False
        )

        # Assert the result matches the mocked return value
        self.assertEqual(result, {
            "summary": "This is a test summary.",
            "context": {"purpose": "test"}
        })

if __name__ == "__main__":
    unittest.main()