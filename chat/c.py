import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import time

# 서버 주소와 포트
host = '192.168.35.99'  # 서버 IP 주소
port = 6969  # 서버 포트

# 소켓 초기화
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버로부터 메시지를 받는 함수
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # 메인 스레드에서 GUI를 업데이트하도록 요청
                chat_box.after(0, update_chat_box, message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# 메시지 보내기 함수
def send_message(event=None):  # 엔터키 이벤트를 받을 수 있게 수정
    message = entry_message.get()
    if message:
        # 자신이 보낸 메시지를 먼저 채팅창에 표시
        chat_box.after(0, update_chat_box, f"[{time.strftime('%H:%M:%S')}] [{client_name}] {message}")
        
        # 메시지를 서버로 전송
        client_socket.send(f"[{time.strftime('%H:%M:%S')}] [{client_name}] {message}".encode('utf-8'))
        
        entry_message.delete(0, tk.END)  # 입력창 초기화

# 채팅창 업데이트 함수 (GUI 업데이트)
def update_chat_box(message):
    chat_box.config(state=tk.NORMAL)  # 텍스트 박스를 수정 가능하게 설정
    chat_box.insert(tk.END, f"{message}\n")
    chat_box.yview(tk.END)  # 스크롤을 최신 메시지로 이동
    chat_box.config(state=tk.DISABLED)  # 다시 텍스트 박스를 수정 불가능하게 설정

# 이름 입력 화면 (GUI로 이름 입력받기)
def show_name_input_screen():
    def start_chat(event=None):
        global client_name
        client_name = entry_name.get()  # 입력받은 이름을 클라이언트 이름으로 설정
        if client_name:  # 이름이 비어있지 않으면
            name_input_window.destroy()  # 이름 입력 창 닫기
            start_chat_window()  # 채팅 화면 시작
    
    # 이름 입력 화면 생성
    name_input_window = tk.Tk()
    name_input_window.title("wave chat")
    name_input_window.geometry("300x400")
    name_input_window.configure(bg="#CBDDF5")  # 전체 배경을 파란색으로 설정

    # 아이콘 설정 (아이콘 파일 경로는 실제 아이콘 파일로 바꿔주세요)
    name_input_window.iconbitmap("w.ico")  # 아이콘 파일 설정

    # 중앙 정렬을 위한 Frame 추가
    frame = tk.Frame(name_input_window, bg="#CBDDF5")  # Frame 배경도 파란색으로 설정
    frame.pack(expand=True)  # 화면 중앙에 배치
    
    # 'W'는 크고 흰색으로 설정
    label_W = tk.Label(frame, text="W", font=("Comic Sans MS", 40, "bold"), fg="white", bg="#CBDDF5")
    label_W.pack(pady=5)
    
    # 'wave chat'은 작은 글씨로 설정, 흰색으로
    label_wave_chat = tk.Label(frame, text="wave chat", font=("Comic Sans MS", 12), fg="white", bg="#CBDDF5")
    label_wave_chat.pack(pady=5)
    
    # 이름 입력 필드
    entry_name = tk.Entry(frame, font=("나눔고딕", 12))
    entry_name.pack(pady=10)
    
    # 엔터키 이벤트 바인딩
    entry_name.bind("<Return>", start_chat)
    
    name_input_window.mainloop()  # 이름 입력 창 실행

# 채팅 화면 시작
def start_chat_window():
    # 클라이언트 소켓 서버에 연결
    client_socket.connect((host, port))
    
    # Tkinter GUI 설정
    root = tk.Tk()
    root.title("wave chat")
    root.geometry("300x400")  # 창 크기 설정
    root.configure(bg="#CBDDF5")  # 배경색을 #CBDDF5 파란색으로 설정
    # 아이콘 설정 (아이콘 파일 경로는 실제 아이콘 파일로 바꿔주세요)
    root.iconbitmap("w.ico")  # 아이콘 파일 설정
    
    # Grid 레이아웃 설정
    root.grid_rowconfigure(0, weight=1)  # 첫 번째 행에 크기 비율 설정
    root.grid_rowconfigure(1, weight=0)  # 두 번째 행은 비율을 설정하지 않음
    root.grid_columnconfigure(0, weight=1)  # 첫 번째 열에 크기 비율 설정
    root.grid_columnconfigure(1, weight=0)  # 두 번째 열은 비율을 설정하지 않음
    
    # 채팅 화면 (스크롤바가 없는 텍스트 영역)
    global chat_box
    chat_box = tk.Text(root, width=70, height=15, wrap=tk.WORD, state=tk.DISABLED, font=("나눔고딕", 12), bg="#ffffff", fg="#333333", bd=1, relief="solid")
    chat_box.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")  # 크기에 맞게 확대
    
    # 메시지 입력 창
    global entry_message
    entry_message = tk.Entry(root, font=("나눔고딕", 12), bd=1, relief="solid")
    entry_message.grid(row=3,columnspan=2, column=0, padx=20, pady=20, sticky="ew")  # 수평으로 크기 맞추기
    
    # 엔터키 이벤트 바인딩 (보내기 버튼 대신 엔터키로 메시지 전송)
    entry_message.bind("<Return>", send_message)  # 엔터키 누르면 send_message 함수 실행
    
    # 서버로부터 메시지 받기 시작 (별도의 스레드에서)
    threading.Thread(target=receive_messages, daemon=True).start()

    # GUI 실행
    root.mainloop()

# 프로그램 실행 시작
if __name__ == "__main__":
    show_name_input_screen()  # 이름 설정 화면 시작
