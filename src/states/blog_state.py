# src/states/blog_state.py
from typing import List, Optional, Literal
from typing_extensions import TypedDict

class BlogState(TypedDict, total=False):
    # Inputs
    topic: str                     # required input for topic-based generation
    language: Optional[str]        # e.g., "en", "hi", "es" ... used by translation/summarization
    action: Optional[Literal["translate", "summarize", "none"]]

    # Outputs / intermediate
    title: str
    html: str
    images: List[str]              # list of image URLs
    image_attribution: Optional[str]
