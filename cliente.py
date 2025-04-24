import socket

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    print("Conectado ao servidor.")

    # Envio e validação do nome
    while True:
        nome = input("Digite o nome de usuário: ")
        msg = f"MSG: <NOME> {nome}"
        cliente.sendall(msg.encode())

        resposta = cliente.recv(1024).decode().strip()
        print(f"Servidor respondeu: {resposta}")

        if resposta == "MSG: <ACK>":
            print("Nome aceito. Conexão concluída.")
            break
        elif resposta == "MSG: <NACK>":
            print("Nome já em uso. Tente outro.")

    # Loop de comunicação
    while True:
        print("\nComandos disponíveis:")
        print("- MSG: <ALL> sua mensagem → Envia uma mensagem geral")
        print("- MSG: <SAIR> → Encerra a conexão")
        entrada = input("\nDigite o comando: ")

        cliente.sendall(entrada.encode())

        if entrada.startswith("MSG: <SAIR>"):
            print("Saindo...")
            break

        resposta = cliente.recv(1024).decode().strip()
        print(f"Servidor respondeu: {resposta}")
