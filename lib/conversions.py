import math

#FUNCTION DEFINITIONS
def cubic_to_cart(xxyyzz, HexTiles, GameBoard):
    x = xxyyzz[0]  * (3/2) * HexTiles.side_length + GameBoard.width/2
    y = math.sqrt(3) * HexTiles.side_length * (xxyyzz[0]/2 + xxyyzz[1]) + GameBoard.height/2
    return x, y


neighbours_list = [[1,-1,0],[1,0,-1],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1]]
def hex_neighbours(xxyyzz, zone_list_hex):
    nbrs = []
    for x in range(len(neighbours_list)):
        a = [xxyyzz[i] + neighbours_list[x][i] for i in range(len(xxyyzz))]
        if a in zone_list_hex:
            nbrs.append(a)
    return nbrs

