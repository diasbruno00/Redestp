import socket
import threading
import json

HOST = '192.168.1.102'
PORT = 5000

# Criando o socket  IPV4, TCP/IP 
usuarioConectado = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def conectandoAoServidor(HOST, PORT):
    try:
        # Conectando ao servidor
        usuarioConectado.connect((HOST, PORT))
        print('Conectado ao servidor')
    except ConnectionRefusedError as e:
        print(f'Servidor indisponível: {e}')
        exit()



def receberListaDeUsuariosConectados(usuario):
   lista = usuario.recv(1024).decode('utf-8')
   print(lista)



def receberMensagem(usuario):
    while True:
        try:
            mensagem = usuario.recv(1024).decode('utf-8')
            print(mensagem)
            if mensagem == 'exit':
                break
            if mensagem == 'atualizarLista':
                receberListaDeUsuariosConectados(usuario)
                soliciarApelidoDoUsuario()

        except ConnectionResetError:
            print('Conexão encerrada')
            usuario.close()
            break

def enviarMensagem(usuario):
    while True:
        try:
            print("\n Aguardando mensagem ... \n")
            mensagem = input()
            usuario.send(mensagem.encode('utf-8'))
            if mensagem == 'exit':
                break
        except Exception as e:
            print(f'Erro ao enviar mensagem: {e}')
            break


def soliciarApelidoDoUsuario():
    apelidoDoUsuarioQueDesejaConectar = input('Digite o apelido do usuário que deseja se conectar: ')
    usuarioConectado.send(apelidoDoUsuarioQueDesejaConectar.encode('utf-8'))


def enviarDadosInicias() :

    # Enviando a mensagem inicial
    apelido = input('Digite seu apelido: ')
    usuarioConectado.send(apelido.encode('utf-8'))

    # Recebendo a lista de usuarios conectados
    print("------------------ Lista de usuarios disponiveis para conexao ----------------")
    receberListaDeUsuariosConectados(usuarioConectado)

    # Enviando o apelido do usuario que deseja se conectar
    soliciarApelidoDoUsuario()
    


# Iniciando a conexão com o servidor
conectandoAoServidor(HOST, PORT)

# Enviando os dados iniciais
enviarDadosInicias()


threading1 = threading.Thread(target=receberMensagem, args=(usuarioConectado,))
threading2 = threading.Thread(target=enviarMensagem, args=(usuarioConectado,))

threading1.start()
threading2.start()

