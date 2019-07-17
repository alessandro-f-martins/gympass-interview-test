# coding: utf-8
""" Módulo testa_corrida_gympass:

Módulo executável de testes para corrida_gympass para o teste prático do
processo seletivo para a posição de Tech Lead Engineer na Gympass.

"""

from corrida_gympass import AvaliaCorrida
from pprint import pprint

# Para fins de testes, os pilotos foram colocados em um dicionário em
# separado, pois os nomes constantes na massa de testes fornecida estão
# inconsistentes, em especial "F.MASSA" e "F.MASS" (Vide referência nos
# comentários do módulo `corrida_gympass`.
pilotos_para_teste = {
    '002': 'Kimi Raikkonen',
    '011': 'Sebastian Vettel',
    '015': 'Fernando Alonso',
    '023': 'Mark Webber',
    '033': 'Rubens Barrichello',
    '038': 'Felipe Massa'
}

if __name__ == "__main__":

    avalia_corrida = AvaliaCorrida('./corredores.data')

    print('\nTestando o módulo de avaliação de corridas para a Gympass: \n')
    print('Serão usados os seguintes códigos para os pilotos:\n')
    for piloto in pilotos_para_teste:
        print('%s: %s' % (pilotos_para_teste[piloto], piloto))

    resultado_prova = avalia_corrida.resultado_corrida()
    # Inserindo uma coluna com os nomes dos pilotos para exibição
    resultado_prova.insert(1, 'Nome Piloto', resultado_prova['Codigo Piloto'].
                           apply(lambda x: pilotos_para_teste[x]))

    melhor_volta_pilotos = {pilotos_para_teste[no_piloto]:
                            avalia_corrida.melhor_volta(no_piloto)
                            for no_piloto in pilotos_para_teste}

    melhor_volta_corrida = avalia_corrida.melhor_volta()
    vel_medias = avalia_corrida.velocidade_media()
    dif_pilotos = avalia_corrida.diferencas_pilotos()

    print("\nResultado da prova:\n")
    pprint(resultado_prova)
    print('\n ==========================\n')

    print("Melhor volta de cada piloto:\n")
    for piloto in melhor_volta_pilotos:
        print("%s: %sª volta (Tempo: %s)" % (piloto,
                                             melhor_volta_pilotos[piloto][2],
                                             melhor_volta_pilotos[piloto][3]))
    print('\n ==========================\n')

    print("Melhor volta da prova:\n")
    print("%s: %sª volta (Tempo: %s)" %
          (pilotos_para_teste[melhor_volta_corrida[0]],
           melhor_volta_corrida[2], melhor_volta_corrida[3]))
    print('\n ==========================\n')

    print("Velocidades médias:\n")
    for piloto in vel_medias:
        print("%s: %.2f km/h" % (pilotos_para_teste[piloto],
                                 vel_medias[piloto]))
    print('\n ==========================\n')

    vencedor = next(iter(dif_pilotos))
    dif_pilotos.pop(vencedor)
    print("Diferenças de tempo para o 1º colocado (%s):\n" %
          pilotos_para_teste[vencedor])
    for piloto in dif_pilotos:
        print("%s: %s" % (pilotos_para_teste[piloto], dif_pilotos[piloto]))
    print('\n ==========================\n')
