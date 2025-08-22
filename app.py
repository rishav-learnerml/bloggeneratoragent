# app.py (only show the changed bits)
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")

@app.post("/blogs")
async def create_blogs(request: Request):
    data = await request.json()
    topic = (data.get("topic") or "").strip()
    language = (data.get("language") or "").strip()
    action = (data.get("action") or "none").strip().lower()  # "translate" | "summarize" | "none"

    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required to generate a blog")

    llm = GroqLLM().get_llm()
    graph_builder = GraphBuilder(llm)

    # choose graph
    usecase = "language" if (language or action != "none") else "topic"
    graph = graph_builder.setup_graph(usecase=usecase)

    initial_state = {"topic": topic}
    if language:
        initial_state["language"] = language
    if action:
        initial_state["action"] = action

    state = graph.invoke(initial_state)
    return {"data": state.get("html", ""), "title": state.get("title", ""), "images": state.get("images", [])}
