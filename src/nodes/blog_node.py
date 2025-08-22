# src/nodes/blog_node.py
from typing import Any, Dict
from src.states.blog_state import BlogState
from src.tools.image_tool import ImageFetcher

class BlogNode:
    """
    Node implementations for the blog graph.
    Each node takes the current state dict and returns a partial state dict to merge.
    """
    def __init__(self, llm: Any) -> None:
        self.llm = llm
        self.image_fetcher = ImageFetcher()

    # --- Core Generation ---

    def title_creation(self, state: BlogState) -> Dict[str, Any]:
        topic = (state.get("topic") or "").strip()
        language = (state.get("language") or "en").strip()

        if not topic:
            # Nothing to do if there's no topic; let upstream validation handle errors
            return {}

        prompt = (
            f"Generate a concise, catchy, SEO-friendly blog title in {language}. "
            f"Topic: {topic}\n"
            "Return ONLY the title text without quotes or extra lines."
        )
        resp = self.llm.invoke(prompt)
        title = getattr(resp, "content", str(resp)).strip()
        return {"title": title}

    def content_generation(self, state: BlogState) -> Dict[str, Any]:
        topic = state.get("topic", "").strip()
        title = (state.get("title") or f"Blog on {topic or 'Selected Topic'}").strip()
        language = (state.get("language") or "en").strip()

        prompt = f"""
You are an expert writer. Write a well-structured blog as **valid HTML** in {language}.

Requirements:
- Include a main title as <h1>{title}</h1>.
- Use semantic sections with <h2> and <h3>.
- Use short paragraphs, bullet points where helpful (<ul><li>...</li></ul>).
- Add a brief introduction and conclusion.
- Do NOT include external CSS/JS, inline styles allowed minimally.
- Do NOT include <html>, <head>, or <body> tags. Return only the inner HTML.

Topic: {topic}
"""
        resp = self.llm.invoke(prompt)
        html = getattr(resp, "content", str(resp)).strip()
        return {"html": html}

    # --- Media / Tools ---

    def get_images(self, state: BlogState) -> Dict[str, Any]:
        """
        Fetch a cover image for the blog and optionally inject it at the top of HTML.
        """
        topic_or_title = (state.get("title") or state.get("topic") or "").strip()
        if not topic_or_title:
            return {}

        result = self.image_fetcher.fetch_cover_image(topic_or_title)
        images = list(state.get("images") or [])
        images.insert(0, result.url)

        html = state.get("html", "")
        banner = (
            f'<img src="{result.url}" alt="{topic_or_title}" '
            f'style="max-width:100%;height:auto;border-radius:12px;margin:16px 0;" />'
        )
        # Simple heuristic: prepend banner
        merged_html = f"{banner}\n{html}" if html else banner

        return {"images": images, "image_attribution": result.attribution, "html": merged_html}

    # --- Routing ---

    def route(self, state: BlogState) -> Dict[str, Any]:
        """
        Pass-through node (required so add_conditional_edges can attach to a node).
        Returns state unchanged.
        """
        return {}

    def route_decision(self, state: BlogState) -> str:
        """
        Decide the next step after content generation:
        - 'translate'  -> go to translation
        - 'summarize'  -> go to summarization
        - '__end__'    -> finish
        """
        action = (state.get("action") or "none").strip().lower()
        language = (state.get("language") or "").strip().lower()

        if action == "summarize":
            return "summarize"
        if action == "translate" and language and language not in ("", "en"):
            return "translate"
        return "__end__"

    # --- Post-processing routes ---

    def translation(self, state: BlogState) -> Dict[str, Any]:
        """
        Translate the generated HTML into the target `language`.
        HTML structure must be preserved; translate only text content.
        """
        target_lang = (state.get("language") or "").strip()
        html = state.get("html", "").strip()
        if not target_lang or not html:
            return {}

        prompt = f"""
Translate the following HTML into {target_lang}.
- Keep all HTML tags and structure unchanged.
- Translate only the visible text content.
- Return ONLY the translated HTML (no extra commentary).

HTML:
{html}
"""
        resp = self.llm.invoke(prompt)
        out_html = getattr(resp, "content", str(resp)).strip()
        return {"html": out_html}

    def summarization(self, state: BlogState) -> Dict[str, Any]:
        """
        Produce a concise summary (TL;DR) of the HTML in the same or specified `language`.
        Return valid HTML (e.g., <h2>Summary</h2><ul><li>...</li></ul>).
        """
        html = state.get("html", "").strip()
        language = (state.get("language") or "en").strip()
        if not html:
            return {}

        prompt = f"""
Summarize the following blog content into a concise HTML summary in {language}.
- Use <h2>Summary</h2> followed by a short bullet list (<ul><li>...</li></ul>).
- Keep it factual, non-repetitive, and easy to scan.
- Return ONLY the summary HTML.

Content:
{html}
"""
        resp = self.llm.invoke(prompt)
        summary_html = getattr(resp, "content", str(resp)).strip()
        return {"html": summary_html}
