from src.states.blog_state import BlogState


class BlogNode:
    """
    A class to represent the blog node
    """

    def __init__(self,llm) -> None:
        self.llm=llm

    def title_creation(self,state:BlogState):
        """
        create a title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""
            You are an expert blog content writer. Use simple text. 
            Generate a single blog title for the {topic}. This title should be creative
            and seo friendly. Give the title directly.
            """

            system_message=prompt.format(topic=state['topic'])
            response = self.llm.invoke(system_message)
            return {'blog':{'title':response.content}}
        
    
    def content_generation(self,state:BlogState):
        """
        create a meaningful content for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""
            You are an expert blog content writer. Use HTML formatting. 
            Generate a detailed blog content with detailed breakdown for the {topic}. This description should be creative
            and seo friendly. Use semantic html tags with proper formatting. DO NOT include title and give only the blog content. DO NOT use any special characters like - ",**,;,/ or anything that breaks or makes bad html.
            """

            system_message=prompt.format(topic=state['topic'])
            response = self.llm.invoke(system_message)
            return {'blog':{'content':response.content}}
        
    