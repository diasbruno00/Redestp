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
ListaDeIP = []
listaDeClientes = []

clienteEnontradoPadrao = None

listaDeClientesConectados = {}

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
        if cliente in listaDeClientes:
            listaDeClientes.remove(cliente)
            cliente.close()
    except Exception as e:
        print(f"Erro ao excluir cliente: {e}")

def receberMensagem(cliente):
    while True:
        try:
            # Recebe a mensagem do cliente em formato json
            mensagem = cliente.recv(1024).decode('utf-8')

            # Decodifica a mensagem json
            dados = json.loads(mensagem)
            
            # Adiciona o apelido do cliente na lista de apelidos
            listaDeApelidos.append(dados.get('apelido', ''))
            print(listaDeApelidos)

            
            listaDeClientesConectados[dados.get('apelido')] = cliente

            # busca o cliente pelo ip
            clienteEncontradoNaBaseDeDados = buscarClientePorIp(dados.get('ip'))

            if clienteEncontradoNaBaseDeDados is None:
                cliente.send("cliente nao encontrado").encode('utf-8')
                break
            else:
                # Se o cliente não foi encontrado, envia uma mensagem de erro
                conectar_clientes(cliente, clienteEncontradoNaBaseDeDados)

                while True:
                    mensagem = cliente.recv(1024).decode('utf-8')
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


def buscarClientePorIp(ip):
    for cliente in listaDeClientes:
        if cliente.getpeername()[0] == ip:
            return cliente

    return None

67
while True:
    try:
        # Aceita a conexão
        cliente, addr = server.accept()

        # Recupera o IP e Porta do cliente
        ip_cliente, porta_cliente = addr
        listaDeClientes.append(cliente)

        print(cliente)

        print(f'Conectado com o cliente de IP: {ip_cliente} e Porta: {porta_cliente}')
        ListaDeIP.append(ip_cliente)

        print(ListaDeIP)
        
        # Recebe dados do cliente em pedaços de 1024 bytes
        thread = threading.Thread(target=receberMensagem, args=(cliente,))
        thread.start()
    except ConnectionError as e:
        print(f"Erro ao conectar com o cliente: {e}")
    
   

