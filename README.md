Avaliador de Corridas 
=====================
*Um teste de desenvolvimento para o processo seletivo de Tech Lead Engineer para a Gympass*

***Autor:*** Alessandro Martins  
***Data***: 17/07/2019

Introdução
----------

A presente aplicação foi desenvolvida por Alessandro Martins em 17 de julho de 2019 de acordo com as especificações encontradas no site https://github.com/Gympass/interview-test.

A aplicação baseia-se no módulo `AvaliaCorrida`, que é inicializado com um arquivo de dados sobre uma prova de Kart e realiza as seguintes análises:

  - Tabela com o resultado final da prova, contendo, por piloto:
    - Posição de chegada
    - Código do piloto
    - Nome do piloto
    - Número de voltas completadas
    - Tempo total de prova
  - Volta mais rápida da prova
  - Volta mais rápida por piloto
  - Velocidade média por piloto
  - Diferença de tempo entre cada piloto e o vencedor


Utilização
----------

### Pré-requisitos

A aplicação utiliza a biblioteca *Pandas* para manipulação de dados tabulares. Para instalá-la, execute na linha de commandos:

```shell
$ pip install -U pandas
```

### Execução

A aplicação conta com o módulo `corrida_gympass`, que provê a classe `AvaliaCorrida`. Esta classe possui os seguintes métodos:

  - `AvaliaCorrida(nome_arq)`: inicia o avaliador de corridas com os dados do arquivo `nome_arq`. 
  - `carrega_dados(nome_arq)`: carrega o avaliador com um novo arquivo de dados.
  - `resultado_corrida()`: retorna o resultado da corrida (prova) como um DataFrame pandas.
  - `melhor_volta(no_piloto)`: retorna a volta mais rápida da prova (se chamado sem argumentos) ou a melhor volta do piloto de código `no_piloto`.
  - `velocidade_media()`: retorna a velocidade média de cada piloto.
  - `diferencas_pilotos()`: retorna as diferenças de tempo de chegada entre o vencedor e os demais pilotos. Os tempos são dados como strings no formato “MMminSSsddd”. *Obs.*: o vencedor é retornado na primeira posição da lista com valor 0 (`0min0s0`).

Para exemplos de utilização, consulte código do módulo de teste `testa_corrida_gympass.py`.


Detalhes da implementação
-------------------------

### Arquivos para a aplicação:

  - `corrida_gympass.py`: principal módulo, contém a classe `AvaliaCorrida`
    – `__init__.py`: arquivo vazio, complementar ao módulo `corrida_gympass`
  - `testa_corrida_gympass.py`: código para testes e demonstração de uso da aplicação
  - `corredores.data`: arquivo gerado pela cópia e colagem dos dados do site de especificações do teste
  - `corrida_gympass.hlp`: arquivo de ajuda para o módulo `corrida_gympass`, gerado por PyDoc a partir dos docstrings do módulo.
  - `README.md`: este documento
  - `SUAS-INSTRUÇÕES.txt`: este documento em formato texto simples, de acordo com os requerimentos

### Sobre a obtenção e tratamento do arquivo de dados

Os dados foram obtidos pela cópia e colagem do painel de texto fornecido na página do teste. 

O arquivo dado como exemplo possui muitas irregularidades na separação dos campos. Para respeitar a proposta do teste, assume-se que o *programa deva ser capaz de tratar tais pontos*, e toda limpeza de dados é realizada pelo código, sem modificação ou preparação externa.

Continuando com a premissa de não-interferência externa no arquivo de dados fornecido, percebeu-se também inconsistências nos nomes dos pilotos (Ex.: "F.MASSA" e "F.MASS"). Desta forma, optou-se por fazer a referência aos pilotos por seu código. Para isso, o *parsing* do arquivo separa o código do nome e o coloca em um campo interno em separado.

Desta forma, ao serem realizados os testes, os nomes dos pilotos foram colocados em uma estrutura de dados separada do módulo principal, no programa de testes, e toda manipulação de dados foi feita utilizando-se o código do piloto.

### Utilização de Pandas

Para a manipulação de dados em forma tabular, optou-se pela utilização da biblioteca Python *Pandas*, que permite uma abordagem simplificada para as operações necessárias aos requerimentos, como:

  - Tratamento e preparação de dados
  - Agrupamento de registros
  - Cálculo de função agregadas, como soma e média de colunas
  - Consulta de valores máximos e mínimos
  - Inserção, remoção e realocação de colunas
  - Aplicação de funções de transformação a todo o conjunto de dados (*DataFrame*) ou a colunas específicas

Outra motivação para a escolha do Pandas como biblioteca central da aplicação é sua eficiência. Por ser baseada em no pacote *Numpy*, suas operações internas são escritas em C, permitindo uma velocidade de execução muito maior do que se fossem realizadas em Python padrão.

Para mais detalhes, visite https://pandas.pydata.org/.


Testes
------

A tela de resultados abaixo é resultado da execução do script `testa_corrida_gympass.py`:

```shell 
$ python testa_corrida_gympass.py

Testando o módulo de avaliação de corridas para a Gympass: 

Serão usados os seguintes códigos para os pilotos:

Kimi Raikkonen: 002
Sebastian Vettel: 011
Fernando Alonso: 015
Mark Webber: 023
Rubens Barrichello: 033
Felipe Massa: 038

Resultado da prova:

                Codigo Piloto         Nome Piloto Tempo Total de Prova Qtde Voltas Completadas
Posição Chegada                                                                               
1                         038        Felipe Massa           4min11s578                       4
2                         002      Kimi Raikkonen           4min15s153                       4
3                         033  Rubens Barrichello            4min16s80                       4
4                         023         Mark Webber           4min17s722                       4
5                         015     Fernando Alonso           4min54s221                       4
6                         011    Sebastian Vettel           6min27s276                       3

 ==========================

Melhor volta de cada piloto:

Kimi Raikkonen: 4ª volta (Tempo: 1:03.076)
Sebastian Vettel: 3ª volta (Tempo: 1:18.097)
Fernando Alonso: 2ª volta (Tempo: 1:07.011)
Mark Webber: 4ª volta (Tempo: 1:04.216)
Rubens Barrichello: 3ª volta (Tempo: 1:03.716)
Felipe Massa: 3ª volta (Tempo: 1:02.769)

 ==========================

Melhor volta da prova:

Felipe Massa: 3ª volta (Tempo: 1:02.769)

 ==========================

Velocidades médias:

Felipe Massa: 44.25 km/h
Kimi Raikkonen: 43.63 km/h
Rubens Barrichello: 43.47 km/h
Mark Webber: 43.19 km/h
Fernando Alonso: 38.07 km/h
Sebastian Vettel: 25.75 km/h

 ==========================

Diferenças de tempo para o 1º colocado (Felipe Massa):

Kimi Raikkonen: 0min3s575
Rubens Barrichello: 0min4s502
Mark Webber: 0min6s144
Fernando Alonso: 0min42s643
Sebastian Vettel: 2min15s698

 ==========================
```
Apêndice
--------

### Arquivo de ajuda para o módulo `corrida_gympass` (corrida_gympass.hlp):

```python
Help on module corrida_gympass:

NAME
    corrida_gympass - Módulo corrida_gympass:

DESCRIPTION
    Este módulo implementa um avaliador simples de resultados para corridas de
    Kart, de acordo com o solicitado para o teste prático do processo seletivo
    para a posição de Tech Lead Engineer na Gympass.

CLASSES
    builtins.object
        AvaliaCorrida

    class AvaliaCorrida(builtins.object)
     |  AvaliaCorrida(nome_arq)
     |
     |  Avalia o resultado de provas de Kart.
     |
     |  AvaliaCorrida(nome_arq)
     |
     |  Args:
     |      nome_arq (str): inicia o avaliador de corridas com os dados do
     |      arquivo `nome_arq`. Este arquivo deve ser um TSV (tab-separated values)
     |      no seguinte formato:
     |
     |      Linhas de cabeçalho:
     |          - Hora: momento da tomada de volta, no formato HH:MM:SS.mmmm
     |          - Piloto: referência ao piloto, no formato
     |              `<cod_piloto> – <nome_piloto>`
     |              NOTA: o caracter `–` é um EN-dash; não confundir com um hífen
     |              comum (`-`)
     |          - Nº Volta: número da volta
     |          - Tempo Volta: tomada de tempo da volta, no formato MM:SS.mmmm
     |          - Velocidade média da volta: no formato dd.dddd ou dd,dddd
     |
     |      O avaliador aceita arquivos com separadores de campos alternando entre
     |      tabs e espaços (para as linhas de dados) e tabs _ou_ um ou mais espaços
     |      (para o cabeçalho).
     |
     |      Exemplo:
     |
     |      Hora   Piloto  Nº Volta  Tempo Volta  Velocidade média da volta
     |      23:49:08.277 038 – F.MASSA 1  1:02.852  44,275
     |
     |  Methods defined here:
     |
     |  __init__(self, nome_arq)
     |      Vide descrição da classe.
     |
     |  carrega_dados(self, nome_arq)
     |      Carrega o avaliador com um novo arquivo de dados.
     |
     |      Args:
     |          nome_arq (str): Nome do arquivo de dados
     |
     |  diferencas_pilotos(self)
     |      Retorna as diferenças de tempo de chegada entre o vencedor e os
     |      demais pilotos. Os tempos são dados como strings no formato
     |      "MMminSSsddd".
     |
     |      Obs.: o vencedor é retornado na primeira posição da lista com valor 0
     |      (`0min0s0`).
     |
     |      Returns:
     |          Dicionário com os seguintes dados:
     |          {<cod_piloto_vencedor>: <tempo_piloto_vencedor>,...
     |           <cod_piloto_2>: <velocidade_piloto_2>}
     |           <cod_piloto_n>: <velocidade_piloto_n>}
     |
     |  melhor_volta(self, no_piloto=None)
     |      Retorna a volta mais rápida da prova ou a melhor volta de um piloto.
     |
     |      Args:
     |          no_piloto: código do piloto, ou None para a melhor volta da prova
     |          (default: None).
     |
     |      Returns:
     |          Tupla com os seguintes dados:
     |          (<cod_piloto>, <nome_piloto>, <numero_volta>, <tempo_volta>)
     |
     |  resultado_corrida(self)
     |      Retorna o resultado da corrida (prova) como um DataFrame pandas.
     |
     |      Returns:
     |          Resultado da prova como um DataFrame pandas, com os seguintes
     |          dados:
     |              - Posição Chegada
     |              - Codigo Piloto
     |              - Nome Piloto
     |              - Tempo Total de Prova
     |              - Qtde Voltas Completadas
     |
     |  velocidade_media(self)
     |      Retorna a velocidade média de cada piloto.
     |
     |      Returns:
     |          Dicionário com os seguintes dados:
     |          {<cod_piloto_1>: <velocidade_piloto_1>,...
     |           <cod_piloto_n>: <velocidade_piloto_n>}
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

FILE
    ./corrida_gympass.py

```
