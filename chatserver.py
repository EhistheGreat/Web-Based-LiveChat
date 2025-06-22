from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data on server
Session(app)

socketio = SocketIO(app, manage_session=False)

@app.route('/')
def index():
    return render_template('chat1.html')

@socketio.on('connect')
def handle_connect():
    print('New user connected')

@socketio.on('set_username')
def handle_username(username):
    session['username'] = username
    send(f"{username} has joined the chat!", broadcast=True)

@socketio.on('message')
def handle_message(msg):
    username = session.get('username', 'Anonymous')
    full_msg = f"[{username}]: {msg}"
    print(full_msg)
    send(full_msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)

