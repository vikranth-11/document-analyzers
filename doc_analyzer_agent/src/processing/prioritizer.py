from core.llm_service import LLMService
import json

class SuggestionPrioritizer:
    """Prioritizes suggestions based on estimated impact and difficulty using an LLM."""

    def __init__(self, llm_service: LLMService):
        """Initializes the SuggestionPrioritizer.

        Args:
            llm_service: An instance of the LLMService to use for analysis.
        """
        self.llm_service = llm_service

    def prioritize(self, all_suggestions: list[dict]) -> list[dict]:
        """Prioritizes a list of suggestions using the LLM.

        Args:
            all_suggestions: A list of suggestion dictionaries. Each dictionary
                             should at least contain a 'suggestion' key with the text.
                             Example: [{'suggestion': 'Sentence X is too long...', 'source': 'Readability'}, ...]

        Returns:
            A list of suggestion dictionaries, each augmented with 'impact' (e.g., High, Medium, Low)
            and 'difficulty' (e.g., High, Medium, Low) scores, and sorted by impact.
            Returns the original list if prioritization fails.
        """
        if not all_suggestions:
            return []

        # Prepare the suggestions for the prompt
        suggestions_text = "\n".join([f"- {s.get('suggestion', 'N/A')} (Source: {s.get('source', 'Unknown')})" for s in all_suggestions])

        prompt = f"""Given the following list of suggestions for improving documentation, please evaluate each suggestion based on its potential **impact** on user understanding/experience and the estimated **difficulty** to implement the change. 

Use categories: High, Medium, Low for both impact and difficulty.

Suggestions:
{suggestions_text}

Format the output as a JSON list of objects. Each object should contain:
1.  "suggestion": The original suggestion text.
2.  "impact": "High", "Medium", or "Low".
3.  "difficulty": "High", "Medium", or "Low".

Example output format:
[
  {{
    "suggestion": "Sentence X is too long...",
    "impact": "Medium",
    "difficulty": "Low"
  }},
  {{
    "suggestion": "Add an example demonstrating feature Y.",
    "impact": "High",
    "difficulty": "Medium"
  }}
]
"""

        prioritization_result = self.llm_service.query_llm(prompt)

        if prioritization_result and isinstance(prioritization_result, list):
            # Add scores back to the original suggestions (match by suggestion text)
            scored_suggestions = []
            original_suggestions_map = {s.get('suggestion'): s for s in all_suggestions}
            
            for scored_item in prioritization_result:
                original_suggestion_text = scored_item.get('suggestion')
                if original_suggestion_text in original_suggestions_map:
                    original_suggestion = original_suggestions_map[original_suggestion_text]
                    original_suggestion['impact'] = scored_item.get('impact', 'N/A')
                    original_suggestion['difficulty'] = scored_item.get('difficulty', 'N/A')
                    scored_suggestions.append(original_suggestion)
                else:
                    # Handle cases where the LLM might slightly alter the suggestion text
                    print(f"Warning: Could not map prioritized suggestion back: {original_suggestion_text}")
                    # Add it anyway, but mark it
                    scored_item['source'] = 'Unknown (Mapping Failed)'
                    scored_suggestions.append(scored_item)

            # Sort by impact (High > Medium > Low)
            impact_order = {"High": 0, "Medium": 1, "Low": 2, "N/A": 3}
            scored_suggestions.sort(key=lambda x: impact_order.get(x.get('impact', 'N/A'), 3))
            
            # Ensure all original suggestions are included, even if scoring failed for some
            returned_suggestions_texts = {s.get('suggestion') for s in scored_suggestions}
            for original in all_suggestions:
                if original.get('suggestion') not in returned_suggestions_texts:
                    original['impact'] = 'N/A'
                    original['difficulty'] = 'N/A'
                    scored_suggestions.append(original)
                    print(f"Warning: Suggestion not scored by LLM: {original.get('suggestion')}")

            return scored_suggestions
        else:
            print(f"Suggestion prioritization failed or returned unexpected format: {prioritization_result}")
            # Return original suggestions with N/A scores if LLM fails
            for s in all_suggestions:
                s['impact'] = 'N/A'
                s['difficulty'] = 'N/A'
            return all_suggestions

