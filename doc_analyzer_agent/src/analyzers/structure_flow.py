from core.llm_service import LLMService

class StructureFlowAnalyzer:
    """Analyzes the structure and logical flow of text content."""

    def __init__(self, llm_service: LLMService):
        """Initializes the StructureFlowAnalyzer.

        Args:
            llm_service: An instance of the LLMService to use for analysis.
        """
        self.llm_service = llm_service

    def analyze(self, text_content: str) -> dict:
        """Analyzes the structure and flow of the provided text content.

        Args:
            text_content: The text content to analyze.

        Returns:
            A dictionary containing the structure/flow assessment and suggestions.
            Example structure:
            {
                "assessment": "The structure is generally clear, but the flow could be improved...",
                "suggestions": [
                    "Consider adding subheadings in section Y.",
                    "Paragraph starting with Z seems out of place."
                ],
                "positive_feedback": "Good use of headings to break up content.",
                "quantified_issues": "3 paragraphs exceed recommended length."
            }
        """
        prompt = f"""Analyze the structure and logical flow of the following documentation content. Consider:
- Use of headings and subheadings for organization.
- Paragraph length and focus.
- Use of lists or bullet points for clarity.
- Logical progression of information: Is it easy to follow? Can users easily find specific information?

Provide:
1.  A brief overall assessment (1-2 sentences) of the structure and flow.
2.  Specific, actionable suggestions for improvement related to structure (headings, paragraphs, lists) and flow (logical order, navigation).
3.  Any positive feedback regarding structure or flow.
4.  Any quantified issues observed (e.g., number of long paragraphs, lack of lists where useful).

Format the output as a JSON object with keys: "assessment", "suggestions" (list of strings), "positive_feedback" (string), and "quantified_issues" (string).

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
                "positive_feedback": analysis_result.get("positive_feedback", ""),
                "quantified_issues": analysis_result.get("quantified_issues", "")
            }
        else:
            print(f"Structure/Flow analysis failed or returned unexpected format: {analysis_result}")
            return {
                "assessment": "Structure/Flow analysis could not be performed.",
                "suggestions": [],
                "positive_feedback": "",
                "quantified_issues": ""
            }

