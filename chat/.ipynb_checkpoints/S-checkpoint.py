import socket
import threading

# 서버에 접속하는 클라이언트 처리 함수
def handle_client(client_socket, client_address):
    print(f"💻 클라이언트 {client_address}가 연결되었습니다.")
    client_socket.send("👋 안녕하세요! 서버에 연결되었습니다.".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"클라이언트 {client_address}로부터 받은 메시지: {message}")
        except:
            break

    print(f"💻 클라이언트 {client_address}가 연결을 종료했습니다.")
    client_socket.close()

# 서버 시작 함수
def start_server():
    host = "192.168.35.99"  # 서버 IP 주소
    port = 6969  # 포트 번호

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 서버 소켓 바인딩
    try:
        server_socket.bind((host, port))
    except OSError as e:
        print(f"❌ 포트를 사용할 수 없습니다: {e}")
        return
    
    server_socket.listen(5)
    print(f"🚀 서버가 {host}:{port}에서 실행 중입니다...")
    print("💬 서버에 접속한 클라이언트의 메시지를 처리합니다.")
    print("💬 서버에서 메시지를 입력하면 클라이언트로 전송됩니다.")

    client_sockets = []  # 연결된 클라이언트 소켓을 저장하는 리스트

    # 클라이언트 접속 처리
    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

        # 클라이언트 소켓 리스트에 추가
        client_sockets.append(client_socket)

        # 서버에서 메시지 입력 받기
        while True:
            message_to_send = input(":")
            if message_to_send.lower() == 'exit':
                print("✅ 서버가 종료되었습니다.")
                # 모든 클라이언트 소켓 닫기
                for sock in client_sockets:
                    sock.close()
                server_socket.close()  # 서버 소켓 닫기
                return  # 서버 종료
            else:
                # 연결된 클라이언트들에게 메시지를 전송
                for sock in client_sockets:
                    try:
                        sock.send(message_to_send.encode())
                    except:
                        # 연결이 끊어진 클라이언트 소켓은 리스트에서 제거
                        client_sockets.remove(sock)
                        sock.close()

# 서버 실행 여부 묻기
def ask_to_start_server():
    start = input("서버를 시작하시겠습니까? (yes/no): ").strip().lower()
    if start == 'yes':
        start_server()
    else:
        print("서버 실행이 취소되었습니다.")

# 프로그램 실행 시작
if __name__ == "__main__":
    ask_to_start_server()  # 서버 시작 여부 묻기
