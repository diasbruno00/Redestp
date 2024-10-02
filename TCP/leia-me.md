
**1º Passo – Instalar a Linguagem de Programação Python**

A versão do Python utilizada neste projeto foi a 3.11.3.

Utilize uma versão igual ou superior para evitar problemas de incompatibilidade.

Você pode baixar o Python no seguinte link: [https://www.python.org/downloads/](https://www.python.org/downloads/).

**2º Passo – Como Executar via Terminal**

**Execução do Servidor:**

1. Navegue até a pasta `TCP/Servidor` e abra o terminal.
2. Execute o seguinte comando: python servidor.py
3. Após a execução, digite o endereço IP IPV4 do servidor no input. Para descobrir o endereço IP da sua máquina, abra o CMD e digite `ipconfig`.
4. O servidor estará aguardando a conexão dos clientes.

**Execução do Cliente:**

1. Navegue até a pasta `TCP/Cliente` e abra o terminal.
2. Execute o seguinte comando: python cliente.py
3. Após a execução, insira novamente o endereço IP IPV4 que foi utilizado no servidor.
4. Digite seu apelido, que servirá como uma forma de identificação para cada cliente.
5. Aparecerá uma lista com todos os clientes disponíveis para comunicação. Escolha o apelido de um cliente e digite o nome correspondente para iniciar a comunicação. Se o apelido for inválido, o processo será repetido.
6. Se o apelido for válido, a conexão será estabelecida e o cliente poderá enviar mensagens para o outro cliente.
7. Digite `sair` para encerrar o conexão.