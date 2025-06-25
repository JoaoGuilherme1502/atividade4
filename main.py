import requests # Possibilita usar a localização do usuario
import os # Possibilita limpar o terminal

def limpar_terminal(): # Para limpar o terminal
    os.system('cls' if os.name == 'nt' else 'clear')

# variaveis pedidas
def info_inicio():
    
    while True:
        limpar_terminal()
        print('Coletando algumas informações...')
        print('=' * 60)
        dados = {}
        dados['nome'] = input('Olá, qual seu nome? ').strip()
        dados['idade'] = input('Sua idade: ').strip()
        dados['city'] = input('Qual sua cidade? ').strip() # Será que consigo ver a localização e indicar livrarias?
        dados['estado'] = input('Seu estado: ').strip()
        dados['livros_digitais'] = int(input('Quantos livros digitais lidos por você no último ano? '))
        dados['livros_fisicos'] = int(input('E quantos livros físicos lidos nesse último ano? '))
        print('Qual sua preferência de leitura:\n1. DIGITAL, como Kindle\n2. LIVRO FÍSICO')
        dados['pref_de_leitura'] = input('Escolha uma opção válida: ').strip()
        dados['hora_estudo'] = int(input('Quantas horas você dedica aos livros por ESTUDO por semana? '))
        dados['hora_entretenimento'] = int(input('Quantas horas você dedica aos livros por ENTRETENIMENTO por semana? '))
        print('Deseja mudar alguma informação?\n1. Sim, desejo mudar\n2. Não, desejo continuar')
        editar_info_inicio = input('Digite: ').strip()
        
        if editar_info_inicio == '1':
            continue
        elif editar_info_inicio == '2':
            return dados
        else:
            print('Dado inválido, digite 1 ou 2.')

# Agora que entra a busca de bibliotecas usando a localização

def busca(city, estado, limite=10):
    url = "https://nominatim.openstreetmap.org/search" # API do OpenStreetMap
    busca = f'library in {city}, {estado}, Brazil' # Faz uma pesquisa

    params = {
        'q' : busca,
        'format' : 'json',
        'limit' : limite
    }

    headers = {
        'User-Agent': 'meu-app-biblioteca/1.0 (jgsa1502@gmail.com)' # Para acessar
    }

    resposta = requests.get(url, params=params, headers=headers)

    if resposta.status_code == 200:
        resultados = resposta.json()
        nomes = [lugar.get('display_name') for lugar in resultados]
        return nomes
    else:
        return[]
    

def estatisticas(dados):
    limpar_terminal()
    print('=' * 60)
    print(f'Olá, {dados['nome']}, seja muito bem-vindo(a) ao BookStatistics!')
    print('=' * 60)

    total_ano = dados['livros_digitais'] + dados['livros_fisicos']
    total_5_anos = total_ano * 5

    if total_ano <= 3:
        print(f'Você leu apenas {total_ano} livros no ano. Que tal aumentar? Em 5 anos terá lido {total_5_anos}.')
    elif total_ano <= 5:
        print(f'Você leu {total_ano} livros no ano, boa média! Em 5 anos terá lido {total_5_anos}.')
    else:
        print(f'Você leu {total_ano} livros no ano! Excelente! Em 5 anos, {total_5_anos} livros.')

    print('=' * 60)
    print(f'{dados['nome']}, você estuda {dados['hora_estudo']}h por semana, somando {dados['hora_estudo'] * 52}h ao ano.')
    print(f'E lê por entretenimento {dados['hora_entretenimento']}h por semana, totalizando {dados['hora_entretenimento'] * 52}h ao ano.')
    print('=' * 60)
    
    # Outra estimativa, agora sobre a preferencia de leitura
    print('Comparando seu tipo de leitura...')
    # Em busca da preferencia real
    if dados['livros_digitais'] > dados['livros_fisicos']: 
        tipo_real = 'Digital'

    elif dados['livros_digitais'] < dados['livros_fisicos']:
        tipo_real = 'Físico'
    
    else:
        tipo_real = 'Empate'
    # Em busca da preferencia com base na Pergunta sobre a preferencia
    if dados['pref_de_leitura'] == '1':
        tipo_pref = 'Digital'
    elif dados['pref_de_leitura'] == '2':
        tipo_pref = 'Físico'

    print(f'Sua preferência declarada é: {tipo_pref}\nVocê leu mais: {tipo_real}')

    # Comparando 
    if tipo_real == tipo_pref:
        if tipo_real == 'Empate':
            print('Você está bem equilibrado entre digital e físico!')
        else:
            print('Legal! Seu hábito de leitura bate com sua preferência. ')
    else:
        if tipo_real == 'Empate':
            print('Você tem uma preferência, mas sua leitura está equilibrada em dois tipos.')
        else:
            print('Curioso! Sua prática não bate com sua preferência. Esta em busca de novas formas de ler?')
        print('=' * 60)

    while True:
        print('\nDeseja ver bibliotecas na sua região?\n1. Sim\n2. Não')
        opcao = input('Digite: ').strip()

        if opcao == '1':
            bibliotecas = busca(dados['city'], dados['estado'])
            print(f'\nBibliotecas encontradas em {dados['city']}, {dados['estado']}:\n')
            if bibliotecas:
                for i, b in enumerate(bibliotecas, 1):
                    partes = b.split(',')
                    nome_bib = partes[0].strip()
                    local = ', '.join(partes[1:4]).strip()
                    print(f'{i}. {nome_bib}\n{local}\n')
            else:
                print('Nenhuma biblioteca encontrada.')
        elif opcao == '2':
            print('\nObrigado por usar o BookStatistics! Até a próxima.')
            break
        else:
            print('Opção inválida. Digite 1 ou 2.')

def main():
    dados = info_inicio()
    estatisticas(dados)

if __name__ == "__main__":
    main()
    