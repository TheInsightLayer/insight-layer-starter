# tests/test_task_agent.py

import unittest
from unittest.mock import patch, MagicMock
from src.graph.task_agent import run_task, log_prompt_trace 


class TestTaskAgent(unittest.TestCase):

    @patch("src.graph.task_agent.ChatOpenAI.invoke")
    @patch("src.graph.task_agent.log_prompt_trace")
    def test_run_task_success(self, mock_log_trace, mock_invoke):
        """
        Test run_task when the OpenAI API successfully returns a response.
        """
        mock_invoke.return_value = MagicMock(content="This is the LLM output.")

        prompt = "What strategies can we use to improve customer retention in Q3?"
        task_meta = {"purpose": "strategy", "task": "Improve customer retention"}
        insights = [{"id": "insight1", "summary": "Retention increased by 15% in Q2."}]

        result = run_task(prompt, task_meta, insights)

        self.assertEqual(result, "This is the LLM output.")
        mock_log_trace.assert_called_once_with(
            task=task_meta["task"],
            task_meta=task_meta,
            insights=insights,
            prompt=prompt,
            output="This is the LLM output.",
            success=True
        )

    @patch("src.graph.task_agent.ChatOpenAI.invoke")
    @patch("src.graph.task_agent.log_prompt_trace")
    def test_run_task_failure(self, mock_log_trace, mock_invoke):
        """
        Test run_task when the OpenAI API raises an exception.
        """
        mock_invoke.side_effect = Exception("Simulated API failure")

        prompt = "What strategies can we use to improve customer retention in Q3?"
        task_meta = {"purpose": "strategy", "task": "Improve customer retention"}
        insights = [{"id": "insight1", "summary": "Retention increased by 15% in Q2."}]

        with self.assertRaises(RuntimeError) as context:
            run_task(prompt, task_meta, insights)

        self.assertIn("Prompt execution failed: Simulated API failure", str(context.exception))
        mock_log_trace.assert_called_once_with(
            task=task_meta["task"],
            task_meta=task_meta,
            insights=insights,
            prompt=prompt,
            output="Simulated API failure",
            success=False
        )

if __name__ == "__main__":
    unittest.main()
