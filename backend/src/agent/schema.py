from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from typing import TypedDict, Annotated


class InputSchema(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]