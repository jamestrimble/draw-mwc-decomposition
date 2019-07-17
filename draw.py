import math
import svgwrite
import sys

class Graph(object):
    def __init__(self, adjmat, weights):
        self.n = len(adjmat)
        self.adjmat = adjmat
        self.weights = weights

    def calc_vertex_positions(self, width, height):
        x_mid = width / 2
        y_mid = height / 2
        x_quarter = width / 4
        y_quarter = height / 4
        positions = []
        for i in range(self.n):
            angle = i / float(self.n) * 2 * math.pi
            x = math.cos(angle)
            y = math.sin(angle)
            positions.append((x * x_quarter + x_mid, y * y_quarter + y_mid))
        return positions

    def get_edges(self):
        edges = []
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.adjmat[i][j]:
                    edges.append((i, j))
        return edges

    def draw(self, width, height):
        dwg = svgwrite.Drawing("drawing.svg", ("{}px".format(width), "{}px".format(height)))
        dwg.add(dwg.rect((10, 50), (10, 15), fill='blue'))
        positions = self.calc_vertex_positions(width, height)
        for v, w in self.get_edges():
            print v, w
            vx = positions[v][0]
            vy = positions[v][1]
            wx = positions[w][0]
            wy = positions[w][1]
            dwg.add(dwg.line((vx, vy), (wx, wy), stroke='black'))
        for i in range(self.n):
            x = positions[i][0]
            y = positions[i][1]
            dwg.add(dwg.circle((x, y), 10, fill='lightsteelblue', stroke='black'))


        dwg.save()

def read_instance(lines):
    lines = [line.strip().split() for line in lines]
    p_line = [line for line in lines if line[0]=="p"][0]
    n_lines = [line for line in lines if line[0]=="n"]
    e_lines = [line for line in lines if line[0]=="e"]
    n = int(p_line[2])
    weights = [1] * n
#    print "Number of vertices:", n
#    print "Number of edges:", len(e_lines)
    adjmat = [[False] * n for _ in range(n)]
    for e in e_lines:
        v, w = int(e[1])-1, int(e[2])-1
        adjmat[v][w] = adjmat[w][v] = True
    for line in n_lines:
        v, weight = int(e[1])-1, int(e[2])
        weights[v] = weight
#    print "Finished reading instance."
    return Graph(adjmat, weights)

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        g = read_instance([line for line in f.readlines()])
    g.draw(400, 400)
