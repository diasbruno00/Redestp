import socket
import threading
import json

HOST = 'localhost'
PORT = 5000

# Criando o socket  IPV4, TCP/IP 
UsarioConectado = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conectandoAoServidor(HOST, PORT):
    try:
        # Conectando ao servidor
        UsarioConectado.connect((HOST, PORT))
        print('Conectado ao servidor')
    except ConnectionRefusedError as e:
        print(f'Servidor indisponível: {e}')
        exit()

def receberMensagem(usuario):
    while True:
        try:
            mensagem = usuario.recv(1024).decode('utf-8')
            print(f'Mensagem recebida: {mensagem}')
            if mensagem == 'exit':
                break;
        except ConnectionResetError:
            print('Conexão encerrada')
            usuario.close()
            break
def enviarMensagem(usuario):
    while True:
        try:
            print("Digite a mensagem: ")
            mensagem = input()
            usuario.send(mensagem.encode('utf-8'))
            if mensagem == 'exit':
                break
        except Exception as e:
            print(f'Erro ao enviar mensagem: {e}')
            break

conectandoAoServidor(HOST, PORT)
apelido = input('Digite seu apelido: ')
enderecoIPdoUsuarioQueDesejaConectar = input('Digite o IP do usuário que deseja se conectar: ')

mensagem_inicial = {
    'apelido': apelido,
     'ip': enderecoIPdoUsuarioQueDesejaConectar
}

            # Enviando a mensagem inicial
UsarioConectado.send(json.dumps(mensagem_inicial).encode('utf-8'))

threading1 = threading.Thread(target=receberMensagem, args=(UsarioConectado,))
threading2 = threading.Thread(target=enviarMensagem, args=(UsarioConectado,))

threading1.start()
threading2.start()