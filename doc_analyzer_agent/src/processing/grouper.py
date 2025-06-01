# src/processing/grouper.py
from core.llm_service import LLMService
import json
import hashlib
import re # Import regex for cleaning

class SuggestionGrouper:
    """Groups suggestions thematically using an LLM."""

    def __init__(self, llm_service: LLMService):
        """Initializes the SuggestionGrouper."""
        self.llm_service = llm_service

    def _generate_suggestion_id(self, suggestion_dict: dict) -> str:
        """Generates a stable ID for a suggestion dictionary."""
        suggestion_text = suggestion_dict.get("suggestion", "")
        return hashlib.md5(suggestion_text.encode()).hexdigest()[:8] # Short hash

    def group(self, prioritized_suggestions: list[dict]) -> dict:
        """Groups a list of prioritized suggestions into thematic categories using the LLM."""
        if not prioritized_suggestions:
            print("No suggestions provided for grouping.")
            return {}

        suggestion_map_by_id = {}
        suggestions_for_prompt = []
        for i, s in enumerate(prioritized_suggestions):
            s_id = f"sugg_{i}"
            suggestion_map_by_id[s_id] = s
            s_text = s.get("suggestion", "N/A")
            s_impact = s.get("impact", "N/A")
            s_difficulty = s.get("difficulty", "N/A")
            s_source = s.get("source", "Unknown")
            prompt_line = f"- ID: {s_id}, Suggestion: {s_text} (Impact: {s_impact}, Difficulty: {s_difficulty}, Source: {s_source})"
            suggestions_for_prompt.append(prompt_line)

        suggestions_text = "\n".join(suggestions_for_prompt)

        prompt = f"""Given the following list of prioritized suggestions for improving documentation, each with a unique ID, group them into logical thematic categories. Choose concise, descriptive names for each category (e.g., "Clarity & Conciseness", "Structural Enhancements", "Example Addition", "Tone Adjustment", "User Experience").

Suggestions:
{suggestions_text}

Format the output STRICTLY as a JSON object where keys are the thematic category names and values are lists of the corresponding suggestion IDs (e.g., ["sugg_0", "sugg_5"]) that belong to that category. Do NOT include the suggestion text in the output JSON values, only the IDs. Ensure the output is only the JSON object, with no surrounding text or markdown formatting.

Example output format:
{{
  "Clarity & Conciseness": ["sugg_1", "sugg_4"],
  "Structural Enhancements": ["sugg_0"],
  "User Experience": ["sugg_2", "sugg_3", "sugg_5"]
}}
"""

        print("--- Sending grouping prompt to LLM ---")
        # Removed expect_json=True
        llm_response_raw = self.llm_service.query_llm(prompt)
        print("--- Received LLM grouping response ---")

        grouped_suggestions_dict = {}
        processed_ids = set()
        raw_grouped_ids = None

        # Manually parse the JSON response
        if llm_response_raw and isinstance(llm_response_raw, str):
            try:
                # Clean potential markdown code fences
                cleaned_response = re.sub(r"^```json\n?|\n?```$", "", llm_response_raw.strip(), flags=re.MULTILINE)
                raw_grouped_ids = json.loads(cleaned_response)
                if not isinstance(raw_grouped_ids, dict):
                    print(f"Warning: Parsed JSON for grouping is not a dictionary. Type: {type(raw_grouped_ids)}")
                    raw_grouped_ids = None # Reset if not a dict
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to decode LLM grouping response as JSON: {e}. Response: {llm_response_raw}")
        else:
             print(f"Warning: LLM grouping response was not a string or was empty. Response: {llm_response_raw}")

        # Process the parsed dictionary (if successful)
        if raw_grouped_ids and isinstance(raw_grouped_ids, dict):
            for theme, suggestion_ids in raw_grouped_ids.items():
                if isinstance(suggestion_ids, list):
                    grouped_suggestions_dict[theme] = []
                    for s_id in suggestion_ids:
                        if isinstance(s_id, str) and s_id in suggestion_map_by_id:
                            grouped_suggestions_dict[theme].append(suggestion_map_by_id[s_id])
                            processed_ids.add(s_id)
                        else:
                            print(f"Warning: LLM returned unknown or invalid suggestion ID: {s_id} for theme ", {theme})
                else:
                     print(f"Warning: Invalid format for theme ", {theme}, " in grouping result. Expected list of IDs.")
            print(f"Successfully grouped suggestions into themes: {list(grouped_suggestions_dict.keys())}")
        else:
             print("Grouping dictionary was not successfully created from LLM response.")
             # Fallback handled later

        # Check for uncategorized suggestions
        uncategorized = []
        for s_id, original_sugg in suggestion_map_by_id.items():
            if s_id not in processed_ids:
                uncategorized.append(original_sugg)

        if uncategorized:
            if not grouped_suggestions_dict: # If primary grouping failed entirely
                 print("LLM grouping failed. Falling back to grouping by source.")
                 fallback_grouping = {}
                 for s in prioritized_suggestions:
                     source = s.get("source", "Unknown")
                     if source not in fallback_grouping:
                         fallback_grouping[source] = []
                     fallback_grouping[source].append(s)
                 return fallback_grouping
            else:
                grouped_suggestions_dict["Uncategorized"] = uncategorized
                print(f"Warning: {len(uncategorized)} suggestions were not categorized by the LLM and placed in \'Uncategorized\'.")

        if not grouped_suggestions_dict:
             print("Critical: Grouping failed and fallback also yielded no groups.")
             fallback_grouping = {}
             for s in prioritized_suggestions:
                 source = s.get("source", "Unknown")
                 if source not in fallback_grouping:
                     fallback_grouping[source] = []
                 fallback_grouping[source].append(s)
             return fallback_grouping

        return grouped_suggestions_dict
