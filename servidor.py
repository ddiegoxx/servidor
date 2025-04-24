import socket
import threading
import time

# Configurações
HOST = '127.0.0.1'
PORT = 12345
TIMEOUT = 60  # segundos

clientes = {}
nomes = set()

def tratar_cliente(conn, addr):
    nome = None
    tempo_ultima_msg = time.time()

    try:
        while True:
            # Timeout
            if time.time() - tempo_ultima_msg > TIMEOUT:
                print(f"[TIMEOUT] Conexão de {addr} encerrada por inatividade.")
                break

            conn.settimeout(1.0)
            try:
                data = conn.recv(1024)
            except socket.timeout:
                continue  # volta para checar o timeout manual

            if not data:
                break

            tempo_ultima_msg = time.time()
            msg = data.decode().strip()
            print(f"[{addr}] {msg}")

            if msg.startswith("MSG: <NOME>"):
                candidato = msg.split(" ", 2)[-1]
                if candidato not in nomes:
                    nome = candidato
                    nomes.add(nome)
                    clientes[nome] = conn
                    conn.sendall("MSG: <ACK>".encode())
                else:
                    conn.sendall("MSG: <NACK>".encode())

            elif msg.startswith("MSG: <ALL>"):
                conteudo = msg.split(">", 1)[-1].strip()
                resposta = f"MSG: {conteudo}"
                for outro_nome, outro_conn in clientes.items():
                    if outro_nome != nome:
                        outro_conn.sendall(resposta.encode())
                conn.sendall(resposta.encode())  # eco para quem enviou

            elif msg.startswith("MSG: <SAIR>"):
                conn.sendall("MSG: <SAIR>".encode())
                break

    except Exception as e:
        print(f"[ERRO] {e}")

    finally:
        if nome:
            nomes.discard(nome)
            clientes.pop(nome, None)
        conn.close()
        print(f"[DESCONECTADO] {addr} saiu.")

# Inicialização do servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[SERVIDOR] Escutando em {HOST}:{PORT}...")

    while True:
        conn, addr = servidor.accept()
        print(f"[NOVA CONEXÃO] {addr} conectado.")
        threading.Thread(target=tratar_cliente, args=(conn, addr)).start()
