from core.llm_service import LLMService

class CompletenessExamplesAnalyzer:
    """Analyzes the completeness of information and the quality/sufficiency of examples."""

    def __init__(self, llm_service: LLMService):
        """Initializes the CompletenessExamplesAnalyzer.

        Args:
            llm_service: An instance of the LLMService to use for analysis.
        """
        self.llm_service = llm_service

    def analyze(self, text_content: str) -> dict:
        """Analyzes the completeness and examples of the provided text content.

        Args:
            text_content: The text content to analyze.

        Returns:
            A dictionary containing the completeness/examples assessment and suggestions.
            Example structure:
            {
                "assessment": "The article provides a good overview, but lacks detail on X...",
                "suggestions": [
                    "Add an example demonstrating feature Y.",
                    "Clarify the prerequisites mentioned in paragraph Z."
                ],
                "positive_feedback": "The initial example is clear and helpful."
            }
        """
        prompt = f"""Analyze the following documentation content for completeness of information and the quality/sufficiency of examples. Consider:
- Does the article provide enough detail for a user to understand and implement the feature or concept?
- Are there sufficient, clear, and relevant examples provided?
- Are there areas where the information seems incomplete or ambiguous?
- Are there specific places where examples would significantly improve understanding?

Provide:
1.  A brief overall assessment (1-2 sentences) of the content's completeness and the use of examples.
2.  Specific, actionable suggestions for improvement, focusing on adding necessary details or suggesting specific examples (e.g., "Add an example showing how to configure X", "Explain the parameter Y in more detail").
3.  Any positive feedback regarding completeness or the examples provided.

Format the output as a JSON object with keys: "assessment", "suggestions" (list of strings), and "positive_feedback" (string).

Content to analyze:
---
{text_content}
---
"""

        analysis_result = self.llm_service.query_llm(prompt)

        # Basic validation and parsing
        if analysis_result and isinstance(analysis_result, dict):
            return {
                "assessment": analysis_result.get("assessment", "Analysis failed or format incorrect."),
                "suggestions": analysis_result.get("suggestions", []),
                "positive_feedback": analysis_result.get("positive_feedback", "")
            }
        else:
            print(f"Completeness/Examples analysis failed or returned unexpected format: {analysis_result}")
            return {
                "assessment": "Completeness/Examples analysis could not be performed.",
                "suggestions": [],
                "positive_feedback": ""
            }

