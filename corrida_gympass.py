# coding: utf-8
""" Módulo corrida_gympass:

Este módulo implementa um avaliador simples de resultados para corridas de
Kart, de acordo com o solicitado para o teste prático do processo seletivo
para a posição de Tech Lead Engineer na Gympass.

"""

from collections import OrderedDict
import re
import pandas as pd


class AvaliaCorrida:
    """Avalia o resultado de provas de Kart.

    AvaliaCorrida(nome_arq)

    Args:
        nome_arq (str): inicia o avaliador de corridas com os dados do
        arquivo `nome_arq`. Este arquivo deve ser um TSV (tab-separated values)
        no seguinte formato:

        Linhas de cabeçalho:
            - Hora: momento da tomada de volta, no formato HH:MM:SS.mmmm
            - Piloto: referência ao piloto, no formato
                `<cod_piloto> – <nome_piloto>`
                NOTA: o caracter `–` é um EN-dash; não confundir com um hífen
                comum (`-`)
            - Nº Volta: número da volta
            - Tempo Volta: tomada de tempo da volta, no formato MM:SS.mmmm
            - Velocidade média da volta: no formato dd.dddd ou dd,dddd

        O avaliador aceita arquivos com separadores de campos alternando entre
        tabs e espaços (para as linhas de dados) e tabs _ou_ um ou mais espaços
        (para o cabeçalho).

        Exemplo:

        Hora   Piloto  Nº Volta  Tempo Volta  Velocidade média da volta
        23:49:08.277 038 – F.MASSA 1  1:02.852  44,275

    """

    def __init__(self, nome_arq):
        """Vide descrição da classe."""
        self.df_corrida = None
        self.carrega_dados(nome_arq)

    def _tempo_em_milis(self, tempo):
        """Método privado. Converte tempo no formato MM:SS.mmm para
            milissegundos."""
        tempo_lista = re.split(':|\.', tempo)
        return int(tempo_lista[0])*60000 + int(tempo_lista[1])*1000 + \
            int(tempo_lista[2])

    def _milis_em_tempo_str(self, tempo_milis):
        """Método privado. Converte tempo em milissegundos em uma string com
        o formato 'MM:SS.mmm'."""
        mins = str(tempo_milis // 60000)
        segs = (tempo_milis % 60000) // 1000
        segs = '0' + str(segs) if segs < 10 else str(segs)
        milis = tempo_milis % 1000
        if milis < 10:
            milis = '00' + str(milis)
        elif milis >= 10 and milis < 100:
            milis = '0' + str(milis)
        else:
            milis = str(milis)

        return mins + ':' + segs + '.' + milis

    def _calcula_colocacao(self):
        """Método privado. Calcula a ordem de chegada e o total de tempo de
           prova em milissegundos."""
        return self.df_corrida.groupby('Codigo Piloto').sum().\
            sort_values('Tempo Volta em milis', ascending=True).\
            filter(items=['Codigo Piloto', 'Tempo Volta em milis'])

    def carrega_dados(self, nome_arq):
        """Carrega o avaliador com um novo arquivo de dados.

        Args:
            nome_arq (str): Nome do arquivo de dados

        """

        primeira_linha = None
        dados_lista = []
        # O arquivo dado como exemplo possui muitas irregularidades na
        # separação dos campos. Para respeitar a proposta do teste, assume-se
        # que o programa deva ser capaz de tratar tais pontos, e toda limpeza
        # de dados é realizada pelo código, sem preparação ou preparação
        # externa.
        with open(nome_arq, 'r') as arq:
            for linha in arq:
                if not primeira_linha:
                    # Continuando com a premissa de não-interferência externa
                    # no arquivo de dados fornecido, percebeu-se também
                    # inconsistências nos nomes dos pilotos (Ex.: "F.MASSA" e
                    # "F.MASS"). Desta forma, optou-se por fazer a referência
                    # aos pilotos por seu código. Para isso, o parsing do
                    # arquivo separa o código do nome e o coloca em um campo
                    # interno em separado.
                    primeira_linha = re.split('  +|\t+', linha.rstrip())
                    primeira_linha.insert(1, 'Codigo Piloto')
                    # Inserção de um novo campo com o tempo de volta em
                    # milissegundos para cálculos.
                    primeira_linha.append('Tempo Volta em milis')
                else:
                    nova_linha = re.split('  +| *\t+ *| – ', linha.rstrip())
                    nova_linha[-1] = float(nova_linha[-1].replace(',', '.'))
                    # Inserção de um novo campo com o tempo de volta em
                    # milissegundos para cálculos.
                    nova_linha.append(self._tempo_em_milis(
                        nova_linha[primeira_linha.index('Tempo Volta')]))
                    dados_lista.append(nova_linha)

        # Cria o DataFrame principal da classe e converte Nº de Volta para
        # inteiro
        self.df_corrida = pd.DataFrame(columns=primeira_linha,
                                       data=dados_lista)
        self.df_corrida['Nº Volta'] = self.df_corrida['Nº Volta'].astype(int)

    def resultado_corrida(self):
        """Retorna o resultado da corrida (prova) como um DataFrame pandas.

        Returns:
            Resultado da prova como um DataFrame pandas, com os seguintes
            dados:
                - Posição Chegada
                - Codigo Piloto
                - Nome Piloto
                - Tempo Total de Prova
                - Qtde Voltas Completadas

        """

        # Obtendo do DataFrame com os tempos de prova totais em milissegundos
        # na ordem de término de prova (vide método _calcula_colocacao()).
        colocacao = self._calcula_colocacao()
        # Formatando o tempo de prova para exibição e renomeando o nome da
        # coluna de acordo com os requerimentos
        colocacao['Tempo Total de Prova'] = colocacao['Tempo Volta em milis'].\
            apply(self._milis_em_tempo_str)
        # Retirando a coluna 'Tempo Total de Prova em milis' para retorno e
        # exibição.
        colocacao.drop(columns=['Tempo Volta em milis'], inplace=True)
        # Obtendo do DataFrame com a última volta completa de cada piloto
        volta_completa = self.df_corrida.groupby('Codigo Piloto').max().\
            sort_values('Nº Volta').filter(items=['Codigo Piloto', 'Nº Volta'])
        # Renomeando a coluna de acordo com os requerimentos
        volta_completa.rename(
            columns={'Nº Volta': 'Qtde Voltas Completadas'}, inplace=True)
        # Realizando o join dos resultados
        res_corrida = colocacao.join(volta_completa,
                                     on='Codigo Piloto').reset_index()
        # Renumerando o índice para refletir a posição de chegada e nomeando-o
        # de acordo com os requerimentos
        res_corrida.index += 1
        res_corrida.index.name = 'Posição Chegada'
        return res_corrida

    def melhor_volta(self, no_piloto=None):
        """Retorna a volta mais rápida da prova ou a melhor volta de um piloto.

        Args:
            no_piloto: código do piloto, ou None para a melhor volta da prova
            (default: None).

        Returns:
            Tupla com os seguintes dados:
            (<cod_piloto>, <nome_piloto>, <numero_volta>, <tempo_volta>)

        Raises:
            KeyError: se o piloto de código 'no_piloto' não for encontrado

        """

        if no_piloto:
            # Subconjunto do DataFrame relativo ao piloto.
            if no_piloto not in list(self.df_corrida['Codigo Piloto']):
                raise KeyError('Código de piloto não encontrado.')
            temp_df = self.df_corrida[self.df_corrida['Codigo Piloto']
                                      == no_piloto]
        else:
            temp_df = self.df_corrida

        # Encontrando o registro com o menor valor para o tempo de volta
        _melhor_volta = temp_df[temp_df['Nº Volta'] == temp_df.loc[temp_df[
            'Tempo Volta em milis'].idxmin()]['Nº Volta']].reset_index()

        return (_melhor_volta.loc[0, 'Codigo Piloto'],
                _melhor_volta.loc[0, 'Piloto'],
                _melhor_volta.loc[0, 'Nº Volta'],
                _melhor_volta.loc[0, 'Tempo Volta'])

    def velocidade_media(self):
        """Retorna a velocidade média de cada piloto.

        Returns:
            OrderedDict com os seguintes dados:
            {<cod_piloto_1>: <velocidade_piloto_1>,...
             <cod_piloto_n>: <velocidade_piloto_n>}

        """

        # Agrupando os registros por piloto, calculando a média das
        # velocidades, ordenando por esta média, transformando em array Numpy
        # e retornando por código do piloto como dicionário
        medias_vel = self.df_corrida.groupby('Codigo Piloto').mean().\
            sort_values('Velocidade média da volta', ascending=False).\
            filter(items=['Codigo Piloto', 'Velocidade média da volta']).\
            reset_index().values
        # Usando OrderedDict para garantir a ordem por velocidades médias
        # em Python versão < 3.7
        return OrderedDict((a[0], a[1]) for a in medias_vel)

    def diferencas_pilotos(self):
        """Retorna as diferenças de tempo de chegada entre o vencedor e os
        demais pilotos. Os tempos são dados como strings no formato
        "MMminSSsddd".

        Obs.: o vencedor é retornado na primeira posição da lista com valor 0
        (`0min0s0`).

        Returns:
            OrderedDict com os seguintes dados:
            {<cod_piloto_vencedor>: <tempo_piloto_vencedor>,
             <cod_piloto_2>: <velocidade_piloto_2>,...
             <cod_piloto_n>: <velocidade_piloto_n>}

        """

        # Obtendo a colocação dos pilotos em ordem com seus tempos totais de
        # prova em milissegundos e transformando em array Numpy (vide método
        # _calcula_colocacao()
        resultado_corrida_voltas = self._calcula_colocacao().\
            reset_index().values
        # Extraindo o tempo do vencedor
        tempo_ganhador = resultado_corrida_voltas[0][1]
        # Retornando as diferenças. Usando OrderedDict para garantir a ordem
        # por diferença de tempo em Python versão < 3.7
        return OrderedDict((a[0],
                            self._milis_em_tempo_str(a[1] - tempo_ganhador))
                           for a in resultado_corrida_voltas)
