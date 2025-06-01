# src/processing/summary_generator.py
from core.llm_service import LLMService
import json
import re # Import regex for cleaning

class SummaryGenerator:
    """Generates an executive summary of the analysis findings using an LLM."""

    def __init__(self, llm_service: LLMService):
        """Initializes the SummaryGenerator."""
        self.llm_service = llm_service

    def generate(self, analysis_results: dict, grouped_suggestions: dict) -> str:
        """Generates an executive summary based on analysis results and suggestions."""
        if not analysis_results and not grouped_suggestions:
            return "No analysis results or suggestions available to generate a summary."

        # Prepare a concise summary of findings and suggestions for the prompt
        # CORRECTED: Use standard single quotes inside the f-string expression
        findings_summary = "\n".join([
            f"- {analyzer.capitalize()}: {result.get('assessment', 'N/A')}" 
            for analyzer, result in analysis_results.items()
        ])
        
        suggestion_themes = ", ".join(grouped_suggestions.keys())
        if not suggestion_themes:
             suggestion_themes = "No specific themes identified."

        prompt = f"""Based on the following analysis findings and suggestion themes for a documentation article, write a concise executive summary (2-4 sentences). Highlight the main strengths and the key areas needing improvement.

Analysis Findings:
{findings_summary}

Suggestion Themes:
{suggestion_themes}

Format the output STRICTLY as a JSON object with a single key "summary" containing the executive summary text as its value. Ensure the output is only the JSON object, with no surrounding text or markdown formatting.

Example output format:
{{
  "summary": "The documentation is generally clear but lacks sufficient examples and could benefit from structural improvements like subheadings."
}}
"""
        print("--- Sending summary prompt to LLM ---")
        # Removed expect_json=True
        llm_response_raw = self.llm_service.query_llm(prompt)
        print("--- Received LLM summary response ---")

        summary_text = None
        # Manually parse the JSON response
        if llm_response_raw and isinstance(llm_response_raw, str):
            try:
                # Clean potential markdown code fences
                cleaned_response = re.sub(r"^```json\n?|\n?```$", "", llm_response_raw.strip(), flags=re.MULTILINE)
                parsed_result = json.loads(cleaned_response)
                if isinstance(parsed_result, dict) and "summary" in parsed_result and isinstance(parsed_result["summary"], str):
                    summary_text = parsed_result["summary"]
                    print("Executive summary generated successfully.")
                else:
                    print(f"Warning: Parsed JSON for summary is not a dict with a 'summary' key or value is not string. Parsed: {parsed_result}")
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to decode LLM summary response as JSON: {e}. Response: {llm_response_raw}")
                # Attempt to use raw response if it looks like a simple string summary
                if len(llm_response_raw) < 500 and "{" not in llm_response_raw: # Heuristic for simple string
                     summary_text = llm_response_raw.strip()
                     print("Using raw LLM response as summary.")
        else:
             print(f"Warning: LLM summary response was not a string or was empty. Response: {llm_response_raw}")

        # Provide fallback if parsing failed
        if summary_text is None:
            print("Using fallback summary.")
            findings_str = findings_summary if isinstance(findings_summary, str) else "N/A"
            fallback_summary = "Executive summary could not be automatically generated. Key findings include: " + findings_str.replace("\n", "; ") + ". Key suggestion themes: " + suggestion_themes + "."
            if len(fallback_summary) > 300:
                 fallback_summary = fallback_summary[:297] + "..."
            return fallback_summary
        else:
            return summary_text

