import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
import os
from dotenv import load_dotenv
load_dotenv()

app=FastAPI()

os.environ["LANGSMITH_API_KEY"]=os.getenv('LANGSMITH_API_KEY','')

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to ["http://localhost:3000"] or your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## apis

@app.post('/blogs')
async def create_blogs(request:Request):
    data=await request.json()
    topic=data.get("topic","")

    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required to generate a blog")

    ## get llm

    groqllm = GroqLLM()
    llm=groqllm.get_llm()

    ## get the graph

    graph_builder=GraphBuilder(llm)
    if topic:
        graph=graph_builder.setup_graph(usecase="topic")
        state=graph.invoke({'topic':topic}) # type: ignore
    
        return {"data":state} # type: ignore
    
    else:
        return {"data":""}

if __name__=="__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=8000,reload=True)
