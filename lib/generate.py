


#generate a list of hex center locations in the hex coordinate sytem
def cubic_hex(BOARD_SIZE):
    zone_list_hex=[]
    for x in range(-BOARD_SIZE,BOARD_SIZE+1):
        for y in range(-BOARD_SIZE,BOARD_SIZE+1):
            for z in range(-BOARD_SIZE,BOARD_SIZE+1):
                
                if x+y+z==0:
                    zone_list_hex.append([x,y,z])
                    #print(x,y,z)
    return zone_list_hex


def sorted_zones(num_columns, board_size, zone_list_hex):
    
    board_columns_rows = []
    NTOTAL_HEXES=0

    for i in range(1,num_columns + 1):
        if i <= board_size +1:
            board_columns_rows.append(board_size+i)
        elif i>board_size +1:
            board_columns_rows.append(board_size*2 - (i-board_size-2))
        NTOTAL_HEXES += board_columns_rows[i-1]




    # SORT ZONE_LIST_HEX..... by left -> right (already done) then by up -> down
    zone_list_hex2 = list(zone_list_hex)
    zone_list_hex_sortedtmp = []
    zone_list_hex_sorted = []
    for i in range(1,num_columns+1):
        for k in range(1, board_columns_rows[i-1] +1):
            zone_list_hex_sortedtmp.append(zone_list_hex2.pop(0))
            #print('k3:', i)
        zone_list_hex_sortedtmp.sort(key=lambda x: x[1], reverse=True)
        for k in range(1, board_columns_rows[i-1] + 1):
            zone_list_hex_sorted.append(zone_list_hex_sortedtmp.pop(0))
            #print('k4:', i)
    
    return zone_list_hex_sorted



# returns a list of the hex coordinates of planets in order of players 1-4
# and a list of the hex coordinates of random planets
def generate_planet_placements(bs, config = 1):
    #bs = boardsize
    if config == 1:
        starter_planet_locations = [[-bs,0,bs], [-bs,bs,0], [bs,-bs,0], [bs,0,-bs]]
        unclaimed_planet_locations = [[0,-1,1],[0,1,-1]]
    if config == 2:
        starter_planet_locations = [[-bs,0,bs], [-bs,bs,0], [bs,-bs,0], [bs,0,-bs]]
        unclaimed_planet_locations = [[1,-1,0],[-1,1,0],[1,0,-1],[-1,0,1]]
    if config == 3:
        starter_planet_locations = [[-bs,0,bs], [-bs,bs,0], [bs,-bs,0], [bs,0,-bs]]
        unclaimed_planet_locations = [[0,0,0]]
    if config == 4:
        starter_planet_locations = [[-bs,0,bs], [-bs,bs,0], [bs,-bs,0], [bs,0,-bs]]
        unclaimed_planet_locations = [[1,-1,0],[-1,1,0],[1,0,-1],[-1,0,1],[0,-1,1],[0,1,-1]]
        
    return starter_planet_locations, unclaimed_planet_locations
    
    
#generate ship identifiers - n_colours hues w/ tokens of up to 4 colours
def ship_id_list(n_colours):
    # create a list [1,2,3,...,n_colours]
    in_list = [i for i in range(n_colours)]
    out_list = []
    #create out_list with every possible combination of in_list Choose 1,2,3,and4 
    for i in range(1, 5):
        out_list.extend(itertools.combinations(in_list, i))    


    out_list2 = []
    for i in out_list:
        # translate each combination into an id tag of the form [0,0,1,0,0] denoting which colours it is comprised of
        inter_list = [0 for i in range(n_colours)]
        for j in range(0,n_colours):
            if j in i:
                inter_list[j] = 1
        out_list2.append(inter_list)
    return out_list2
    
    
"""
#define cartesian location of hex centers in pixels
def generateCartHex(zone_list_hex,hex_side_length,height,width):
    zone_pixels_cart=[]
    for liste in zone_list_hex:
        xx = liste[0] * (3/2) * hex_side_length + width/2
        yy =  math.sqrt(3) * hex_side_length * (liste[0]/2 + liste[1]) + height/2
        zone_pixels_cart.append([xx,yy])
    return zone_pixels_cart
"""

"""
#given x,y .. return all verticies of relevant hexagon
#starts at right and goes clockwise
def generateHexVerts(x,y,hex_side_length):
    
    degsyy = 0
    x1= x + hex_side_length * math.cos(math.radians(degsyy))
    y1= y + hex_side_length * math.sin(math.radians(degsyy))
    
    degsyy = 60
    x2= x + hex_side_length * math.cos(math.radians(degsyy))
    y2= y + hex_side_length * math.sin(math.radians(degsyy))
    
    degsyy = 120
    x3= x + hex_side_length * math.cos(math.radians(degsyy))
    y3= y + hex_side_length * math.sin(math.radians(degsyy))
    
    degsyy = 180
    x4= x + hex_side_length * math.cos(math.radians(degsyy))
    y4= y + hex_side_length * math.sin(math.radians(degsyy))
    
    degsyy = 240
    x5= x + hex_side_length * math.cos(math.radians(degsyy))
    y5= y + hex_side_length * math.sin(math.radians(degsyy))
    
    degsyy = 300
    x6= x + hex_side_length * math.cos(math.radians(degsyy))
    y6= y + hex_side_length * math.sin(math.radians(degsyy))
    
    return [[x1,y1],[x2,y2],[x3,y3],[x4,y4],[x5,y5],[x6,y6]]
"""

