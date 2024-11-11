from bibgrafo.grafo_exceptions import VerticeInvalidoException
from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from bibgrafo.grafo_errors import *


class MeuGrafo(GrafoListaAdjacencia):

    def vertices_nao_adjacentes(self):
        """
        Provê um conjunto de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um objeto do tipo set que contém os pares de vértices não adjacentes
        """
        VnAdJ = set()  # Inicializa um conjunto vazio para armazenar os pares de vértices não adjacentes

        tam = len(self.vertices)  # Obtém o tamanho do número de vértices no grafo
        for i in range(tam):  # Loop para percorrer cada vértice
            for j in range(i + 1, tam):  # Loop para comparar o vértice atual com todos os próximos
                u, v = self.vertices[i], self.vertices[j]  # Obtém os dois vértices a serem comparados
                for a in self.arestas:  # Loop para percorrer todas as arestas do grafo
                    # Verifica se existe uma aresta entre u e v (sem considerar a direção)
                    if (self.arestas[a].v1 == v and self.arestas[a].v2 == u) or (
                            self.arestas[a].v2 == v and self.arestas[a].v1 == u):
                        break  # Se houver uma aresta, interrompe o loop
                else:  # Se o loop não foi interrompido, significa que não há aresta entre u e v
                    VnAdJ.add(f'{u}-{v}')  # Adiciona o par de vértices ao conjunto

        return VnAdJ  # Retorna o conjunto com os pares de vértices não adjacentes

    def ha_laco(self):
        """
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        """
        # Itera sobre todas as arestas do grafo
        for a in self.arestas:
            # Verifica se a aresta conecta um vértice a ele mesmo (laço)
            if self.arestas[a].v1 == self.arestas[a].v2:
                return True  # Retorna True se encontrar um laço

        # Se o loop terminar e não encontrar nenhum laço, retorna False
        return False  # Nenhum laço encontrado, retorna False

    def grau(self, V=''):
        """
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        """
        # Inicializa o grau como 0
        GRAU = 0

        # Verifica se o vértice fornecido existe no grafo
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError  # Se o vértice não existir, lança um erro

        # Itera sobre todas as arestas do grafo
        for a in self.arestas:
            # Se a aresta é conectada ao vértice V (considerando tanto a origem quanto o destino da aresta)
            if self.arestas[a].v1.rotulo == V:
                GRAU += 1  # Incrementa o grau para cada aresta conectando ao vértice
            if self.arestas[a].v2.rotulo == V:
                GRAU += 1  # Incrementa o grau para cada aresta conectando ao vértice

        # Retorna o grau final do vértice
        return GRAU

    def ha_paralelas(self): #ja foi
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        # Dicionário para armazenar pares de vértices que já possuem uma aresta entre eles
        pares_arestas = {}

        for a in self.arestas:
            v1 = self.arestas[a].v1.rotulo
            v2 = self.arestas[a].v2.rotulo
            par = tuple(sorted([v1, v2]))  # Usamos o par ordenado para evitar duplicidade

            if par in pares_arestas:
                # Se o par já existe no dicionário, significa que há uma aresta paralela
                return True
            else:
                # Caso contrário, adicionamos o par ao dicionário
                pares_arestas[par] = True

        return False  # Se nenhum par repetido for encontrado, não há arestas paralelas

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: Um string com o rótulo do vértice a ser analisado
        :return: Um conjunto (set) com os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        '''

        # Verificar se o vértice existe no grafo
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError  # Lança exceção se o vértice não existir no grafo

        arestas_incidentes = set()  # Usar um set para garantir que os rótulos sejam únicos

        # Percorrer todas as arestas do grafo
        for a in self.arestas:
            aresta = self.arestas[a]
            if aresta.v1.rotulo == V or aresta.v2.rotulo == V:  # Verifica se o vértice está na aresta
                arestas_incidentes.add(a)  # Adiciona o rótulo da aresta ao set

        return arestas_incidentes  # Retorna o set com os rótulos das arestas incidentes sobre o vértice

    def eh_completo(self):
        """
        Verifica se o grafo é completo utilizando a função 'existe_aresta'.
        :return: Um valor booleano que indica se o grafo é completo
        """
        # Cria uma lista com todos os vértices do grafo
        vertices = list(self.vertices)  # Converte o conjunto de vértices para uma lista para iterar com índice

        # Percorre todos os pares de vértices únicos no grafo
        for i in range(len(vertices)):  # O primeiro vértice do par
            for j in range(i + 1, len(vertices)):  # O segundo vértice do par, evitando repetições
                u, v = vertices[i], vertices[j]  # O par de vértices u e v

                # Verifica se há uma aresta entre u e v usando a função 'existe_aresta'
                if not self.existe_aresta(u, v):  # Se não houver aresta entre u e v
                    return False  # O grafo não é completo, pois falta a aresta entre u e v

        # Se o loop terminar sem encontrar pares de vértices sem aresta, o grafo é completo
        return True  # Todos os pares de vértices possuem uma aresta, então é um grafo completo

    def existe_aresta(self, v1, v2):
        """
        Verifica se existe uma aresta entre os vértices v1 e v2.
        :param v1: O primeiro vértice
        :param v2: O segundo vértice
        :return: True se existe aresta entre v1 e v2, False caso contrário
        """
        # Verifica se v1 está no grafo e tem arestas
        if v1 in self.vertices:
            for aresta in self.arestas:
                if (self.arestas[aresta].v1 == v1 and self.arestas[aresta].v2 == v2) or (self.arestas[aresta].v1 == v2 and self.arestas[aresta].v2 == v1):
                    return True
        return False