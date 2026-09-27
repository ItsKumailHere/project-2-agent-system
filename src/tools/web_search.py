from duckduckgo_search import DDGS
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def search_web(query: str, max_results: int = 3) -> str:
    """
    Searches the web and returns snippets.
    This tool is given to the Research Agent.
    """
    logger.info(f"Searching web for: {query}")
    try:
        results = DDGS().text(query, max_results=max_results)
        
        formatted_results = []
        for r in results:
            formatted_results.append(f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}")
            
        return "\n\n---\n\n".join(formatted_results)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return f"Error performing search: {str(e)}"
