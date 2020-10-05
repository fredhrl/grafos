    # Implementação de uma classe para grafos
# Alunos:
#   Frederico Henrique do Rosario Lopes - 201606840082
#   Hudson Alves Aguiar - 201606840017

from collections import defaultdict 
from collections import deque
import itertools
import math
import matplotlib.pyplot as plt


class Grafo(): 
    # construtor da classe
    def __init__(self,vertices,eh_digraf): 
        self.grafo = defaultdict(list) 
        self.V = vertices
        self.IN = [0] * vertices
        self.pesos = {}
        self.eh_digraf = eh_digraf
    # adição de arestas
    def adiciona_aresta(self,u,v,peso):
        #digrafo significa direcional
        if(not self.eh_digraf):
            if(u == v):
                self.grafo[u].append(v)
                self.IN[v] += 1
                self.pesos[(u, v)] = peso
            else:
                self.grafo[u].append(v)
                self.grafo[v].append(u)
                self.IN[u] += 1
                self.IN[v] += 1
                self.pesos[(u, v)] = peso
                self.pesos[(v, u)] = peso
        else:
            self.grafo[u].append(v)
            self.IN[v] += 1
            self.pesos[(u, v)] = peso
    # a) função para verificar a existencia de uma dada aresta
    def tem_aresta(self,orig,dest):
            #itera sobre cada aresta de um vertice
        for aresta in self.grafo[orig]:
            if(aresta == dest):
                print("Sucesso de busca pela aresta\n {}->{}\n".format(orig,dest))
                return True
        print("falha na busca pela aresta\n {}->{}\n".format(orig,dest))
        return False
    # remoção de aresta
    def remove_aresta(self,orig,dest):
        if(self.tem_aresta(orig,dest)):
            if(self.eh_digraf):
                if(orig == dest):
                    self.grafo[orig].pop(dest)
                    self.IN[orig] -= 1
                    self.pesos[orig].pop(dest)
                else:
                    self.grafo[orig].pop(dest)
                    self.grafo[dest].pop(orig)
                    self.IN[orig] -= 1
                    self.IN[dest] -= 1
                    self.pesos[orig].pop(dest)
                    self.pesos[dest].pop(orig)
            else:
                self.grafo[orig].pop(dest)
                self.IN[dest] -= 1
                self.pesos[orig].pop(dest)
        else:
            print("aresta inexistente")        
    # b) função para Informar o grau de um dado vértice
    def grau(self,u):
        # verifica o numero de arestas de um vertice
        print("grau do vertice {} é {}".format(u,len(self.grafo[u])))
    # c) função para printar a lista de adjacencia do grafo
    def lista_adj(self):
        #itera sobre cada vertice do grafo
        for vertice in self.grafo:
            print("lista de adjacencia do vertice {}\n{}:".format(vertice,vertice), end="")
            #itera sobre cada aresta de um vertice
            for aresta in self.grafo[vertice]:
                print("{},".format(aresta), end="")
            print("\n")
    # d) verificar se o grafo é ciclico
    # função auxiliar
    def ciclico_util(self, v, visitado, recStack): 
        # Utilizando o algoritmo depth first search
        # Marca o vertice atual como visitado e o adiciona para o stack de recursão
        visitado[v] = True
        recStack[v] = True
        #recursão aplicada para todos os vizinhos
        # se algum vizinho foi visitado e está no stack de recursão 
        # o grafo é ciclico
        for vizinho in self.grafo[v]: 
            if visitado[vizinho] == False: 
                if self.ciclico_util(vizinho, visitado, recStack) == True: 
                    return True
            elif recStack[vizinho] == True: 
                return True
  
        # o vertice é removido do stack antes de terminar a função  
        # recursion stack before function ends 
        recStack[v] = False
        return False
    # Retorna verdadeiro se for ciclico e falso se nao
    def eh_ciclico(self): 
        visitado = [False] * self.V 
        recStack = [False] * self.V 
        for node in range(self.V): 
            if visitado[node] == False: 
                if self.ciclico_util(node,visitado,recStack) == True: 
                    return print("O grafo é ciclico")
        return print("O grafo nao é ciclico")
    # E) Verificar se o grafo é conexo
    def tem_caminho_util(self, orig,dest, visitado, recStack): 
        # Utilizando o algoritmo depth first search
        # Marca o vertice atual como visitado e o adiciona para o stack de recursão
        visitado[orig] = True
        recStack[orig] = True
        #recursão aplicada para todos os vizinhos
        # se algum vizinho foi visitado e está no stack de recursão 
        # o grafo é ciclico
        if(orig == dest):
            return True
        for vizinho in self.grafo[orig]: 
            if visitado[vizinho] == False: 
                if self.tem_caminho_util(vizinho,dest,visitado,recStack) == True: 
                    return True
            elif recStack[vizinho] == True: 
                return True
        recStack[orig] = False
        return False   
    def eh_conexo(self):
        result = []
        visitado = [False] * self.V 
        recStack = [False] * self.V
        combs = list(itertools.product(range(self.V),repeat = 2))
        for par in combs:
            result.append(g.tem_caminho_util(par[0],par[1],visitado,recStack))
        if(all(result)):
            print("o grafo é conexo")
        else:
            print("o grafo não é conexo")
    # F) função para determinar os elementos fortemente conexos do grafo
    # seguindo o algoritmo de kosaraju:
    # cria uma pilha L
    # faz busca em profundidade em cada vertice do grafo g
    # se o vertice atual já foi visitadado ele é adicionado a pilha L
    # garante que na pilha o proximo grupo fortemente conexo termina de ser 
    # visitado antes de algum vertice do componente anterior
    # faz-se isso até encher a pilha
    # traspõe-se o grafo
    # garantir que na ordem da pilha ele explore
    # para garantir que na volta somente os membros de um mesmo
    # grupo
    # enquanto tiver vertices na pilha:
    #   remove-se vertices v da pilha
    #   aplica busca em profundidade no vertice v do grafo transposto
    #   para printar os componentes fortemente conexos de v
    #   se a busca em profundidade tiver passado por um vertice que nao foi visitado
    #   marca o fim de um componente fortemente conexo

    # função auxiliar para busca em profundidade
    def busca_profund_util(self,v,visitado): 
        # marca o vertice atual como visitado
        visitado[v]= True
        print ("{},".format(v),end="")
        # aplica recursão para os vizinhos
        for i in self.grafo[v]: 
            if visitado[i]==False: 
                self.busca_profund_util(i,visitado)     
    # função auxiliar para busca em profundidade que adiciona os vertices em uma pilha para
    # obter a ordem dos componentes
    def ordena_comp(self,v,visitado, pilha): 
        # marca o vertice atual como visitado  
        visitado[v]= True
        # aplica recursão nos vizinhos
        for i in self.grafo[v]: 
            if visitado[i]==False: 
                self.ordena_comp(i, visitado, pilha)
        # adiciona o vertice para a pilha se já o tiver visitado    
        pilha = pilha.append(v)
    # função para obter a transposta do grafo 
    def transposta(self): 
        g = Grafo(self.V,self.eh_digraf)
        for i in self.grafo: 
            for j in self.grafo[i]: 
                g.adiciona_aresta(j,i,1) 
        return g
    # define os elementos fortemente conexos
    def fortemente_conexos(self,euler):
        # inicializa a pilha
        pilha = []
        # inicializa todos os vertices com nao visitado
        visitado =[False]*(self.V) 
        # 
        for i in range(self.V): 
            if visitado[i]==False: 
                self.ordena_comp(i, visitado, pilha)
  
        # cria a trasposta do grafo 
        gr = self.transposta()
        # reinicializa todos os vertices com nao visitado) 
        visitado =[False]*(self.V)
        # processa todos os vertices na ordem da pilha
        elementos = 0

        if(not euler):
            while pilha:
                i = pilha.pop()
                if visitado[i]==False:
                    gr.busca_profund_util(i, visitado)
                    elementos += 1
                    print("") 
            print("quantidade de elementos fortemente conexos: {}".format(elementos))
        return elementos
    # G)Verificar se o grafo é Euleriano.
    def eh_euleriano(self):
        # verifica se todos os vertices fazem parte do mesmo
        #componente fortemente conexo
        if(self.fortemente_conexos(1) != 1):
            print("O grafo não é euleriano")
            return False

        if(not self.eh_digraf):
        # verifica se o grau de entrada é o mesmo do grau de saida para cada vertice
            impar = 0
            for i in range(self.V): 
                    if len(self.grafo[i]) % 2 !=0:
                        impar +=1
    
            if impar == 0:
                return print("O grafo  é euleriano")
            elif impar == 2:
                return print("O grafo tem um caminho euleriano(semi-euleriano)")
            elif impar > 2: 
                return print("O grafo não é euleriano")
        else:
            for v in range(self.V): 
                if len(self.grafo[v]) != self.IN[v]:
                    return print("O grafo não é euleriano")
                
        return print("O grafo é euleriano")
    # H) função para achar o caminho mais curto
    def BFS_SP(self, orig, dest): 

        visitado = [] 
        
        #fila do bfs
        fila = [[orig]] 
        #se chegar no vertic de destino
        if orig == dest: 
            print("Same Node") 
            return
        
        # repete pela fila
        while fila: 
            # O caminho recebe o primeiro da fila
            caminho = fila.pop(0)
            # inicializa o vertice atual como o ultimo do caminho
            vertice = caminho[-1] 
            
            # Verifica se o vertice foi visitado
            if vertice not in visitado: 
                vizinhos = self.grafo[vertice]

                
                # Itera sobre os vizinhos do vertice atual
                for vizinho in vizinhos:
                    # cria o caminho
                    novo_caminho = list(caminho) 
                    # adiciona o vizinho para o novo caminho 
                    novo_caminho.append(vizinho) 
                    # adiciona o novo caminho para fila
                    fila.append(novo_caminho) 
                    
                    # Verifica o vizinho do vertice é o destino
                    if vizinho == dest: 
                        print("caminho mais curto  = {}".format(novo_caminho)) 
                        return
                visitado.append(vertice) 
    
        # Condição quando os vertices não estão conectados
        print("Desculpe, mas não existe um caminho que ligue{} a {}:".format(orig,dest))
        return
    # I) Plotar o grafo
    # tentou- n deu a melhor solução- mas que deu, deu
    def plot(self):
        r = 2
        x = []
        y = []

        for t in range(self.V):
            x.append(5+r*math.sin((t*2*math.pi)/self.V))
            y.append(5+r*math.cos((t*2*math.pi)/self.V))
        plt.plot(x,y,marker = 'o',markersize=16,linewidth = 0)
        for vertice in self.grafo:
            plt.annotate("{}".format(vertice), 
                 (x[vertice], y[vertice]), 
                 textcoords="offset points", 
                 size = 22,
                 xytext=(5,10),
                 ha='center')
            for aresta in self.grafo[vertice]:
                plt.arrow(x[vertice], y[vertice],0.96*(x[aresta]-x[vertice]), 0.96*(y[aresta]-y[vertice]), head_width=0.075, head_length=0.1,width = 0.02, fc='k', ec='k')
        return plt.show()
if __name__ == "__main__": 
    # menu
    flag = True
    while(flag):
        print("Menu de operações\n")
        print(" A) Verificar a existencia de uma aresta.")
        print(" B) Informar o grau de um dado vértice.")
        print(" C) Printar a lista de adjacencia do grafo.")
        print(" D) Verificar se o grafo é ciclico.")
        print(" E) Verificar se um grafo é conexo.")
        print(" F) Listar os elementos fortemente conexos de um grafo.")
        print(" G) Verificar se o grafo é euleriano.")
        print(" H) Caminho mais curto entre dois vertices.")
        print(" I) Plotar o grafo.")
        print(" J) Criar o grafo.")
        print(" K) Usar o grafo pre-definido.")
        print(" L) Sair.")
        ans = input("Escolha uma opção:")
        ans = ans.upper()

        if(ans == "A"):
            orig = int(input("insira o valor do vertice de origem desejado:"))
            dest = int(input("insira o valor do vertice  de destino desejado:"))
            g.tem_aresta(orig,dest)
            input("Aperte qualquer tecla para continuar...")
        elif (ans == "B"):
            vertice = int(input("insira o valor do vertice desejado:"))
            g.grau(vertice)
            input("Aperte qualquer tecla para continuar...")
        elif (ans == "C"):
            g.lista_adj()
            input("Aperte qualquer tecla para continuar...")
        elif (ans == "D"):
            g.eh_ciclico()
            input("Aperte qualquer tecla para continuar...")
        elif (ans == "E"):
            g.eh_conexo()
            input("Aperte qualquer tecla para continuar...")
        elif (ans == "F"):
            print("Lista dos elementos fortemente conectados:")
            g.fortemente_conexos(0)
            input("Aperte qualquer tecla para continuar...")
        elif (ans == "G"):
            g.eh_euleriano()
            input("Aperte qualquer tecla para continuar...")
        elif (ans == "H"):
            a = int(input("Entre com o vertice de origem:\n"))
            b = int(input("Entre com o vertice de destino\n"))
            g.BFS_SP(a,b)
            input("Aperte qualquer tecla para continuar...")
        elif (ans == "I"):
            g.plot()
            input("Aperte qualquer tecla para continuar...")
        elif (ans == "J"):
            flag = "s"
            v = int(input("Entre com o numero de vertices dos grafo:\n"))
            eh_digraf = int(input("informe se o grafo é digrafo:(0 se não/1 se sim)\n"))
            g = Grafo(v,eh_digraf)
            while(flag == "s"):
                print("Criação de grafo:\n 1) Adicionar aresta.\n 2) Remover aresta.\n 3) Sair")
                flag1 =int(input("Escolha uma opção:\n"))
                if(flag1 == 1):
                    orig = int(input("Entre com o vertice de origem:\n"))
                    dest = int(input("Entre com o vertice de destino:\n"))
                    peso = int(input("Entre com o peso da aresta:\n"))
                    g.adiciona_aresta(orig,dest,peso)
                elif(flag1 == 2):
                    orig = int(input("Entre com o vertice de origem:\n"))
                    dest = int(input("Entre com o vertice de destino:\n"))
                    g.remove_aresta(orig,dest)
                else:
                    break
                flag = input("Continuar?(s/n)\n")
        elif (ans == "K"):
            g = Grafo(5,1)
            g.adiciona_aresta(0,1,1)
            g.adiciona_aresta(1,2,1)
            g.adiciona_aresta(1,3,1)
            g.adiciona_aresta(2,0,1)
            g.adiciona_aresta(2,3,1)
            g.adiciona_aresta(3,4,1)
            input("Aperte qualquer tecla para continuar...")
        else:
            flag = False