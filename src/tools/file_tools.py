import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Ensure output directory exists
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def save_markdown_report(title: str, content: str) -> str:
    """
    Saves the provided markdown content to a file.
    This tool is given to the Report Agent.
    """
    safe_title = "".join([c if c.isalnum() else "_" for c in title]).lower()
    filepath = OUTPUT_DIR / f"{safe_title}.md"
    
    logger.info(f"Saving report to {filepath}")
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully saved report to {filepath.absolute()}"
    except Exception as e:
        return f"Failed to save report: {str(e)}"
