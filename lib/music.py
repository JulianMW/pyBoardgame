import numpy as np


global hsvrng1a, hsvrng1ax, hsvrng2a, hsvrng3a, hsvrng4a, hsvrng5a, hsvrng6a
global hsvrng1b, hsvrng1bx, hsvrng2b, hsvrng3b, hsvrng4b, hsvrng5b, hsvrng6b
global hsv1frame, hsv2frame, hsv3frame, hsv4frame, hsv5frame, hsv6frame


# DEFINE colour thresholds
hsvrng1a = np.array([0*179/360,saturtna,vallua])
hsvrng1ax = np.array([340*179/360,saturtna,vallua])
hsvrng2a = np.array([(60-dftl)*179/360,saturtna,vallua])
hsvrng3a = np.array([(120-dftl)*179/360,saturtna,vallua])
hsvrng4a = np.array([(180-dftl)*179/360,saturtna,vallua])
hsvrng5a = np.array([(240-dftl)*179/360,saturtna,vallua])
hsvrng6a = np.array([(290-dftl)*179/360,saturtna,vallua])

hsvrng1b = np.array([(dftl)*179/360,saturtnb,vallub])
hsvrng1bx = np.array([(359.9)*179/360,saturtnb,vallub])
hsvrng2b = np.array([(60+dftl)*179/360,saturtnb,vallub+20])
hsvrng3b = np.array([(120+dftl)*179/360,saturtnb,vallub])
hsvrng4b = np.array([(180+dftl)*179/360,saturtnb,vallub])
hsvrng5b = np.array([(240+dftl)*179/360,saturtnb,vallub])
hsvrng6b = np.array([(300+dftl)*179/360,saturtnb,vallub])


#takes in a r
def setColourThresholds(dftl = 20,saturtna = 60,vallua = 60,saturtnb = 255,vallub = 155,sat_dftl = 20,val_dftl = 20):

    if ControlBoard.control_boards_list[0].col_hues[0] < dftl:
        hsvrng1a = np.array([(  0  ),  int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl),
                             int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1b = np.array([(ControlBoard.control_boards_list[0].col_hues[0]+dftl)*180/360, 
                             int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl), 
                             int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        hsvrng1ax = np.array([( 360 - dftl + ControlBoard.control_boards_list[0].col_hues[0])*180/360  , 
                              int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl), 
                              int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1bx = np.array([(  360  )*180/360,  int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl), 
                              int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
    elif ControlBoard.control_boards_list[0].col_hues[0] > (360 - dftl):
        hsvrng1a = np.array([(  0  ),  int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl), 
                             int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1b = np.array([(ControlBoard.control_boards_list[0].col_hues[0]+dftl)*180/360, 
                             int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl), 
                             int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        hsvrng1ax = np.array([(ControlBoard.control_boards_list[0].col_hues[0] - dftl)*180/360  , 
                              int(ControlBoard.control_boards_list[0].col_sats[0] - sat_dftl), 
                              int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1bx = np.array([(  dftl - (360 -  ControlBoard.control_boards_list[0].col_hues[0])  )*180/360, 
                              int(ControlBoard.control_boards_list[0].col_sats[0] + sat_dftl), 
                              int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
    else:
        hsvrng1a = np.array([(ControlBoard.control_boards_list[0].col_hues[0]
                              -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] -
                                                 sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1ax = np.array([(ControlBoard.control_boards_list[0].col_hues[0]
                               -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] -
                                                  sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] - val_dftl)])
        hsvrng1b = np.array([(ControlBoard.control_boards_list[0].col_hues[0] +
                              dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] +
                                                sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        hsvrng1bx = np.array([(ControlBoard.control_boards_list[0].col_hues[0] +
                               dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[0] +
                                                 sat_dftl),int(ControlBoard.control_boards_list[0].col_vals[0] + val_dftl)])
        
                            
        

    #hsvrng1a =  np.array([  0,int(ControlBoard.control_boards_list[0].col_sats[1]/2),int(ControlBoard.control_boards_list[0].col_vals[1]/2)])
    #hsvrng1ax = np.array([340*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]/2),int(ControlBoard.control_boards_list[0].col_vals[1]/2)])
    
    hsvrng2a = np.array([(ControlBoard.control_boards_list[0].col_hues[1]
                          -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]/2),
                         int(ControlBoard.control_boards_list[0].col_vals[1]/2)])
    hsvrng3a = np.array([(ControlBoard.control_boards_list[0].col_hues[2]
                          -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[2]/2),
                         int(ControlBoard.control_boards_list[0].col_vals[2]/2)])
    hsvrng4a = np.array([(ControlBoard.control_boards_list[0].col_hues[3]
                          -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[3]/2),
                         int(ControlBoard.control_boards_list[0].col_vals[3]/2)])
    hsvrng5a = np.array([(ControlBoard.control_boards_list[0].col_hues[4]
                          -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[4]/2),
                         int(ControlBoard.control_boards_list[0].col_vals[4]/2)])
    hsvrng6a = np.array([(ControlBoard.control_boards_list[0].col_hues[5]
                          -dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[5]/2),
                         int(ControlBoard.control_boards_list[0].col_vals[5]/2)])

    #hsvrng1b =  np.array([(dftl)*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]+20),int(ControlBoard.control_boards_list[0].col_vals[1]+20)])
    #hsvrng1bx = np.array([(359.9)*180/360,int(ControlBoard.control_boards_list[0].col_sats[1]+20),int(ControlBoard.control_boards_list[0].col_vals[1]+20)])
    
    hsvrng2b = np.array([(ControlBoard.control_boards_list[0].col_hues[1]+dftl)*180/360,
                         int(ControlBoard.control_boards_list[0].col_sats[1]+20),
                         int(ControlBoard.control_boards_list[0].col_vals[1]+20)])
    hsvrng3b = np.array([(ControlBoard.control_boards_list[0].col_hues[2]+dftl)*180/360,
                         int(ControlBoard.control_boards_list[0].col_sats[2]+20),
                         int(ControlBoard.control_boards_list[0].col_vals[2]+20)])
    hsvrng4b = np.array([(ControlBoard.control_boards_list[0].col_hues[3]+dftl)*180/360,
                         int(ControlBoard.control_boards_list[0].col_sats[3]+20),
                         int(ControlBoard.control_boards_list[0].col_vals[3]+20)])
    hsvrng5b = np.array([(ControlBoard.control_boards_list[0].col_hues[4]+dftl)*180/360,
                         int(ControlBoard.control_boards_list[0].col_sats[4]+20),
                         int(ControlBoard.control_boards_list[0].col_vals[4]+20)])
    hsvrng6b = np.array([(ControlBoard.control_boards_list[0].col_hues[5]+dftl)*180/360,
                         int(ControlBoard.control_boards_list[0].col_sats[5]+20),
                         int(ControlBoard.control_boards_list[0].col_vals[5]+20)])


#generate a list of hex center locations in the hex coordinate sytem
def generateCubicHex(BOARD_SIZE):
    zone_list_hex=[]
    for x in range(-BOARD_SIZE,BOARD_SIZE+1):
        for y in range(-BOARD_SIZE,BOARD_SIZE+1):
            for z in range(-BOARD_SIZE,BOARD_SIZE+1):
                
                if x+y+z==0:
                    zone_list_hex.append([x,y,z])
                    #print(x,y,z)
    return zone_list_hex
    

