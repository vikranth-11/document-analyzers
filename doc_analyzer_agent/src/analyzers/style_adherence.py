from core.llm_service import LLMService

class StyleAdherenceAnalyzer:
    """Analyzes the text content for adherence to simplified style guidelines."""

    def __init__(self, llm_service: LLMService):
        """Initializes the StyleAdherenceAnalyzer.

        Args:
            llm_service: An instance of the LLMService to use for analysis.
        """
        self.llm_service = llm_service

    def analyze(self, text_content: str) -> dict:
        """Analyzes the style adherence of the provided text content.

        Focuses on:
        - Voice and Tone: Customer-focused, clear, concise.
        - Clarity and Conciseness: Avoiding overly complex sentences or jargon.
        - Action-oriented language: Guiding the user effectively.

        Args:
            text_content: The text content to analyze.

        Returns:
            A dictionary containing the style assessment, suggestions, and feedback.
            Example structure:
            {
                "assessment": "The tone is generally good, but some sentences lack conciseness...",
                "suggestions": [
                    "Rephrase sentence X to be more action-oriented.",
                    "Simplify the jargon used in paragraph Y."
                ],
                "positive_feedback": "The voice is customer-focused throughout.",
                "snippet_specific_feedback": "The instruction in step 3 is very clear."
            }
        """
        prompt = f"""Analyze the following documentation content for adherence to these simplified style guidelines:
1.  **Voice and Tone:** Is it customer-focused, clear, and concise?
2.  **Clarity and Conciseness:** Are there overly complex sentences or jargon that could be simplified?
3.  **Action-oriented language:** Does it guide the user effectively, telling them what to do?

Provide:
1.  A brief overall assessment (1-2 sentences) of the style adherence based on these points.
2.  Specific, actionable suggestions for improvement, citing specific sentences or phrases where possible, related to voice/tone, clarity/conciseness, or action-oriented language.
3.  Any positive feedback regarding style adherence.
4.  One or two examples of snippet-specific positive feedback if applicable (e.g., "The call to action in section Z is effective").

Format the output as a JSON object with keys: "assessment", "suggestions" (list of strings), "positive_feedback" (string), and "snippet_specific_feedback" (string).

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
                "snippet_specific_feedback": analysis_result.get("snippet_specific_feedback", "")
            }
        else:
            print(f"Style Adherence analysis failed or returned unexpected format: {analysis_result}")
            return {
                "assessment": "Style Adherence analysis could not be performed.",
                "suggestions": [],
                "positive_feedback": "",
                "snippet_specific_feedback": ""
            }

