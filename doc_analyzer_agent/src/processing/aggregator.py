def aggregate_suggestions(analysis_results: dict) -> list[dict]:
    """Aggregates suggestions from all analyzer results.

    Args:
        analysis_results: A dictionary where keys are analyzer names (e.g., 'readability')
                          and values are the dictionaries returned by each analyzer's
                          analyze() method.

    Returns:
        A list of suggestion dictionaries, each augmented with a 'source' key
        indicating which analyzer generated it.
        Example: [{"suggestion": "Sentence X is too long...", "source": "readability"}, ...]
    """
    all_suggestions = []
    for analyzer_name, result in analysis_results.items():
        if result and isinstance(result, dict):
            suggestions = result.get("suggestions", [])
            if isinstance(suggestions, list):
                for sugg_text in suggestions:
                    if isinstance(sugg_text, str): # Ensure it's the text suggestion
                        all_suggestions.append({
                            "suggestion": sugg_text,
                            "source": analyzer_name.replace("_", " ").title() # Use a readable source name
                        })
                    elif isinstance(sugg_text, dict) and "suggestion" in sugg_text: # Handle if suggestions are already dicts
                         sugg_text["source"] = analyzer_name.replace("_", " ").title()
                         all_suggestions.append(sugg_text)
                    else:
                        print(f"Warning: Unexpected suggestion format from {analyzer_name}: {sugg_text}")
            else:
                 print(f"Warning: Suggestions from {analyzer_name} are not in a list format: {suggestions}")

    return all_suggestions

