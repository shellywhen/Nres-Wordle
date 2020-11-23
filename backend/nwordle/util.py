import numpy as np
from colormath.color_objects import AdobeRGBColor, HSLColor, LCHabColor
from colormath.color_conversions import convert_color
from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage, misc
import random
import time

def constructBox(layout, width, height):
    total = len(layout)
    xlist = []
    ylist = []
    flag = np.array([[False for j in range(4)] for i in range(total)])  # x1 y1 x2 y2 flag=false means continue
    typelist = [[False for j in range(4)] for i in range(total)]  # false means expand
    stopIter = True
    for (word, count), font_size, position, box, orientation, color in layout:
        y, x = position
        w, h = box
        h = font_size
        xlist.append([x, x+w])
        ylist.append([y, y+h])
    for a in range(total):
        cross = [False for i in range(4)]
        corner = [False for i in range(4)]
        for b in range(total):
            if ylist[a][0] < ylist[b][1] and ylist[a][0] > ylist[b][0]:  # y0 cross
                if xlist[a][0] < xlist[b][1] and xlist[a][0] > xlist[b][0]:  # x0 cross
                    cross[0] = True
                    cross[1] = True
                    corner[0] = True
                if xlist[a][1] < xlist[b][1] and xlist[a][1] > xlist[b][0]:  # x1 cross
                    cross[1] = True
                    cross[2] = True
                    corner[1] = True
                if xlist[a][1] > xlist[b][1] and xlist[a][0] < xlist[b][0]:  # x0 x1 between
                    cross[1] = True
                if xlist[b][1] > xlist[a][1] and xlist[b][0] < xlist[a][0]:
                    cross[1] = True
            if ylist[a][1] < ylist[b][1] and ylist[a][1] > ylist[b][0]: # y1 cross
                if xlist[a][1] < xlist[b][1] and xlist[a][1] > xlist[b][0]:  # x1 cross
                    corner[2] = True
                    cross[2] = True
                    cross[3] = True
                if xlist[a][0] < xlist[b][1] and xlist[a][0] > xlist[b][0]:  # x0 cross
                    corner[3] = True
                    cross[3] = True
                    cross[0] = True
                if xlist[a][1] > xlist[b][1] and xlist[a][0] < xlist[b][0]:  # x1 x0 between
                    cross[3] = True
                if xlist[b][1] > xlist[a][1] and xlist[b][0] < xlist[a][0]:
                    cross[3] = True
            if ylist[b][1] < ylist[a][1] and ylist[b][0] > ylist[a][0]:  # y0 y1 inner between
                if xlist[a][0] > xlist[b][0] and xlist[a][0] < xlist[b][1]:  # x0 cross
                    cross[0] = True
                if xlist[a][1] > xlist[b][0] and xlist[a][1] < xlist[b][1]:  # x1 cross
                    cross[2] = True
            if ylist[b][1] > ylist[a][1] and ylist[b][0] < ylist[a][0]:  # y0 y1 outer over
                if xlist[a][0] > xlist[b][0] and xlist[a][0] < xlist[b][1]:  # x0 cross
                    cross[0] = True
                if xlist[a][1] > xlist[b][0] and xlist[a][1] < xlist[b][1]:  # x1 cross
                    cross[2] = True
        typelist[a] = cross
    k = 0
    while (stopIter and k < int(max(height, width)/2)):
        k += 1
#         if k%100==0:
#             print('iter:', k, flag)
        for a in range(total):
            if all(flag[a]):
                continue
            cross = [False for i in range(4)]  # indicates the l/u/r/b whether has a cross
            for b in range(total):
                if a == b:
                    continue
                if ylist[a][0] <= ylist[b][1] and ylist[a][0] >= ylist[b][0]:  # y0 cross
                    if xlist[a][0] <= xlist[b][1] and xlist[a][0] >= xlist[b][0]:  # x0 cross
                        cross[0] = True
                        cross[1] = True
                    if xlist[a][1] <= xlist[b][1] and xlist[a][1] >= xlist[b][0]:  # x1 cross
                        cross[1] = True
                        cross[2] = True
                    if xlist[a][1] >= xlist[b][1] and xlist[a][0] <= xlist[b][0]:  # x0 x1 between
                        cross[1] = True
                    if xlist[b][1] >= xlist[a][1] and xlist[b][0] <= xlist[a][0]:
                        cross[1] = True
                if ylist[a][1] <= ylist[b][1] and ylist[a][1] >= ylist[b][0]: # y1 cross
                    if xlist[a][1] < xlist[b][1] and xlist[a][1] > xlist[b][0]:  # x1 cross
                        cross[2] = True
                        cross[3] = True
                    if xlist[a][0] <= xlist[b][1] and xlist[a][0] >= xlist[b][0]:  # x0 cross
                        cross[3] = True
                        cross[0] = True
                    if xlist[a][1] >= xlist[b][1] and xlist[a][0] <= xlist[b][0]:  # x1 x0 between
                        cross[3] = True
                    if xlist[b][1] >= xlist[a][1] and xlist[b][0] <= xlist[a][0]:
                        cross[3] = True
                if ylist[b][1] <= ylist[a][1] and ylist[b][0] >= ylist[a][0]:  # y0 y1 inner between
                    if xlist[a][0] >= xlist[b][0] and xlist[a][0] <= xlist[b][1]:  # x0 cross
                        cross[0] = True
                    if xlist[a][1] >= xlist[b][0] and xlist[a][1] <= xlist[b][1]:  # x1 cross
                        cross[2] = True
                if ylist[b][1] >= ylist[a][1] and ylist[b][0] <= ylist[a][0]:  # y0 y1 outer over
                    if xlist[a][0] >= xlist[b][0] and xlist[a][0] <= xlist[b][1]:  # x0 cross
                        cross[0] = True
                    if xlist[a][1] >= xlist[b][0] and xlist[a][1] <= xlist[b][1]:  # x1 cross
                        cross[2] = True
            if not flag[a][0]:
                if not typelist[a][0]:
                    if not cross[0]:
                        xlist[a][0] -= 1
                    if cross[0] or xlist[a][0]==0:
                        flag[a][0] = True
                else:
                    if cross[0]:
                        xlist[a][0] += 1
                    if not cross[0] or xlist[a][1]-xlist[a][0]<layout[a][3][0]*0.7:
                        flag[a][0] = True
            if not flag[a][1]:
                if typelist[a][1]:
                    if cross[1]:
                        ylist[a][0] += 1
                    if ylist[a][1]-ylist[a][0]<layout[a][3][1]*0.7 or not cross[1]:
                        flag[a][1] = True
                else:
                    if not cross[1]:
                        ylist[a][0] -= 1
                    if ylist[a][0]==0 or cross[1]:
                        flag[a][1] = True
            if not flag[a][2]:
                if typelist[a][2]:
                    if cross[2]:
                        xlist[a][1] -= 1
                    if xlist[a][1]-xlist[a][0]<layout[a][3][0]*0.7 or not cross[2]:
                        flag[a][2] = True
                else:
                    if not cross[2]:
                        xlist[a][1] += 1
                    if xlist[a][1] == width-1 or cross[2]:
                        flag[a][2] = True
            if not flag[a][3]:
                if typelist[a][3]:
                    if cross[3]:
                        ylist[a][1] -= 1
                    if ylist[a][1]-ylist[a][0]<layout[a][3][1]*0.7 or not cross[3]:
                        flag[a][3] = True
                else:
                    if not cross[3]:
                        ylist[a][1] += 1
                    if ylist[a][1]==height-1 or cross[3]:
                        flag[a][3] = True
        stopIter = not all(flag.flatten())
    print(k)

    for a in range(total):
        x1list = []
        x0list = []
        y0list = []
        y1list = []
        for b in range(total):
            if a == b:
                continue
            if (ylist[b][0]>=ylist[a][0] and ylist[b][0]<=ylist[a][1]) \
             or (ylist[b][1] <= ylist[a][1] and ylist[b][1] >= ylist[a][0])\
             or (ylist[b][0]>=ylist[a][0] and ylist[b][1]<=ylist[a][1]) \
             or (ylist[b][0]<=ylist[a][0] and ylist[b][1]>ylist[a][1]):
                if xlist[b][1] <= xlist[a][0]:
                    x1list.append(xlist[b][1])
                if xlist[b][0] >= xlist[a][1]:
                    x0list.append(xlist[b][0])
            if (xlist[b][0]>=xlist[a][0] and xlist[b][0]<=xlist[a][1]) \
              or (xlist[b][1] <= xlist[a][1] and xlist[b][1] >= xlist[a][0])\
              or (xlist[b][0]>=xlist[a][0] and xlist[b][1]<=xlist[a][1]) \
              or (xlist[b][0]<=xlist[a][0] and xlist[b][1]>xlist[a][1]):
                if ylist[b][1] <= ylist[a][0]:
                    y1list.append(ylist[b][1])
                if ylist[b][0] >= ylist[a][1]:
                    y0list.append(ylist[b][0])
        xlist[a][0] = 0 if len(x1list)==0 else max(x1list)
        xlist[a][1] = width if len(x0list)==0 else min(x0list)
        ylist[a][0] = 0 if len(y1list)==0 else max(y1list)
        ylist[a][1] = height if len(y0list)==0 else min(y0list)
    result = []
    for idx, item in enumerate(layout):
        (word, count), font_size, position, box, orientation, color = item
        orientation = (xlist[idx][0], ylist[idx][0], xlist[idx][1]-xlist[idx][0], ylist[idx][1]-ylist[idx][0])
        result.append(((word, count), font_size, position, box, orientation, color))
    return result

def wordToid(wordlist, keyname='word'):
    mapping = {}
    for idx, item in enumerate(wordlist):
        mapping[item['word']] = idx
    return mapping

def colorAdjust(layout, ctype=0, origin='rgb(0,0,0)'):
    result = []
    for item in layout:
        (word, count), font_size, (x,y), (width,height), orientation, color = item
        [r, g ,b] = origin.replace('rgb(', '').replace(')', '').split(',')
        rgbObj = AdobeRGBColor(r, g, b)
        l, c, h = convert_color(rgbObj, LCHabColor).get_value_tuple()
        if ctype == 0:  # base
            l = random.randint(4300, 4700)
            c = random.randint(2300, 2500)
            h = random.randint(0, 2500)
        if ctype == 1:   # inner
            l = random.randint(3000, 3500)
            c += random.randint(-30, 0)
            h += random.randint(-60, 60)
        if ctype == 2:   # outer
            l = random.randint(3000, 5000)
            c += random.randint(-10, 30)
            h += random.randint(-30, 30)
        nr, ng, nb = convert_color(LCHabColor(l, c, h), AdobeRGBColor).get_value_tuple()
        color = f'rgb({int(nr)},{int(ng)},{int(nb)})'
        result.append(((word, count), font_size, (x,y), (width,height), orientation, color))
    return result

def getBackground(cropped, filtersize=20):
    mask = np.array(cropped)
    background = np.ones(mask.shape)
    dilate_image_arr = ndimage.minimum_filter(mask, size=filtersize)
    dilate_image = np.uint8(dilate_image_arr)
    background[dilate_image==255] = 0
    background[dilate_image!=255] = 255
    background = np.uint8(background)
    return background

def getForeGround(cropped, filtersize=20):
    mask = np.array(cropped)
    foreground = np.ones(mask.shape)
    dilate_image_arr = ndimage.minimum_filter(mask, size=filtersize)
    dilate_image = np.uint8(dilate_image_arr)
    return dilate_image
