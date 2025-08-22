# src/graphs/graph_builder.py
from langgraph.graph import StateGraph, START, END
from src.states.blog_state import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self, llm) -> None:
        self.llm = llm
        # NOTE: We'll reset self.graph inside each builder to avoid node duplication across builds.
        self.graph: StateGraph = StateGraph(BlogState)

    def build_topic_graph(self) -> StateGraph:
        """
        Build a graph to generate blogs based on topic.
        title_creation -> content_generation -> get_images -> END
        """
        # Fresh graph for this build
        self.graph = StateGraph(BlogState)
        self.blog_node_obj = BlogNode(self.llm)

        # Nodes
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation", self.blog_node_obj.content_generation)
        self.graph.add_node("get_images", self.blog_node_obj.get_images)

        # Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "get_images")
        self.graph.add_edge("get_images", END)

        return self.graph

    def build_language_graph(self) -> StateGraph:
        """
        Build a graph for blog generation with inputs: topic, plus optional language/action.
        After content_generation, we:
          - always try get_images
          - also route to optional post-steps (translation/summarization)
        """
        # Fresh graph for this build
        self.graph = StateGraph(BlogState)
        self.blog_node_obj = BlogNode(self.llm)

        # Nodes
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation", self.blog_node_obj.content_generation)
        self.graph.add_node("get_images", self.blog_node_obj.get_images)

        # Router node + post-processing nodes
        self.graph.add_node("route", self.blog_node_obj.route)
        self.graph.add_node("translation", self.blog_node_obj.translation)
        self.graph.add_node("summarization", self.blog_node_obj.summarization)

        # Edges & conditional edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "get_images")
        self.graph.add_edge("content_generation", "route")

        # Conditional routing:
        # - 'translate'  -> 'translation'
        # - 'summarize'  -> 'summarization'
        # - '__end__'    -> END
        self.graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "translate": "translation",
                "summarize": "summarization",
                "__end__": END,
            },
        )

        # End points
        self.graph.add_edge("translation", END)
        self.graph.add_edge("summarization", END)
        self.graph.add_edge("get_images", END)

        return self.graph

    def setup_graph(self, usecase: str):
        if usecase == "topic":
            g = self.build_topic_graph()
            return g.compile()
        if usecase == "language":
            g = self.build_language_graph()
            return g.compile()

        # default: topic graph
        return self.build_topic_graph().compile()


# --- Below code is for LangSmith / LangGraph Studio convenience ---
if __name__ == "__main__":
    from src.llms.groqllm import GroqLLM

    llm = GroqLLM().get_llm()
    builder = GraphBuilder(llm)
    graph = builder.build_topic_graph().compile()
