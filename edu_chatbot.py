from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton
from googleapiclient.discovery import build
import pyttsx3

# === Replace these with your API Key and CSE ID ===
API_KEY = 'AIzaSyAY9LY3kHYdG-6PtUGMppk3hUoZmICfdr0'    # <-- Put your API key here (in quotes)
CSE_ID = '8799236735ee747ad'      # <-- Put your CSE ID here (in quotes)

def google_search(query):
    try:
        service = build("customsearch", "v1", developerKey=API_KEY)
        res = service.cse().list(q=query, cx=CSE_ID, num=1).execute()
        if 'items' in res:
            item = res['items'][0]
            answer = item.get('snippet', "No answer available.")
            link = item.get('link', "")
            return answer, link
        else:
            return "Sorry, I couldn't find an answer.", ""
    except Exception as e:
        return f"Error: {str(e)}", ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

class ChatbotUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Educational Chatbot")
        self.resize(600, 400)
        self.layout = QVBoxLayout()
        
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter your question...")
        self.send_btn = QPushButton("Ask!")
        
        self.send_btn.clicked.connect(self.respond)
        self.input.returnPressed.connect(self.respond)
        
        self.layout.addWidget(self.chat_area)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.send_btn)
        self.setLayout(self.layout)
        
    def respond(self):
        user_text = self.input.text().strip()
        if not user_text:
            return
        self.chat_area.append(f"You: {user_text}")
        answer, link = google_search(user_text)
        bot_response = f"Bot: {answer}"
        if link:
            bot_response += f"\nSource: {link}"
        self.chat_area.append(bot_response)
        speak(answer)
        self.input.clear()

if __name__ == "__main__":
    app = QApplication([])
    win = ChatbotUI()
    win.show()
    app.exec_()
