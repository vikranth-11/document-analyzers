# -*- coding: utf-8 -*-
"""Main script to run the documentation analysis pipeline."""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.fetcher import fetch_html_content
from core.parser import HTMLParser
from core.llm_service import LLMService
from analyzers.readability import ReadabilityAnalyzer
from analyzers.structure_flow import StructureFlowAnalyzer
from analyzers.completeness_examples import CompletenessExamplesAnalyzer
from analyzers.style_adherence import StyleAdherenceAnalyzer
from processing.aggregator import aggregate_suggestions # Need to create this simple aggregator
from processing.prioritizer import SuggestionPrioritizer
from processing.grouper import SuggestionGrouper
from processing.summary_generator import SummaryGenerator
from reporting.formatter import ReportFormatter
import config # To check if API key is set

def run_analysis(url: str):
    """Runs the full documentation analysis pipeline for a given URL."""
    print(f"Starting analysis for URL: {url}")

    # --- 0. Check API Key --- 
    if not config.GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set the environment variable before running.")
        print("Example: export GEMINI_API_KEY=\'YOUR_API_KEY\'")
        return

    # --- 1. Fetch Content --- 
    print("\n--- Fetching Content ---")
    html_content = fetch_html_content(url)
    if not html_content:
        print("Failed to fetch content. Exiting.")
        return
    print("Content fetched successfully.")

    # --- 2. Parse Content --- 
    print("\n--- Parsing Content ---")
    parser = HTMLParser()
    parsed_content = parser.parse(html_content)
    if not parsed_content:
        print("Failed to parse content or content is empty. Exiting.")
        return
    print("Content parsed successfully.")
    # print("\n--- Parsed Markdown (First 500 chars) ---")
    # print(parsed_content[:500] + "...")
    # print("-----------------------------------------")

    # --- 3. Initialize Services --- 
    print("\n--- Initializing Services ---")
    try:
        llm_service = LLMService()
    except ValueError as e:
        print(f"Error initializing LLM Service: {e}")
        return
        
    readability_analyzer = ReadabilityAnalyzer(llm_service)
    structure_analyzer = StructureFlowAnalyzer(llm_service)
    completeness_analyzer = CompletenessExamplesAnalyzer(llm_service)
    style_analyzer = StyleAdherenceAnalyzer(llm_service)
    prioritizer = SuggestionPrioritizer(llm_service)
    grouper = SuggestionGrouper(llm_service)
    summary_gen = SummaryGenerator(llm_service)
    formatter = ReportFormatter()
    print("Services initialized.")

    # --- 4. Run Analyzers --- 
    print("\n--- Running Analyzers ---")
    analysis_results = {}
    analysis_results["readability"] = readability_analyzer.analyze(parsed_content)
    print("Readability analysis complete.")
    analysis_results["structure_flow"] = structure_analyzer.analyze(parsed_content)
    print("Structure/Flow analysis complete.")
    analysis_results["completeness_examples"] = completeness_analyzer.analyze(parsed_content)
    print("Completeness/Examples analysis complete.")
    analysis_results["style_adherence"] = style_analyzer.analyze(parsed_content)
    print("Style Adherence analysis complete.")
    print("All analyzers finished.")

    # --- 5. Aggregate Suggestions --- 
    print("\n--- Aggregating Suggestions ---")
    all_suggestions = aggregate_suggestions(analysis_results)
    print(f"Aggregated {len(all_suggestions)} suggestions.")

    # --- 6. Prioritize Suggestions --- 
    print("\n--- Prioritizing Suggestions ---")
    prioritized_suggestions = prioritizer.prioritize(all_suggestions)
    print("Suggestions prioritized.")

    # --- 7. Group Suggestions --- 
    print("\n--- Grouping Suggestions ---")
    grouped_suggestions = grouper.group(prioritized_suggestions)
    print("Suggestions grouped thematically.")

    # --- 8. Generate Summary --- 
    print("\n--- Generating Summary ---")
    executive_summary = summary_gen.generate(analysis_results, grouped_suggestions)
    print("Executive summary generated.")

    # --- 9. Format Report --- 
    print("\n--- Formatting Report ---")
    final_report = formatter.format_report(
        url=url,
        analysis_results=analysis_results,
        prioritized_suggestions=prioritized_suggestions,
        grouped_suggestions=grouped_suggestions,
        executive_summary=executive_summary
    )
    print("Report formatted.")

    # --- 10. Output Report --- 
    print("\n--- Final Report ---")
    print(final_report)

    # Optionally save to file
    output_filename = "analysis_report.md"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(final_report)
        print(f"\nReport also saved to: {os.path.abspath(output_filename)}")
    except IOError as e:
        print(f"\nError saving report to file: {e}")

if __name__ == "__main__":
    target_url = "https://help.moengage.com/hc/en-us/articles/19708702327572-Raise-a-Support-Ticket-Through-MoEngage-Dashboard"
    if len(sys.argv) > 1:
        target_url = sys.argv[1] # Allow overriding URL via command line argument
    
    run_analysis(target_url)

