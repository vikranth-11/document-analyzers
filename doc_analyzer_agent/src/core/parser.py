from bs4 import BeautifulSoup
import markdownify # Requires installation: pip install markdownify

class HTMLParser:
    """Parses HTML content to extract relevant text, preserving some structure."""

    def parse(self, html_content: str) -> str:
        """Parses the HTML content and converts it to Markdown.

        Args:
            html_content: The raw HTML content string.

        Returns:
            The parsed content as a Markdown string.
            Returns an empty string if parsing fails or content is empty.
        """
        if not html_content:
            return ""
        
        try:
            # Use BeautifulSoup to initially parse the HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # --- Attempt to find the main content area (specific to help.moengage.com) ---
            # This often improves quality by removing headers, footers, nav bars.
            # Inspecting the MoEngage page, the main article seems to be within <article> tag
            # or a div with a specific class like 'article-body'. Let's try 'article-body'.
            article_body = soup.find("div", class_="article-body")
            
            if article_body:
                # Convert the relevant part to Markdown
                # Use markdownify options for better formatting if needed
                md = markdownify.markdownify(str(article_body), heading_style="ATX")
            else:
                # Fallback: If specific content area isn't found, parse the whole body
                print("Warning: Could not find specific article body. Parsing entire HTML body.")
                # Exclude common noise tags if parsing the whole body
                for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
                    tag.decompose()
                md = markdownify.markdownify(str(soup.body), heading_style="ATX")

            return md.strip()
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return ""

