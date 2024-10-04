# projeto_transacoes_bancarias -- DS-PY-17 - logica de programacao II
# readme link here: 
# https://github.com/allansuzuki/ADA_classes/blob/main/DS-PY-Data-Science/DS-PY-017%20L%C3%93GICA%20DE%20PROGRAMA%C3%87%C3%83O%20II%20(PY)/Material%20do%20Aluno/projeto_README.md
# 
# Esse programa é um sistema de gestao de transacoes de uma conta bancária pessoal
# no qual os dados são de transações e possuem seu valor, a categoria do gasto e seu ID.
# 
# Teu objetivo é completar esse sistema CRUD (Create-Read-Update-Delete) simples 
# para ver dados de transacao da tua conta pessoal, criar, editar e excluir transações.
# Também deve fazer com que o programa NUNCA pare, ou seja,
# caso ocorra um possível erro, deve validar as entradas, detectar erros e avisar o usuário
# mas o programa não deve parar.
#
#
# Notas importantes: 
# 1. As funções que geram os dados e criam a interface do sistema já estão prontas. 
# por favor não as altere.
#
# 2. Depois das funções do sistema estão as funções do programa
# No qual podem alterar à vontade, exceto o nome das funções
# Ou seja, podem criar funções, adicionar ou remover parâmetros, 
# mas não alterar o nome das funções existentes.
#
# 3. Coloque opções de navegabilidade em cada janela que o usuário estiver.
# Por exemplo, se ele escolher a opcao "alterar transacao" sem querer, tem que ter a opcao de voltar para a tela anterior ou inicial.
#
# 4. Caso por qualquer motivo queira os dados originais novamente,
# apage o json `transactions` na pasta `data` e inicie o programa novamente para gerar os dados.
# Os valores serão os mesmos, porém os UUID NÃO serão os mesmos!!
#
# Critérios (pontos):
#   tarefas validacoes  total
# C     10      15       25
# R     25      25       50
# U     10      10       20
# D     2.5     2.5      5
#
#
# Boa sorte e divirtam-se :)
# ------------------------------------------------------------------------------
# -----------------------
# depencies
# -----------------------
import json
import os
import uuid
import random
import sys

# -----------------------
# load settings
# -----------------------
sys.path.append('./data/')
from data import settings

# -----------------------
# SYSTEM functions 
# -----------------------
# não alterar nada das funções de system
def criar_transacoes(num_transacoes, proporcao_categorias, seed=settings.seed):
    assert sum([proporcao_categorias[k] for k in proporcao_categorias])==1, '`proporcao_categorias` não soma 100%! Favor rever.'

    # garantir reprodutibilidade dos valores
    random.seed(seed)

    # Calcula o número de transações por categoria com base na proporção
    numero_transacoes_por_categoria = {categoria: int(num_transacoes * proporcao) for categoria, proporcao in proporcao_categorias.items()}
    
    transacoes = []
    
    # Gera as transações
    for categoria, quantidade in numero_transacoes_por_categoria.items():
        for _ in range(quantidade):
            transacao = {
                "UUID": str(uuid.uuid4()),
                "valor": round(random.uniform(1.0, 1000.0), 2),  # Preço aleatório entre 1 e 1000
                "categoria": categoria
            }
            transacoes.append(transacao)
    
    return transacoes

def salvar_json(transacoes, path2save, filename):
    # create path if not exist
    if not os.path.exists(path2save):
        os.makedirs(path2save)
    with open(os.path.join(path2save,filename), "w") as file:
        json.dump(transacoes, file, indent=4)
    print(f"Arquivo salvo em: {os.path.abspath(os.path.curdir)+'/'+path2save+'/'+filename}")

def criar_bd(num_transacoes:int = 10000, proporcao_categorias:list = settings.categorias_proporcao, path2save="./data", filename='transactions.json'):
    salvar_json(criar_transacoes(num_transacoes,  proporcao_categorias),
                path2save, filename
    )

def load_bd(filepath='./data/transactions.json'):
    with open(filepath, "r") as file:
        bd = json.load(file)
    return bd

def tela_inicial():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Bem-vindo <teu nome inteiro aqui>!")
    print('conta: 0000001-0')
    print("\nEste programa permite gerenciar transações de sua conta pessoal.")
    print("\nEscolha uma das opções abaixo:")
    print("1. Visualizar relatórios")
    print("2. Cadastrar transações")
    print("3. Editar transações")
    print("4. Excluir transações")
    print("-" * 10)
    print("0. Sair")
    print('\n')

# -----------------------
# PROGRAM functions 
# -----------------------
# pode editar como quiser as funções abaixo! Somente não altere os nomes das funções.
# para alterar as funções abaixo, basta apagar o `pass` e preencher com as instruções.

def run():
    """
    Esta é a função principal que vai rodar o programa
    """  
    input_usuario = None
    
    while input_usuario != '0':
        # exibe a tela inicial
        tela_inicial()
        input_usuario = input("Digite uma opcao: ").strip()
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            match input_usuario:
                case '0':
                    print('Saindo ...')
                case '1':
                    escolher_relatorio()
                case '2':
                    cadastrar_transacao()
                case '3':
                    editar_transacao_por_ID()
                case '4':
                    excluir_transacao()
                case _:
                    print("Opção inválida. Tente novamente.")
        except Exception:
            print(f"Erro inesperado\nPor favor, tente novamente.")
                
def escolher_relatorio():
    """
    Escolher o relatório a ser visualizado.
    """
    input_usuario = None
    
    while input_usuario != '0':
        # exibe a tela inicial
        visualizar_relatorios()
        input_usuario = input("Digite uma opcao: ").strip()
        os.system('cls' if os.name == 'nt' else 'clear')
        try:
            match input_usuario:
                case '0':
                    print('Retornando ao menu principal ...')
                case '1':
                    total_transacoes = str(calcular_total_transacoes()).replace('.',',')
                    print(f"Total de transações realizadas: R$ {total_transacoes}")
                    if deseja_salvar_relatorio():
                        salvar_relatorio("total_transacoes.txt", f"Total de transações realizado: R$ {total_transacoes}")
                case '2':
                    max5_transacoes, max_5_transacoes_categorias = mostrar_m5_transacoes(max=True)
                    print(f'Valor das 5 transações mais caras: {max5_transacoes}')
                    texto_categorias = "5 transações mais caras por categoria:\n"
                    for categoria, transacoes in max_5_transacoes_categorias.items():
                        texto_categorias += f"{categoria}: {transacoes}\n"
                    print(texto_categorias)
                    if deseja_salvar_relatorio():
                        texto = f"5 transações mais caras: {max5_transacoes}\n"
                        texto += texto_categorias
                        salvar_relatorio("max5_transacoes.txt", texto)
                case '3':
                    mean5_transacoes, mean5_transacoes_categorias = mostrar_m5_transacoes(mean=True)
                    print(f'Valor das 5 transações medianas: {mean5_transacoes}')
                    texto_categorias = "5 transações medianas por categoria:\n"
                    for categoria, transacoes in mean5_transacoes_categorias.items():
                        texto_categorias += f"{categoria}: {transacoes}\n"
                    print(texto_categorias)
                    if deseja_salvar_relatorio():
                        texto = f"5 transações medianas: {mean5_transacoes}\n"
                        texto += texto_categorias
                        salvar_relatorio("mean5_transacoes.txt", texto)
                case '4':
                    min5_transacoes, min5_transacoes_categorias = mostrar_m5_transacoes(min=True)
                    print(f'Valor das 5 transações mais baratas: {min5_transacoes}')
                    texto_categorias = "5 transações mais baratas por categoria:\n"
                    for categoria, transacoes in min5_transacoes_categorias.items():
                        texto_categorias += f"{categoria}: {transacoes}\n"
                    print(texto_categorias)
                    if deseja_salvar_relatorio():
                        texto = f"5 transações mais baratas: {min5_transacoes}\n"
                        texto += texto_categorias
                        salvar_relatorio("min5_transacoes.txt", texto)
                case '5':
                    media_geral, media_por_categoria = calcular_media()
                    print(f'Média total: {media_geral}\nMédia por catergoria: {media_por_categoria}')
                    if deseja_salvar_relatorio():
                        # Gera o conteúdo do arquivo.txt
                        texto_media_geral = f"Média total das transações: {media_geral:.2f}\n"
                        texto_media_categoria = "Média das Transações por Categoria:\n"
                        for categoria, media in media_por_categoria.items():
                            texto_media_categoria += f"{categoria}: {media:.2f}\n"
                        # Salvar o relatório em um arquivo
                        salvar_relatorio("media_geral.txt", texto_media_geral)
                        salvar_relatorio("media_por_categoria.txt", texto_media_categoria)
                case '6':
                    try:
                        print(consultar_transacao_por_ID())
                    except Exception as e:
                        print(f"Erro ao consultar transação: {e}")
                case _:
                    print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"Erro inesperado\nPor favor, tente novamente.")

def visualizar_relatorios():
    """
    Mostra um menu de opcoes no qual gera relatórios com base na escolha do usuário.
    """
    print("Escolha um relatório para ser visualizado: \n")
    print("1. Exibir soma total de transações")
    print("2. 5 transações mais caras")
    print("3. 5 transações medianas")
    print("4. 5 transações mais baratas")
    print("5. Exibir média")
    print("6. Consultar transações por ID")
    print("-" * 10)
    print("0. Voltar ao menu principal")
    print('\n')

def salvar_relatorio(nome_arquivo, conteudo): # Victor
    """
    Salvar o relatório gerado em .txt
    \nAplicar esta função em todos os relatórios listados em visualizar_relatorios
    """

    try:
        with open(nome_arquivo, 'w') as arquivo:
                arquivo.write(conteudo)
                print(f"Relatório salvo com sucesso em: {nome_arquivo}")
    except Exception as e:
            print(f"Erro ao salvar o relatório: {e}")


    '''
    Quando for chamar a função salvar relatório, em caso da variável ser um número float, deve
    transformar a variável em uma formatação "bonitinha" em string, para que não haja conflito.

    Além disso, quando for chamar a função, a chamada deve ocorrer antes do ´return´.
    Exemplo:

    media = soma / len(bd)

    media = f"{media:.2f}"

    salvar_relatorio("media.txt", media)

    return media
    '''
    
def deseja_salvar_relatorio(): # Rafael
    '''
    Checa se usuário deseja salvar o relatório.
    '''
    while True:
        input_usuario = input("Deseja salvar relatório? (s/[n]): ").lower().strip()
        match input_usuario:
            case 's':
                print('Salvando ...')
                os.system('cls' if os.name == 'nt' else 'clear')
                return True
            case 'n':
                print('Saindo ...')
                return False
            case _:
                print('Opção inválida. Tente novamente.')
    

def calcular_total_transacoes(): # Rafael
    """
    Calcula o valor total de transações da conta.
    Utilize essa mesma função para o caso `por categoria`
    """
    total_transacoes = sum([transacao['valor'] for transacao in bd])
    total_transacoes_arredondado = round(total_transacoes, 2)
    return total_transacoes_arredondado

def mostrar_m5_transacoes(**m): # Rafael
    """
    Mostra as m5 transações realizadas, sendo m parâmetro que deve ser adicionada à função.
    \nm : 'max','min','median', sendo 
    \n\t'max' mostra os top 5 maior valor,
    \n\t'min' mostra os top 5 menor valor,
    \n\t'mean' mostra os top 5 valores próximos a média
    
    Utilize essa mesma função para o caso `por categoria`
    """
    transacoes_por_categoria = pegar_transacoes_por_categoria()
    if 'max' in m:
        m5_transacoes = sorted(bd, key=lambda x: x['valor'], reverse=True)[:5]
        m5_transacoes_categorias = {categoria: sorted(transacoes_por_categoria[categoria], key=lambda x: x['valor'], reverse=True)[:5] for categoria in transacoes_por_categoria}
    elif 'min' in m:
        m5_transacoes = sorted(bd, key=lambda x: x['valor'])[:5]
        m5_transacoes_categorias = {categoria: sorted(transacoes_por_categoria[categoria], key=lambda x: x['valor'])[:5] for categoria in transacoes_por_categoria}
    elif 'mean' in m:
        media_geral, _ = calcular_media()
        diferencas = [(transacao, abs(transacao["valor"] - media_geral)) for transacao in bd]
        diferencas_ordenadas = sorted(diferencas, key=lambda x: x[1])
        valores_mais_proximos = [transacao[0] for transacao in diferencas_ordenadas[:5]]
        m5_transacoes = sorted(valores_mais_proximos, key=lambda x: x['valor'])
        m5_transacoes_categorias = {}
        for categoria in transacoes_por_categoria:
            diferencas = [(transacao, abs(transacao["valor"] - media_geral)) for transacao in transacoes_por_categoria[categoria]]
            diferencas_ordenadas = sorted(diferencas, key=lambda x: x[1])
            valores_mais_proximos = [transacao[0] for transacao in diferencas_ordenadas[:5]]
            m5_transacoes_categorias[categoria] = sorted(valores_mais_proximos, key=lambda x: x['valor'])
    m5_valores = [transacao['valor'] for transacao in m5_transacoes]
    m5_valores_categorias = {categoria: [transacao['valor'] for transacao in m5_transacoes_categorias[categoria]] for categoria in m5_transacoes_categorias}
    return m5_valores, m5_valores_categorias

def pegar_transacoes_por_categoria(): # Rafael
    """
    Retorna as transações por categoria.
    """
    # Obtém todas as categorias(map), não repetindo a mesma categoria(set)
    categorias = list(map(lambda transacao: transacao['categoria'], bd))
    # Cria uma lista de listas com as transações por categoria
    transacoes_por_categoria = {categoria: [] for categoria in categorias}
    # Adiciona as transacoes de bd na lista de transacoes_por_categoria
    for transacao in bd:
        categoria = transacao['categoria']
        transacoes_por_categoria[categoria].append(transacao)
    return transacoes_por_categoria
    

def calcular_media(): # Victor
    """
    Calcula a média dos valores das transações.
    Utilize essa mesma função para o caso `por categoria`
    """
    # Obtém todas as categorias(map), não repetindo a mesma categoria(set)
    categorias = set(map(lambda transacao: transacao['categoria'], bd))

    # Armazena a soma e a contagem de transações por categoria
    soma_por_categoria = {}
    contagem_por_categoria = {}

    # Calcula a soma e conta por categoria
    for transacao in bd:
        categoria = transacao['categoria']
        valor = transacao['valor']

        if categoria not in soma_por_categoria:
            soma_por_categoria[categoria] = 0
            contagem_por_categoria[categoria] = 0

        soma_por_categoria[categoria] += valor
        #O tamanho da variável
        contagem_por_categoria[categoria] += 1

    # Calcula a média por categoria
    media_por_categoria = {}
    for categoria in categorias:
        if contagem_por_categoria[categoria] > 0:
            media_por_categoria[categoria] = round(soma_por_categoria[categoria] / contagem_por_categoria[categoria], 2)
        else:
            media_por_categoria[categoria] = 0
            
    # Calcula a média geral
    media_geral = round(sum(soma_por_categoria.values()) / len(bd), 2)
    return media_geral, media_por_categoria


def obter_uuid_valido(): # Rogerio
    while True:
        id = input('Digite o UUID da transação: ').strip()

    #Verifica se o ID está no formato de UUID
        if (len(id) == 36 and
            id[8] == '-' and id[13] == '-' and id[18] == '-' and id[23] == '-' and
            all(c in '0123456789abcdefABCDEF-' for c in id)):
            return id
        else:
            print("O UUID digitado não está no formato correto. Por favor, digite novamente.")
            
def consultar_transacao_por_ID(): # Rogerio
    #consulta ID
    id = obter_uuid_valido()
    for transacao in bd:
      if transacao["UUID"] == id:
        return transacao
    raise Exception("Transação com UUID entregue não encontrado")
    

def cadastrar_transacao(): # Pedro
    """
    Cadastra uma nova transação.
    \nObs:Para gerar um novo uuid, veja como é feito na função `criar_transacoes`.
    """
    while True:
        try:
            valor = 0
            categoria = -1
            while valor<=0:
                valor = float(input("Digite o valor da transação: R$ ").strip())
                if valor <= 0 :
                    print("O valor deve ser maior que zero.")

            categorias_disponiveis = list(settings.categorias_proporcao.keys())
            while True:
                print('Escolha uma categoria: ')
                for i in range(len(categorias_disponiveis)):
                    print(f'{i+1} - {categorias_disponiveis[i]}')
                escolha = int(input("> "))
                if 0 < escolha <= len(categorias_disponiveis):
                    categoria = categorias_disponiveis[escolha-1]
                    break
                else:
                    print("Escolha invalida, tente novamente.")

            novo_uuid = str(uuid.uuid4())

            nova_transacao = {
                "UUID": novo_uuid,
                "valor": round(valor, 2),
                "categoria": categoria
            }

            bd.append(nova_transacao)
            salvar_json(bd, './data', 'transactions.json')
            print(f"Transação cadastrada com sucesso! ID: {novo_uuid}")
            opcao = input("Deseja cadastrar outra transação? (s/[n]): ").strip().lower()
            if opcao != 's':
                break

        except Exception as e:
            print(f"Ocorreu um erro inesperado: [{e}].")
            print("Sua transação NÃO FOI registrada, por favor, tente novamente.")

def novo_valor_valido(): # Rogerio
    while True:
        try:
            novo_valor = input('Digite o novo valor para a transação (por exemplo, 560.21): ').strip()
            
            # Tenta converter a entrada para float
            valor = float(novo_valor)
            
            # Verifica se o valor é positivo
            if valor <= 0:
                print('O valor deve ser um número positivo.')
            else:
                return valor
        except ValueError:
            print('Entrada inválida. Por favor, digite um número válido.')
        except:
            print('Erro desconhecido. Por favor, digite um número válido.')

def editar_transacao_por_ID(): # Rogerio
    id = obter_uuid_valido()
    for transacao in bd:
        if transacao['UUID'] == id:
            print(f'O valor da transação {transacao["valor"]}')
            novo_valor = novo_valor_valido()
            transacao['valor'] = novo_valor
            salvar_json(bd, './data', 'transactions.json')
            return f'Transação editada com sucesso. Novo valor: {novo_valor}'

def excluir_transacao(): # Thales
    """
    Exclui uma transação específica pelo UUID.
    """
    try:
        # Carrega o banco de dados
        bd = load_bd()
        
        # Solicita o UUID da transação a ser excluída
        uuid_input = input("Digite o UUID da transação que deseja excluir (ou '0' para voltar): ").strip()
        
        if uuid_input == '0':
            print("Retornando ao menu principal...")
            return
        
        # Verifica se o UUID existe no banco de dados
        transacao_encontrada = None
        for transacao in bd:
            if transacao["UUID"] == uuid_input:
                transacao_encontrada = transacao
                break
        
        if transacao_encontrada:
            # Confirma a exclusão
            confirmacao = input(f"Você tem certeza que deseja excluir a transação de valor {transacao_encontrada['valor']}? (s/[n]): ").lower().strip()
            if confirmacao == 's':
                bd.remove(transacao_encontrada)
                # Salva as mudanças no arquivo
                salvar_json(bd, './data', 'transactions.json')
                print("Transação excluída com sucesso!")
            else:
                print("Exclusão cancelada.")
        else:
            print("UUID não encontrado. Verifique e tente novamente.")
    
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

# -----------------------
# MAIN SCRIPT
# -----------------------
# não alterar nada abaixo
if __name__ == "__main__":
    
    # -----------------------
    # NÃO ALTERAR ESTE BLOCO
    # -----------------------
    # criar o banco de dados caso ele não exista
    print(os.path.abspath('.'))
    if not os.path.exists('./data/transactions.json'):
        criar_bd()
    
    # load bd 
    bd = load_bd()
    # -----------------------

    # -----------------------
    # ABAIXO PODE ALTERAR
    # -----------------------
    #limpar console (opcional)
    os.system('cls' if os.name == 'nt' else 'clear')
    # inicia o programa
    run()