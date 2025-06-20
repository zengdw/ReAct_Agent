import os
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from agent.configuration import Configuration
from agent.schema import InputSchema
from agent.prompt import get_current_date, answer_instructions


def llm_node(state: InputSchema, config: RunnableConfig):
    configurable = Configuration.from_runnable_config(config)
    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3-0324:free",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )
    prompt = answer_instructions.format(
        current_date=get_current_date(),
        question_topic="",
        summaries="",
        question=state["messages"][-1].content,
    )

    response = llm.invoke(prompt)
    return {"messages": [response]}


graph_builder = StateGraph(InputSchema, Configuration)
graph_builder.add_node("llm", llm_node)
graph_builder.add_edge(START, "llm")
graph_builder.add_edge("llm", END)
graph = graph_builder.compile(checkpointer=InMemorySaver())
