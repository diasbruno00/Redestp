import socket
import threading
import json


HOST = '0.0.0.0' # Endereço IP do servidor
PORT = 5000

# Cria um socket TCP/IP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket a um endereço e porta
server.bind((HOST, PORT))

# Aguarda conexão de um cliente, não a limites de conexões pendentes via parametro
server.listen()

print('Aguardando conexão de um cliente')

# Aceita a conexão
listaDeApelidos  = []

listaDeClientesConectados = {}


def menuDeClienteConectados(listaDeApelidos, cliente):

    if len(listaDeApelidos) == 0:
        cliente.send("Não há clientes conectados".encode('utf-8'))
        return
    
    else:
        listaDeApelidos = str(listaDeApelidos)
        print(listaDeApelidos)
        cliente.send(listaDeApelidos.encode('utf-8'))


def retornaCliente(apelido):
    try:
        return listaDeClientesConectados.get(apelido, None)
    except Exception as e:
        print(f"Erro ao retornar cliente: {e}")
        return None


def retornaApelido(cliente):
    try:
        for apelido, clienteConectado in listaDeClientesConectados.items():
            if clienteConectado == cliente:
                return apelido
    except Exception as e:
        print(f"Erro ao retornar apelido: {e}")
        return None
    


def conectar_clientes(cliente1, cliente2):
    try:
        # Envia uma mensagem para o cliente1 informando que ele está conectado ao cliente2
        mensagem_para_cliente1 = json.dumps({'mensagem': f'Você está conectado ao cliente: {retornaApelido(cliente2)} \n'})
        cliente1.send(mensagem_para_cliente1.encode('utf-8'))

        # Envia uma mensagem para o cliente2 informando que ele está conectado ao cliente1
        mensagem_para_cliente2 = json.dumps({'mensagem': f'Você está conectado ao cliente: {retornaApelido(cliente1)} \n'})
        cliente2.send(mensagem_para_cliente2.encode('utf-8'))


    except Exception as e:
        print(f"Erro ao conectar clientes: {e}")



def excluirCliente(cliente):
    try:
        apelido = retornaApelido(cliente)
        # Remove o cliente da lista de clientes conectados
        listaDeClientesConectados.pop(apelido)
        # Remove o apelido da lista de apelidos
        listaDeApelidos.remove(apelido)
        # Fecha a conexão com o cliente
        cliente.close()
    except Exception as e:
        print(f"Erro ao excluir cliente: {e}")

def receberMensagem(cliente):
    while True:
        try:
            # Recebe a mensagem do cliente em formato json
            apelido = cliente.recv(1024).decode('utf-8')

            listaDeApelidos.append(apelido)

            listaDeClientesConectados[apelido] = cliente
           
            # Adiciona o apelido do cliente na lista de apelidos
            
            apelidoUsuarioConexao = cliente.recv(1024).decode('utf-8')
            # busca o cliente pelo ip
            clienteEncontradoNaBaseDeDados = retornaCliente(apelidoUsuarioConexao)

            if clienteEncontradoNaBaseDeDados is None:
                cliente.send("cliente nao encontrado".encode('utf-8'))
                break
            else:

                while True:
                    
                    mensagem = cliente.recv(1024).decode('utf-8')

                    if mensagem == 'status':
                        menuDeClienteConectados(listaDeApelidos, cliente)
                        continue
                        
                    apelidoCliente = retornaApelido(cliente)
                    mensagem = f"{apelidoCliente}: {mensagem}"
                    print(mensagem)
                    enviarMensagem(mensagem, clienteEncontradoNaBaseDeDados)
     
        except ConnectionResetError:

            print("Conexão encerrada pelo cliente")
            excluirCliente(cliente)
            break

        except json.JSONDecodeError:
            print("Erro ao decodificar a mensagem JSON")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            excluirCliente(cliente)
            break

def enviarMensagem(mensagem, cliente):
    try:
        cliente.send(mensagem.encode('utf-8'))
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        excluirCliente(cliente)


while True:
    try:
        # Aceita a conexão
        cliente, addr = server.accept()
        menuDeClienteConectados(listaDeApelidos, cliente)

        # Recupera o IP e Porta do cliente
        ip_cliente, porta_cliente = addr

        print(f'Conectado com o cliente de IP: {ip_cliente} e Porta: {porta_cliente}')
    
        
        # Recebe dados do cliente em pedaços de 1024 bytes
        thread = threading.Thread(target=receberMensagem, args=(cliente,))
        thread.start()

    except ConnectionError as e:
        print(f"Erro ao conectar com o cliente: {e}")
    
   

