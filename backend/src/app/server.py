import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, Response, stream_with_context, request
from agent.graph import graph

app = Flask(__name__)

@app.route('/sse', methods=['POST'])
def sse():
    data = request.get_json(force=True)
    question = data.get('question', '')
    def event_stream():
        config = {'configurable': {'thread_id': '1'}}
        for event in graph.stream({'messages': [{"role": "user", "content": question}]}, config=config, stream_mode=['messages', 'updates']):
            yield event[1][0].content
    return Response(stream_with_context(event_stream()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
