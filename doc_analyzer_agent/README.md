# AI-Powered Documentation Analyzer Agent

## Overview

This project, developed as part of a technical internship assignment, is an AI-powered agent designed to analyze online documentation articles. It fetches content from a provided URL, parses it, and leverages the Google Gemini language model to evaluate the documentation based on criteria like readability, structure, flow, completeness, examples, and style adherence. The agent then generates a comprehensive report with an executive summary and actionable suggestions for improvement, categorized thematically and prioritized by impact and difficulty.

This README provides instructions for setting up the project, running the agent, and troubleshooting common issues.

## Project Structure

```
doc_analyzer_agent/
├── src/                      # Source code
│   ├── __init__.py
│   ├── main.py             # Main script to run the pipeline
│   ├── config.py           # Configuration (loads API key from .env)
│   ├── core/               # Core components
│   │   ├── __init__.py
│   │   ├── fetcher.py      # Web content fetching (using Playwright)
│   │   ├── parser.py       # HTML parsing
│   │   └── llm_service.py  # Gemini API interaction
│   ├── analyzers/          # Specific analysis modules
│   │   ├── __init__.py
│   │   ├── readability.py
│   │   ├── structure_flow.py
│   │   ├── completeness_examples.py
│   │   └── style_adherence.py
│   ├── processing/         # Suggestion processing & summary
│   │   ├── __init__.py
│   │   ├── aggregator.py
│   │   ├── prioritizer.py
│   │   ├── grouper.py
│   │   └── summary_generator.py
│   └── reporting/          # Report formatting
│       ├── __init__.py
│       └── formatter.py
├── .env.example            # Example environment file
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
└── README.md               # This file
```
*(Note: The final code package includes the `.env.example` and `.gitignore` files)*

## Setup Instructions

Follow these steps to set up the project environment on your local machine:

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd doc_analyzer_agent
    ```

2.  **Create and Activate Virtual Environment (Recommended):**
    Using a virtual environment prevents dependency conflicts.
    ```bash
    # Create the environment (use python3 or python depending on your system)
    python -m venv venv 
    
    # Activate the environment
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows (Command Prompt):
    # venv\Scripts\activate
    # On Windows (PowerShell):
    # .\venv\Scripts\Activate.ps1
    ```
    You should see `(venv)` at the beginning of your terminal prompt.


    After the above step follow these exact commands to install the requirements

    1. cd doc_analyzer_agent

    after changing the path into these directory you can install all the library using the below command

3.  **Install Dependencies:**
    Install all required Python packages from `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright Browsers:**
    Playwright requires browser binaries to function. Run this command (it might take a few minutes):
    ```bash
    playwright install
    ```
    This typically installs Chromium, Firefox, and WebKit.

5.  **Set Up API Key:**
    This agent requires a Google Gemini API key.
    *   There is a file named as .env where you needed to place your gemini api key
        ```
        GEMINI_API_KEY=YOUR_API_KEY_HERE
        ```
    *   Replace `YOUR_API_KEY_HERE` with your actual Google Gemini API key.
    *   The `.gitignore` file is configured to prevent accidentally committing your `.env` file.

## How to Run

1.  Ensure your virtual environment is activated.
2.  Make sure your `.env` file with the API key is present in the project root.
3.  Navigate to the `src` directory:
    ```bash
    cd src
    ```
4.  Run the main script, optionally providing a URL:
    ```bash
    # Analyze the default URL (if specified in main.py, otherwise might error)
    python main.py 
    
    # Analyze a specific URL
    python main.py https://example.com/docs/some-article
    ```

The script will output progress messages to the console and, upon completion, save the detailed analysis report as `analysis_report.md` in the `src` directory.

## Troubleshooting Common Issues

*   **`403 Client Error: Forbidden` during Fetching:**
    *   *Cause:* The target website is blocking direct script access (e.g., using Cloudflare).
    *   *Solution:* This project uses Playwright in `src/core/fetcher.py` specifically to overcome this by simulating a real browser. Ensure Playwright browsers are installed (`playwright install`). If errors persist, the website might have even stricter protections.

*   **`google.api_core.exceptions.PermissionDenied: 403 API key not valid` (or similar API key errors):**
    *   *Cause 1:* The `GEMINI_API_KEY` is missing, incorrect, or hasn't been loaded properly.
    *   *Solution 1:* Double-check that the `.env` file exists in the project root directory (NOT the `src` directory), contains the correct key (`GEMINI_API_KEY=...`), and that you saved the file.
    *   *Cause 2:* The API key might be disabled or lack the necessary permissions in your Google Cloud/AI Studio project.
    *   *Solution 2:* Verify the API key status and permissions in the Google console.

*   **`ModuleNotFoundError: No module named '...'`:**
    *   *Cause 1:* The virtual environment is not activated.
    *   *Solution 1:* Activate the `venv` using the appropriate command for your OS (see Setup step 2).
    *   *Cause 2:* Dependencies were not installed correctly.
    *   *Solution 2:* Ensure you are in the project root directory (where `requirements.txt` is) with the virtual environment active, and run `pip install -r requirements.txt` again.

*   **Playwright Errors (e.g., `Executable doesn't exist at...`):**
    *   *Cause:* The necessary Playwright browser binaries were not installed.
    *   *Solution:* Run `playwright install` in your terminal (with the virtual environment active).

*   **`SyntaxError` (e.g., `f-string expression part cannot include a backslash`):**
    *   *Cause:* This specific error plagued earlier development versions due to incorrect escaping within f-strings. The current code *should* be free of this.
    *   *Solution:* If you encounter this unexpectedly, ensure you have the latest version of the code files (`grouper.py`, `summary_generator.py`) and that no copy-paste errors introduced backslashes inside f-string expressions (`{...}`).

*   **LLM JSON Parsing Errors (Warnings in output):**
    *   *Cause:* The LLM might occasionally return a response that isn't perfectly formatted JSON, despite the prompt instructions.
    *   *Solution:* The code includes basic cleaning (removing markdown fences) and `try-except` blocks for JSON parsing. While it attempts to handle minor deviations, significantly malformed responses might lead to warnings or fallback behavior (like grouping by source or using a basic summary). This reflects the probabilistic nature of LLMs.

## How It Works (Briefly)

1.  **Fetch & Parse:** Playwright fetches the URL's HTML, which is then parsed by BeautifulSoup and converted to Markdown.
2.  **Analyze:** The Markdown content is sent to different analyzer modules, each querying the Gemini LLM with specific prompts to assess readability, structure, etc.
3.  **Process Suggestions:** Suggestions from all analyzers are aggregated, prioritized (using LLM scoring), and grouped thematically (using LLM grouping).
4.  **Summarize:** An executive summary is generated by the LLM based on the findings.
5.  **Report:** All results are formatted into a final Markdown report.

*(For a detailed architecture breakdown and discussion of the development process, please refer to the accompanying PDF report: `Internship_Assignment_Report.pdf`)*

## Assignment Scope

This implementation focuses on fulfilling **Task 1** (Documentation Analysis Agent) of the internship assignment. Task 2 (Revision Agent) is not included.
