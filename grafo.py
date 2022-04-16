class Vertice():
    def __init__(self, id):
        self.id = id
        self.conexoes = []
        self.visited = False
        
        # bellmanFord
        self.bf_pai = None
        self.bf_distancia = float('inf')

        # dijkstra
        self.dj_pai = None
        self.dj_distancia = float('inf')

        # prim 
        self.pm_pai = None
        self.pm_distancia = float('inf')

    def __str__(self):
        return f'id: {self.id}'

    def addAresta(self, dst, weight):
        self.conexoes.append(Aresta(dst, weight))

    def getArestaFromVertice(self, dst):
        for aresta in self.conexoes:
            if aresta.dst == dst:
                return aresta
    def getArestaMenorCusto(self):
        menor = self.conexoes[0]
        for aresta in self.conexoes:
            if aresta.weight < menor.weight:
                menor = aresta
        return menor

class Aresta():
    def __init__(self, dst, w):
        self.dst = dst
        self.w = w


def bfs(g, pai):
    print("BFS")
    for v in g:
        v.visited = False

    q = []
    seq = []

    q.append(pai)
    seq.append(pai)

    print(f'Comecou em {pai.id}')

    while q != []:
        pai = q.pop(0)
        pai.visited = True  

        for ar in pai.conexoes:
            if not ar.dst.visited:
                q.append(ar.dst)
                seq.append(ar.dst)
                ar.dst.visited = True
                print(f'-> {ar.dst.id} ', end='')
        if q == []:
            for v in g:
                if v.visited == False:
                    q.append(v)
                    break

    print(f'\nSequencia de visita em lista: ')
    for v in seq:
        print(v.id, end=" ") 
    print('\n')
    return seq

def dfs(g, pai):
    print("DFS")
    for v in g:
        v.visited = False
    
    q = []
    seq = []

    q.append(pai)
    seq.append(pai)

    print(f'Comecou em {pai.id}')

    while q != []:
        pai = q.pop(0)
        pai.visited = True  

        for ar in pai.conexoes:
            if not ar.dst.visited:
                q = [ar.dst] + q
                seq.append(ar.dst)
                ar.dst.visited = True
                print(f'-> {ar.dst.id} ', end='')
        if q == []:
            for v in g:
                if v.visited == False:
                    q.append(v)
                    break

    print(f'\nSequencia de visita em lista: ')
    for v in seq:
        print(v.id, end=" ") 
    print('\n')
    return seq

def relax(p, f):
    # print(f'\n relaxando {p.id} -> {f.id}')
    if p.bf_distancia + p.getArestaFromVertice(f).w < f.bf_distancia:
        f.bf_distancia = p.bf_distancia + p.getArestaFromVertice(f).w
        # nao eh usado no algoritmo mas pode se usado para retorna do 
        # node atual até o pai pelo melhor caminho (menor custo)
        f.bf_pai = p
def bellman_ford(vertices, pai):
    print("Bellman-Ford")
    # reset node configs
    for v in vertices:
        v.bf_distancia = float('inf')
        v.bf_pai = None

    pai.bf_distancia = 0
    for v in vertices[:-1]:
        for ar in v.conexoes:
            relax(v, ar.dst)
    for v in vertices:
        print(f'{v.id} -> {v.bf_distancia if v.bf_distancia != float("inf") else f"SEM CAMINHO PARTINDO DE {pai.id}"}')
    print('\n')
def dijkstra(vertices, pai):
    print("Dijkstra")
    # reset node configs

    for v in vertices:
        v.dj_distancia = float('inf')
        v.dj_pai = None
        v.visited = False

    print(f'Comecou em {pai.id}')
    pai.dj_distancia = 0
    q = []
    q.append(pai)
    while q != []:
        p = q.pop(0)
        p.visited = True
        for ar in p.conexoes:
            if ar.dst.visited == False:
                q.append(ar.dst)
                ar.dst.visited = True
            if p.dj_distancia + ar.w < ar.dst.dj_distancia:
                ar.dst.dj_distancia = p.dj_distancia + ar.w
                ar.dst.dj_pai = p
    
    for v in vertices:
        print(f'{v.id} -> {v.dj_distancia if v.dj_distancia != float("inf") else f"SEM CAMINHO PARTINDO DE {pai.id}"}')
    print()
# nao funciona com grafo nao orientado com valores negativos
# mas funciona com grafo orientado com valores negativos
def floyd_warshall(vertices):
    print("Floyd-Warshall")
    d = [[float('inf') for i in range(len(vertices))] for j in range(len(vertices))]
    pred = [[float('inf') for i in range(len(vertices))] for j in range(len(vertices))]
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            if i == j:
                d[i][j] = 0
            elif vertices[i].getArestaFromVertice(vertices[j]):
                d[i][j] = vertices[i].getArestaFromVertice(vertices[j]).w
            pred[i][j] = i

    # for i in range(len(vertices)):
    #     for j in range(len(vertices)):
    #         print(f'{d[i][j]}\t', end='')
    #     print()

    for i in range(len(vertices)):
        for j in range(len(vertices)):
            for k in range(len(vertices)):
                if d[i][j] > d[i][k] + d[k][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    pred[i][j] = pred[k][j]

    for i in range(len(vertices)):
        for j in range(len(vertices)):
            print(f'{d[i][j]}\t', end='')
        print()

    print()
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            print(f'{pred[i][j]}\t', end='')
        print()
    print()
    # pred funciona assim:
    # caso vc queria saber o caminho de menor distancia do vertice 0 ao 6
    # vc olha pred[0][6] e ve que o valor eh 2,
    # entao vc olha o menor caminho de 0 a 2, ou seja, pred[0][2] e ve que o valor eh 1,
    # entao vc olha pred[0][1] e ve que o valor eh 0, que eh o vertice que queremos comecar
    # logo temos o menor caminho de 0 ate 6, 0->1->2->6
    # neste caso, menor caminho == menor custo

    return d, pred


def prim(vertices, pai):
    print("Prim")
    for v in vertices:
        v.pm_distancia = float('inf')
        v.pm_pai = None
        v.visited = False

    v = len(vertices)
    noEdge = 0
    selected = [0]*v
    selected[0] = True
    
    l = []

    while noEdge < v-1:
        minimum = float('inf')
        x, y = 0, 0
        for i in range(v):
            if selected[i] == True:
                for j in range(v):
                    if not selected[j] and vertices[i].getArestaFromVertice(vertices[j]):
                        if vertices[i].getArestaFromVertice(vertices[j]).w < minimum:
                            minimum = vertices[i].getArestaFromVertice(vertices[j]).w
                            x = i
                            y = j


        print(f'{vertices[x].id} -> {vertices[y].id}')
        selected[y] = True
        if vertices[x] not in l:
            l.append(vertices[x])
        if vertices[y] not in l:
            l.append(vertices[y])
        noEdge+=1
    for i in range(len(l)):
        print(f'{l[i].id} ', end='')
    print()
    return l


def main():
    # vertices ficao guardados como ponteiros dentro de 'vertices'
    vertices = []
    lenv = 8
    # arestas determina quais conexoes entre os nos sao feitas
    arestas = [(1,2, 2), (1,4, 2), 
               (2,3, -3), (2,4, -1), 
               (3,7, -2), 
               (4,8, 2), (4,1, -1),
               (5,7, 1), (5,6, 2),
               (6,5, 2), 
               (8,7, 4)]
    # arestas = [(1,2, 1), (1,5, 1), (2,3, 2), (2,4, 2), (2,5, 2), (3,5, 3), (4,6, 4), (5,6, 3)]

    for i in range(lenv):
        v = Vertice(i+1)
        vertices.append(v)
   
    # trata de fazer as arestas entre os vertices, arestas orientadas
    # for i in range(len(arestas)):
    #     ipv, iuv = arestas[i]
    #     pv, uv = vertices[ipv-1], vertices[iuv-1]
    #     pv.conexoes.append(uv)
    #     uv.conexoes.append(pv)

    # orientado
    for src, dst, w in arestas:
        vertices[src-1].addAresta(vertices[dst-1], w)

    # nao orientado
    # for src, dst, w, in arestas:
    #     vertices[src-1].addAresta(vertices[dst-1], w)
    #     vertices[dst-1].addAresta(vertices[src-1], w)

    print(vertices[0].id)
    bfs(vertices, vertices[0])
    dfs(vertices, vertices[0])
    bellman_ford(vertices, vertices[0])
    dijkstra(vertices, vertices[0])
    floyd_warshall(vertices)
    prim(vertices, vertices[0])

if __name__ == "__main__":
    main()