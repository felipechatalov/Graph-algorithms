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

    def __str__(self):
        return f'id: {self.id}'

    def addAresta(self, dst, weight):
        self.conexoes.append(Aresta(dst, weight))

    def getArestaFromVertice(self, dst):
        for aresta in self.conexoes:
            if aresta.dst == dst:
                return aresta


class Aresta():
    def __init__(self, dst, w):
        self.dst = dst
        self.w = w


def resetVisitedNodes(g):
    for v in g:
        v.visited = False




def bfs(g, pai):
    resetVisitedNodes(g)

    q = []
    seq = []

    q.append(pai)
    seq.append(pai)

    print(f'\nComecou em {pai.id}')

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
    print()
    return seq

def dfs(g, pai):
    resetVisitedNodes(g)
    
    q = []
    seq = []

    q.append(pai)
    seq.append(pai)

    print(f'\nComecou em {pai.id}')

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
    print()
    return seq


def relax(p, f):
    # print(f'\n relaxando {p.id} -> {f.id}')
    if p.bf_distancia + p.getArestaFromVertice(f).w < f.bf_distancia:
        f.bf_distancia = p.bf_distancia + p.getArestaFromVertice(f).w
        # nao eh usado no algoritmo mas pode se usado para retorna do 
        # node atual até o pai pelo melhor caminho (menor custo)
        f.bf_pai = p
def bellman_ford(vertices, pai):
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

def dijkstra(vertices, pai, dst):
    # reset node configs
    resetVisitedNodes(vertices)
    for v in vertices:
        v.dj_distancia = float('inf')
        v.dj_pai = None


    print(f'\nComecou em {pai.id}')
    pai.dj_distancia = 0
    q = []
    q.append(pai)
    while q != []:
        pai = q.pop(0)
        for ar in pai.conexoes:
            if ar.dst == dst:
                print(f'\nChegou em {ar.dst.id}')
                ar.dst.dj_distancia = pai.dj_distancia + ar.w
                ar.dst.dj_pai = pai
                
                r = ar.dst.dj_pai
                print(f'{ar.dst.id} <- ', end='')
                while r != None:
                    print(f'{r.id} <- ', end='')
                    r = r.dj_pai
                print(f'\n com distancia de {ar.dst.dj_distancia}')
                return ar.dst

            q.append(ar.dst)
            if pai.dj_distancia + ar.w < ar.dst.dj_distancia:
                ar.dst.dj_distancia = pai.dj_distancia + ar.w
                ar.dst.dj_pai = pai
    

def copilot_floyd_warshall(vertices):
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if i.dj_distancia + j.dj_distancia < k.dj_distancia + j.dj_distancia:
                    k.dj_distancia = i.dj_distancia + j.dj_distancia
                    k.dj_pai = j


def floyd_warshall(vertices):
    pass


def main():
    # vertices ficao guardados como ponteiros dentro de 'vertices'
    vertices = []

    # arestas determina quais conexoes entre os nos sao feitas
    arestas = [(1,2, 2), (1,4, 2), (2,3, -3), (2,4, -1), (3,7, -2), (4,8, 2), (5,7, 1), (5,6, 2), (8,7, 4)]
    
    # * = (nao tem conexao para o resto do grafo entao eles entram depois)
    # bfs -> 1 2 4 3 8 7 * 5 6
    # dfs -> 1 2 3 7 4 8 7 * 5 6



    for i in range(8):
        v = Vertice(i+1)
        vertices.append(v)
   
    # trata de fazer as arestas entre os vertices, arestas orientadas
    # for i in range(len(arestas)):
    #     ipv, iuv = arestas[i]
    #     pv, uv = vertices[ipv-1], vertices[iuv-1]
    #     pv.conexoes.append(uv)
    #     uv.conexoes.append(pv)

    for src, dst, w in arestas:
        vertices[src-1].addAresta(vertices[dst-1], w)

    bfs(vertices, vertices[0])
    dfs(vertices, vertices[0])
    bellman_ford(vertices, vertices[0])
    dijkstra(vertices, vertices[0], vertices[6])
    

if __name__ == "__main__":
    main()