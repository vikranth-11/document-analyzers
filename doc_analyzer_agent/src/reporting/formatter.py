from datetime import datetime

class ReportFormatter:
    """Formats the analysis results and suggestions into a structured report."""

    def format_report(
        self,
        url: str,
        analysis_results: dict,
        prioritized_suggestions: list[dict],
        grouped_suggestions: dict,
        executive_summary: str,
        top_n: int = 5 # Number of top suggestions to highlight
    ) -> str:
        """Generates a formatted report string (Markdown).

        Args:
            url: The URL that was analyzed.
            analysis_results: Dictionary containing results from each analyzer module.
            prioritized_suggestions: List of suggestion dictionaries, sorted by priority.
            grouped_suggestions: Dictionary of thematically grouped suggestions.
            executive_summary: The generated executive summary string.
            top_n: The number of top-priority suggestions to list separately.

        Returns:
            A string containing the formatted report in Markdown.
        """
        report = []
        report.append(f"# Documentation Analysis Report")
        report.append(f"**URL Analyzed:** {url}")
        # Format datetime string outside the f-string
        report_time_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        report.append(f"**Report Generated:** {report_time_str}") 
        report.append("\n---")

        # --- Executive Summary ---
        report.append("## Executive Summary")
        report.append(executive_summary)
        report.append("\n---")

        # --- Top N Suggestions ---
        report.append(f"## Top {top_n} Actionable Suggestions (Prioritized)")
        if prioritized_suggestions:
            for i, sugg in enumerate(prioritized_suggestions[:top_n]):
                # Use single quotes for dictionary keys inside f-string
                report.append(f"{i+1}. **{sugg.get('suggestion', 'N/A')}**")
                report.append(f"   - *Impact:* {sugg.get('impact', 'N/A')}, *Difficulty:* {sugg.get('difficulty', 'N/A')}, *Source:* {sugg.get('source', 'Unknown')}")
        else:
            report.append("No suggestions were generated.")
        report.append("\n---")

        # --- Detailed Analysis Breakdown ---
        report.append("## Detailed Analysis Breakdown")
        for analyzer_name, result in analysis_results.items():
            # Use single quotes for dictionary keys inside f-string
            report.append(f"### {analyzer_name.replace('_', ' ').title()}")
            report.append(f"**Assessment:** {result.get('assessment', 'N/A')}")
            if result.get("positive_feedback"): 
                report.append(f"**Positive Feedback:** {result.get('positive_feedback')}")
            if result.get("persona_pain_points"): # Specific to Readability
                 report.append(f"**Potential Persona Pain Points:** {result.get('persona_pain_points')}")
            if result.get("quantified_issues"): # Specific to Structure/Flow
                 report.append(f"**Quantified Issues:** {result.get('quantified_issues')}")
            if result.get("snippet_specific_feedback"): # Specific to Style
                 report.append(f"**Snippet-Specific Feedback:** {result.get('snippet_specific_feedback')}")
            
            suggestions = result.get("suggestions", [])
            if suggestions:
                report.append("**Suggestions:**")
                for sugg in suggestions:
                    report.append(f"- {sugg}") # Suggestions from raw analysis might be just strings
            report.append("") # Add a newline for spacing
        report.append("\n---")

        # --- Thematically Grouped Suggestions ---
        report.append("## All Suggestions by Theme (Prioritized)")
        if grouped_suggestions:
            for theme, suggestions_in_theme in grouped_suggestions.items():
                report.append(f"### {theme}")
                if suggestions_in_theme:
                    for i, sugg in enumerate(suggestions_in_theme):
                        # Use single quotes for dictionary keys inside f-string
                        report.append(f"{i+1}. **{sugg.get('suggestion', 'N/A')}**")
                        report.append(f"   - *Impact:* {sugg.get('impact', 'N/A')}, *Difficulty:* {sugg.get('difficulty', 'N/A')}, *Source:* {sugg.get('source', 'Unknown')}")
                else:
                    report.append("No suggestions in this theme.")
                report.append("") # Add a newline for spacing
        else:
            report.append("Suggestions could not be grouped thematically.")
            if prioritized_suggestions: # List all if grouping failed but prioritization worked
                 report.append("\n**Full Prioritized List:**")
                 for i, sugg in enumerate(prioritized_suggestions):
                    # Use single quotes for dictionary keys inside f-string
                    report.append(f"{i+1}. **{sugg.get('suggestion', 'N/A')}**")
                    report.append(f"   - *Impact:* {sugg.get('impact', 'N/A')}, *Difficulty:* {sugg.get('difficulty', 'N/A')}, *Source:* {sugg.get('source', 'Unknown')}")
            else:
                 report.append("No suggestions available.")

        report.append("\n---")
        report.append("*End of Report*")

        return "\n".join(report)

