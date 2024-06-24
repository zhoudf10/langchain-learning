# app.py
from flask import Flask, render_template
from langchain_community.llms import ollama
from langchain_core.prompts import ChatPromptTemplate
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# 创建 Ollama 实例
llm = ollama.Ollama(model="llama8b")

# 创建消息模板
template = ChatPromptTemplate.from_messages([
    ("system", "你是一个中文机器人,用中文回复"),
    ("human", "{user_input}"),
])

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    # 这里可以添加逻辑来处理消息，然后流式发送响应
    for response_chunk in generate_response(msg):
        emit('stream', response_chunk)
    # emit('finished', 'Finished streaming response.')
    emit('finished', '\n')

def generate_response(user_input):
    # 填充模板并生成 prompt_value
    prompt_value = template.invoke({"user_input": f"{user_input}"})
    
    # 获取流式消息
    messages = llm.stream(prompt_value)
    for chunk in messages:
            yield f"{chunk}\n"

if __name__ == '__main__':
    socketio.run(app, debug=True)