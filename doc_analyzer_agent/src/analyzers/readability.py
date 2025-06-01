from core.llm_service import LLMService

class ReadabilityAnalyzer:
    """Analyzes the readability of text content, focusing on a non-technical marketer persona."""

    def __init__(self, llm_service: LLMService):
        """Initializes the ReadabilityAnalyzer.

        Args:
            llm_service: An instance of the LLMService to use for analysis.
        """
        self.llm_service = llm_service

    def analyze(self, text_content: str) -> dict:
        """Analyzes the readability of the provided text content.

        Args:
            text_content: The text content to analyze.

        Returns:
            A dictionary containing the readability assessment, suggestions,
            and persona pain points.
            Example structure:
            {
                "assessment": "The text is moderately readable for a marketer...",
                "suggestions": [
                    "Sentence X is too long...",
                    "Consider defining jargon Y..."
                ],
                "positive_feedback": "The use of bullet points aids readability.",
                "persona_pain_points": "Marketers might struggle with technical term Z."
            }
        """
        prompt = f"""Analyze the following documentation content strictly from the perspective of a non-technical marketer. Assess its readability. Provide:
1.  A brief overall assessment (1-2 sentences) explaining *why* it is or isn't readable for this persona.
2.  Specific, actionable suggestions for improvement, citing specific sentences or phrases where possible. Focus on clarity, sentence structure, and jargon reduction.
3.  Any positive feedback regarding readability.
4.  Specific examples of 'persona pain points' - parts that would likely confuse or frustrate a marketer.

Format the output as a JSON object with keys: "assessment", "suggestions" (list of strings), "positive_feedback" (string), and "persona_pain_points" (string).

Content to analyze:
---
{text_content}
---
"""

        analysis_result = self.llm_service.query_llm(prompt)

        # Basic validation and parsing (can be enhanced)
        if analysis_result and isinstance(analysis_result, dict):
            # Ensure expected keys are present, add defaults if missing
            return {
                "assessment": analysis_result.get("assessment", "Analysis failed or format incorrect."),
                "suggestions": analysis_result.get("suggestions", []),
                "positive_feedback": analysis_result.get("positive_feedback", ""),
                "persona_pain_points": analysis_result.get("persona_pain_points", "")
            }
        else:
            print(f"Readability analysis failed or returned unexpected format: {analysis_result}")
            return {
                "assessment": "Readability analysis could not be performed.",
                "suggestions": [],
                "positive_feedback": "",
                "persona_pain_points": ""
            }

