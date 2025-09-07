from langchain_openai import ChatOpenAI
from .tools import get_recommendations,lookup_titles,get_movie_info
from .prompt_library import system_prompt
import os

from langgraph.prebuilt import create_react_agent

class Hypatia:
    def __init__(self, memory):
        self.establish_llm()
        self.toolkit = [
            get_recommendations,
            lookup_titles,
            get_movie_info
        ]

        self.memory_store = memory

        self.establish_agent()
    def establish_llm(self, **kwargs):
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            api_key=os.environ["OPENAI_API_KEY"],
            temperature=0.2,
            streaming=False,
            max_completion_tokens = 1000,
            **kwargs
        )
    def invoke(self, query: str, conversation_id):
        config = {"configurable": {"thread_id": conversation_id}}

        messages = self.agent.invoke({
            "messages": [
                ("user", query)
            ]
        }, config)
        return messages["messages"][-1].content
    
    def establish_agent(self):
        self.agent = create_react_agent(
            model = self.llm,
            tools = self.toolkit,
            prompt = system_prompt,
            checkpointer=self.memory_store,
            debug = True
        )
    
