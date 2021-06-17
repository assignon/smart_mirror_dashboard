from app import app as application, socketio

if __name__ == "__main__":
    socketio.run(application)