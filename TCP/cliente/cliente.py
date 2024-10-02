import socket
import threading
import json

# Endereço IP e Porta do servidor
HOST = str(input("Digite o endereço IP do servidor: "))
PORT = 2001

# Criando o socket  IPV4, TCP/IP 
usuario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Função para conectar ao servidor
def conectandoAoServidor(HOST, PORT):
    try:
        # Conectando ao servidor
        usuario.connect((HOST, PORT))
        print('Conectado ao servidor')
    except socket.getaddrinfo as e:
        print('Erro ao resolver o endereço IP ou nome do host')
        exit()
    except ConnectionRefusedError as e:
        print(f'Servidor indisponível: {e}')
        exit()


# Função para receber a lista de usuários conectados
def receberListaDeUsuariosConectados(usuario):
   lista = usuario.recv(1024).decode('utf-8')
   print(lista)


# Função para receber mensagens
def receberMensagem(usuario):
    while True:
        try:
            mensagem = usuario.recv(1024).decode('utf-8')
            print(mensagem)
            if mensagem == 'exit':
                break
        except ConnectionResetError:
            print('Conexão encerrada')
            usuario.close()
            break

# Função para enviar mensagens
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

# Função para solicitar o apelido do usuário que deseja se conectar
def soliciarApelidoDoUsuario(usuario):
    apelidoDoUsuarioQueDesejaConectar = input('Digite o apelido do usuário que deseja se conectar: ')
    usuario.send(apelidoDoUsuarioQueDesejaConectar.encode('utf-8'))


# Função para enviar os dados iniciais
def enviarDadosInicias() :

    try:
    # Enviando a mensagem inicial
        apelido = input('Digite seu apelido: ')
        usuario.send(apelido.encode('utf-8'))

        # Recebendo a lista de usuarios conectados
        print("------------------ Lista de usuarios disponiveis para conexao ----------------")
        receberListaDeUsuariosConectados(usuario)

        # Enviando o apelido do usuario que deseja se conectar
        soliciarApelidoDoUsuario(usuario)

        mensagem = usuario.recv(1024).decode('utf-8')

        if mensagem == 'cliente nao encontrado':
            
            while True:
                conectarOutroUsuario(usuario)
                mensagem = usuario.recv(1024).decode('utf-8')
                print(mensagem)
                if mensagem == 'cliente encontrado':
                    break

    except Exception as e:
        print(f'Erro ao enviar dados iniciais: {e}')

# Função para conectar a outro usuario
def conectarOutroUsuario(usuario):

    try:

        # Recebendo a lista de usuarios conectados
        print("------------------ Lista de usuarios disponiveis para conexao ----------------")
        receberListaDeUsuariosConectados(usuario)

        # Enviando o apelido do usuario que deseja se conectar
        soliciarApelidoDoUsuario(usuario)

    except Exception as e:
        print(f'Erro ao conectar outro usuario: {e}')



# Iniciando a conexão com o servidor
conectandoAoServidor(HOST, PORT)

# Enviando os dados iniciais
enviarDadosInicias()

# Iniciando as threads
threading1 = threading.Thread(target=receberMensagem, args=(usuario,))
threading2 = threading.Thread(target=enviarMensagem, args=(usuario,))

# Iniciando as threads
threading1.start()
threading2.start()

