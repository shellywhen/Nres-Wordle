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
        for b in range(total):
             if ylist[a][0] < ylist[b][1] and ylist[a][0] > ylist[b][0]:  # y0 cross
                if xlist[a][0] < xlist[b][1] and xlist[a][0] > xlist[b][0]:  # x0 cross
                    cross[0] = True
                    cross[1] = True
                if xlist[a][1] < xlist[b][1] and xlist[a][1] > xlist[b][0]:  # x1 cross
                    cross[1] = True
                    cross[2] = True
                if xlist[a][1] > xlist[b][1] and xlist[a][0] < xlist[b][0]:  # x0 x1 between
                    cross[1] = True
                if xlist[b][1] > xlist[a][1] and xlist[b][0] < xlist[a][0]:
                    cross[1] = True
            if ylist[a][1] < ylist[b][1] and ylist[a][1] > ylist[b][0]: # y1 cross
                if xlist[a][1] < xlist[b][1] and xlist[a][1] > xlist[b][0]:  # x1 cross
                    cross[2] = True
                    cross[3] = True
                if xlist[a][0] < xlist[b][1] and xlist[a][0] > xlist[b][0]:  # x0 cross
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
    while (stopIter and k < 500):
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
                if ylist[a][0] < ylist[b][1] and ylist[a][0] > ylist[b][0]:  # y0 cross
                    if xlist[a][0] < xlist[b][1] and xlist[a][0] > xlist[b][0]:  # x0 cross
                        cross[0] = True
                        cross[1] = True
                    if xlist[a][1] < xlist[b][1] and xlist[a][1] > xlist[b][0]:  # x1 cross
                        cross[1] = True
                        cross[2] = True
                    if xlist[a][1] > xlist[b][1] and xlist[a][0] < xlist[b][0]:  # x0 x1 between
                        cross[1] = True
                    if xlist[b][1] > xlist[a][1] and xlist[b][0] < xlist[a][0]:
                        cross[1] = True
                if ylist[a][1] < ylist[b][1] and ylist[a][1] > ylist[b][0]: # y1 cross
                    if xlist[a][1] < xlist[b][1] and xlist[a][1] > xlist[b][0]:  # x1 cross
                        cross[2] = True
                        cross[3] = True
                    if xlist[a][0] < xlist[b][1] and xlist[a][0] > xlist[b][0]:  # x0 cross
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
            if not flag[a][0]:
                if not typelist[a][0]:
                    xlist[a][0] -= 1
                    if cross[0] or xlist[a][0]==0:
                        flag[a][0] = True
                else:
                    xlist[a][0] += 1
                    if not cross[0] or xlist[a][1]-xlist[a][0]<layout[a][3][0]/2:
                        flag[a][0] = True
            if not flag[a][1]:
                if typelist[a][1]:
                    ylist[a][0] += 1
                    if ylist[a][1]-ylist[a][0]<layout[a][3][1]/2 or not cross[1]:
                        flag[a][1] = True
                else:
                    ylist[a][0] -= 1
                    if ylist[a][0]==0 or cross[1]:
                        flag[a][1] = True
            if not flag[a][2]:
                if typelist[a][2]:
                    xlist[a][1] -= 1
                    if xlist[a][1]-xlist[a][0]<layout[a][3][0]/2 or not cross[2]:
                        flag[a][2] = True
                else:
                    xlist[a][1] += 1
                    if xlist[a][1] == width-1 or cross[2]:
                        flag[a][2] = True
            if not flag[a][3]:
                if typelist[a][3]:
                    ylist[a][1] -= 1
                    if ylist[a][1]-ylist[a][0]<layout[a][3][1]/2 or not cross[3]:
                        flag[a][3] = True
                else:
                    ylist[a][1] += 1
                    if ylist[a][1]==height-1 or cross[3]:
                        flag[a][3] = True
        stopIter = not all(flag.flatten())
    print(flag, k)
    result = []
    for idx, item in enumerate(layout):
        (word, count), font_size, position, box, orientation, color = item
        orientation = (xlist[idx][0], ylist[idx][0], xlist[idx][1]-xlist[idx][0], ylist[idx][1]-ylist[idx][0])
        result.append(((word, count), font_size, position, box, orientation, color))
    return result
