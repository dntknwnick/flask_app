from app import create_app, db
from app.models import User, ExamCategory, Subject, Question, Option, UserExam, ExamAttempt
from config import Config
import socket

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'ExamCategory': ExamCategory,
        'Subject': Subject,
        'Question': Question,
        'Option': Option,
        'UserExam': UserExam,
        'ExamAttempt': ExamAttempt
    }

def get_ip_address():
    """Get the local IP address of the machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    host = '0.0.0.0'  # Listen on all available interfaces
    port = Config.PORT
    ip_address = get_ip_address()

    print(f"\n* Running on http://{ip_address}:{port}/ (Press CTRL+C to quit)")
    print(f"* Use this IP address in your React Native app: {ip_address}")
    print(f"* For Android emulator, use: 10.0.2.2:{port}\n")

    app.run(host=host, port=port, debug=True)
