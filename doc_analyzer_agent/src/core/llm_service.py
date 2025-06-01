import google.generativeai as genai
import json
import time
import config # Use absolute import assuming src is in sys.path

class LLMService:
    """Provides an interface to interact with the configured LLM API (Google Gemini)."""

    def __init__(self):
        """Initializes the LLMService, configuring the Gemini API."""
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL_NAME)
        print(f"LLM Service initialized with model: {config.GEMINI_MODEL_NAME}")

    def query_llm(self, prompt: str, retries: int = 3, delay: int = 5) -> dict | str | None:
        """Sends a prompt to the configured LLM and attempts to parse the JSON response.

        Args:
            prompt: The prompt string to send to the LLM.
            retries: Number of times to retry the API call in case of failure.
            delay: Delay in seconds between retries.

        Returns:
            A dictionary if the LLM returns valid JSON, otherwise the raw text response,
            or None if the API call fails after retries.
        """
        for attempt in range(retries):
            try:
                print(f"\n--- Sending prompt to LLM (Attempt {attempt + 1}/{retries}) ---")
                # print(prompt) # Uncomment for debugging prompts
                print("-----------------------------------------------------")
                
                response = self.model.generate_content(prompt)
                
                # Check for safety ratings or blocks
                if not response.candidates:
                     print(f"Warning: LLM response blocked or empty. Prompt: {prompt[:100]}...")
                     # You might want to inspect response.prompt_feedback here
                     # print(f"Prompt Feedback: {response.prompt_feedback}")
                     # Depending on the block reason, you might retry or return None
                     # For now, let's treat it as a failure for this attempt
                     raise Exception(f"LLM response blocked or empty. Feedback: {response.prompt_feedback}")

                raw_response_text = response.text
                print("--- Received LLM Response ---")
                # print(raw_response_text) # Uncomment for debugging responses
                print("---------------------------")

                # Attempt to parse as JSON, assuming the prompt asked for it
                try:
                    # Clean the response text: remove potential markdown code fences
                    cleaned_response = raw_response_text.strip()
                    if cleaned_response.startswith("```json"):
                        cleaned_response = cleaned_response[7:]
                    if cleaned_response.endswith("```"):
                        cleaned_response = cleaned_response[:-3]
                    cleaned_response = cleaned_response.strip()
                    
                    parsed_json = json.loads(cleaned_response)
                    return parsed_json
                except json.JSONDecodeError:
                    print("Warning: LLM response was not valid JSON. Returning raw text.")
                    return raw_response_text # Return raw text if JSON parsing fails

            except Exception as e:
                print(f"Error querying LLM (Attempt {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("LLM query failed after multiple retries.")
                    return None
        return None # Should not be reached if retries > 0, but added for safety

