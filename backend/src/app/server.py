from os import path
import sys
import uuid

from flask import Flask, Response, request, stream_with_context
from flask_cors import CORS

sys.path.append(path.abspath(path.join(path.dirname(__file__), "..")))
from agent.graph import graph


app = Flask(__name__)
CORS(app)


@app.route("/sse", methods=["POST"])
def sse():
    data = request.get_json(force=True)
    question = data.get("question", "")

    # 获取header中的threadId参数
    thread_id = request.headers.get("thread_id")
    if not thread_id:
        thread_id = str(uuid.uuid4())

    def event_stream():
        """生成SSE事件流的生成器函数"""
        config = {"configurable": {"thread_id": thread_id}}
        for event in graph.stream(
            {"messages": [{"role": "user", "content": question}]},
            config=config,
            stream_mode="messages",
        ):
            yield f"data: {event[0].content}\n\n"

    return Response(
        stream_with_context(event_stream()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "thread_id": thread_id,
        },
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
