"""
THIS CODE IS NOT USED IN THE MAIN GAME.
IT GENERATES COLOUR TOKENS AS IMAGES TO BE PRINTED AND THEN USED IN GAMEPLAY
"""

#IMPORTS
from itertools import combinations
from PIL import Image
import colorsys

#DEFINE SIZE OF OUTPUT IMAGE TOKENS, AND THE RATIO OF BLACK TO COLOUR USED
SIZEE = 50
BLACKRATIO = 0.2
def hsv2rgb(h,s,v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    
#HARDCODED COLOURS (IN OPENCV HSV SPACE)
#new new way (corrects for bad printer alignment)
list_of_pixels = []
for bb in [25, 81, 140, 268, 335]:
    list_of_pixels.append(hsv2rgb(bb/360,1,1))
"""
list_of_pixels.append(hsv2rgb(25/360,1,1))
list_of_pixels.append(hsv2rgb(81/360,1,1))
list_of_pixels.append(hsv2rgb(140/360,1,1))
list_of_pixels.append(hsv2rgb(268/360,1,1))
list_of_pixels.append(hsv2rgb(335/360,1,1))
list_of_pixels
"""

rgbCombos1 = list(combinations(list_of_pixels, 1))
rgbCombos2 = list(combinations(list_of_pixels, 2))
rgbCombos3 = list(combinations(list_of_pixels, 3))
rgbCombos4 = list(combinations(list_of_pixels, 4))
print(len(rgbCombos1))
print(rgbCombos1)

def save1Images(aaa,modd):
    imx = Image.new('RGB', (int(SIZEE*(2+BLACKRATIO)),int(SIZEE*(2+BLACKRATIO))),rgbCombos1[aaa][0])
    imx.save(str(aaa+modd)+".png")

def save2Images(aaa,modd):
    im1 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos2[aaa][0])
    im2 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos2[aaa][1])
    im3 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos2[aaa][0])
    im4 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos2[aaa][1])
    imx = Image.new('RGB', (int(SIZEE*(2+BLACKRATIO)),int(SIZEE*(2+BLACKRATIO))))
    imx.paste(im1, (0,0))
    imx.paste(im2, (int(SIZEE*(1+BLACKRATIO)),0))
    imx.paste(im2, (0,int(SIZEE*(1+BLACKRATIO))))
    imx.paste(im1, (int(SIZEE*(1+BLACKRATIO)),int(SIZEE*(1+BLACKRATIO))))
    imx.save(str(aaa+modd)+".png")
#imx.show()


def save3Images(aaa,modd):
    im1 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos3[aaa][0])
    im2 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos3[aaa][1])
    im3 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos3[aaa][2])
    im4 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos3[aaa][0])
    imx = Image.new('RGB', (int(SIZEE*(2+BLACKRATIO)),int(SIZEE*(2+BLACKRATIO))))
    imx.paste(im1, (0,0))
    imx.paste(im2, (int(SIZEE*(1+BLACKRATIO)),0))
    imx.paste(im3, (0,int(SIZEE*(1+BLACKRATIO))))
    imx.paste(im1, (int(SIZEE*(1+BLACKRATIO)),int(SIZEE*(1+BLACKRATIO))))
    imx.save(str(aaa+modd)+".png")
    
def save4Images(aaa,modd):
    im1 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos4[aaa][0])
    im2 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos4[aaa][1])
    im3 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos4[aaa][2])
    im4 = Image.new('RGB', (SIZEE,SIZEE),rgbCombos4[aaa][3])
    imx = Image.new('RGB', (int(SIZEE*(2+BLACKRATIO)),int(SIZEE*(2+BLACKRATIO))))
    imx.paste(im1, (0,0))
    imx.paste(im2, (int(SIZEE*(1+BLACKRATIO)),0))
    imx.paste(im3, (0,int(SIZEE*(1+BLACKRATIO))))
    imx.paste(im4, (int(SIZEE*(1+BLACKRATIO)),int(SIZEE*(1+BLACKRATIO))))
    imx.save(str(aaa+modd)+".png")
    
    
for i in range(len(rgbCombos1)):
    save1Images(i,0)
for i in range(len(rgbCombos2)):
    save2Images(i,len(rgbCombos1))
for i in range(len(rgbCombos3)):
    save3Images(i,len(rgbCombos1) + len(rgbCombos2))
for i in range(len(rgbCombos4)):
    save4Images(i,len(rgbCombos1) + len(rgbCombos2) + len(rgbCombos3))
