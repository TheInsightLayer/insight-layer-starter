import unittest
from unittest.mock import patch, MagicMock
from src.graph.task_parser import parse_task, fallback_parse

class TestTaskParser(unittest.TestCase):

    @patch("src.graph.task_parser.ChatOpenAI.invoke")
    def test_parse_task_success(self, mock_invoke):
        """
        Test parse_task when the OpenAI API successfully returns a response.
        """
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.content = '{"purpose": "campaign planning", "topic": "loyalty", "quarter": "Q2"}'
        mock_invoke.return_value = mock_response

        # Input prompt
        prompt = "Design a Q2 promotion strategy to boost loyalty"

        # Call the function
        result = parse_task(prompt)

        # Assert the result
        self.assertEqual(result["purpose"], "campaign planning")
        self.assertEqual(result["topic"], "loyalty")
        self.assertEqual(result["quarter"], "Q2")

    @patch("src.graph.task_parser.ChatOpenAI.invoke", side_effect=Exception("API failure"))
    def test_parse_task_fallback(self, mock_invoke):
        """
        Test parse_task when the OpenAI API fails and the fallback method is used.
        """
        # Input prompt
        prompt = "Design a Q2 promotion strategy to boost loyalty"

        # Call the function
        result = parse_task(prompt)

        # Assert the fallback result
        fallback_result = fallback_parse(prompt)
        self.assertEqual(result, fallback_result)

    def test_fallback_parse(self):
        """
        Test the fallback_parse function directly.
        """
        # Input prompt
        prompt = "Design a Q2 promotion strategy to boost loyalty"

        # Call the fallback function
        result = fallback_parse(prompt)

        # Assert the result
        self.assertEqual(result["purpose"], "campaign planning")
        self.assertEqual(result["topic"], "loyalty")
        self.assertEqual(result["quarter"], "Q2")

if __name__ == "__main__":
    unittest.main()
