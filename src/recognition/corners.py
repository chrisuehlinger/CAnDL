import cv2
import numpy as np
import math

def corners(imgpath, debug=False):
    gray = cv2.imread(imgpath, 0)
    inputImage = cv2.imread(imgpath, 1)
    out = cv2.imread(imgpath, 1)
    gray = cv2.medianBlur(gray,5)
    cimg = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
    height, width = gray.shape[:2]
    dots = np.zeros((height,width,3), np.uint8)

    circles = []
    params = cv2.SimpleBlobDetector_Params()
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(gray)
    for kp in keypoints:
        circles.append([int(kp.pt[0]), int(kp.pt[1]), int(kp.size)])

    points = []
    sideCandidates = []
    corners = []
    for i in circles:
        color = inputImage[i[1]][i[0]]
        targetColor = [0,0,255]
        colorDiff = math.sqrt((color[2]-targetColor[2])**2 + (color[1]-targetColor[1])**2 + (color[0]-targetColor[0])**2)
        if colorDiff < 150:
          corners.append([int(i[0]),int(i[1])])
          cv2.circle(dots,(i[0],i[1]),0,(255,255,255),10)
        else:
            sideCandidates.append([int(i[0]), int(i[1]), int(i[2])])
        points.append([int(i[0]), int(i[1]), int(i[2])])

        if debug:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),1)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),0,(0,0,255),1)

    if debug:
        cv2.imshow('detected circles',cimg)
        cv2.waitKey(0)

        cv2.imshow('corners', dots)
        cv2.waitKey(0)

    lines = list()
    for i in range(len(corners)):
        for j in range(i+1, len(corners)):
            p1 = points[i]
            p2 = points[j]
            dist = math.hypot(p1[0]-p2[0], p1[1]-p2[1])
            lines.append(dict(p1=i, p2=j, dist=dist))
    lines = sorted(lines, key=lambda x:x['dist'])

    LENGTH_TOLERANCE = 200.0
    CENTER_TOLERANCE = 200.0
    ANGLE_TOLERANCE = 5.0
    candidateRects = []
    for i in range(len(lines)):
        for j in range(i+1,len(lines)):
            v1 = lines[i]
            v2 = lines[j]

            if math.fabs(v1['dist']-v2['dist']) > LENGTH_TOLERANCE:
                if debug:
                    print 'Broke Length Tolerance: ' + str(math.fabs(v1['dist']-v2['dist']))
                break

            if v1['p1'] == v2['p1'] or v1['p1'] == v2['p2'] or v1['p2'] == v2['p1'] or v1['p2'] == v2['p2']:
                continue

            v1p1 = corners[v1['p1']]
            v1p2 = corners[v1['p2']]
            v2p1 = corners[v2['p1']]
            v2p2 = corners[v2['p2']]
            c1 = [(v1p1[0]+v1p2[0])/2, (v1p1[1]+v1p2[1])/2]
            c2 = [(v2p1[0]+v2p2[0])/2, (v2p1[1]+v2p2[1])/2]
            cdist = math.hypot(c1[0]-c2[0], c1[1]-c2[1])
            if cdist > CENTER_TOLERANCE:
                if debug:
                        print 'Broke Center Tolerance: ' + str(cdist)
                continue

            n1 = [v2p1[1]-v1p1[1],v2p1[0]-v1p1[0]]
            n2 = [v2p2[1]-v1p1[1],v2p2[0]-v1p1[0]]
            a1 = math.atan2(n1[1],n1[0])*180/math.pi
            a2 = math.atan2(n2[1],n2[0])*180/math.pi
            diff1 = a2 - a1
            diff1 = (diff1 + 180) % 360 - 180
            diff1 = math.fabs(diff1)
            if math.fabs(diff1-90.0) < ANGLE_TOLERANCE:
                points = sorted([v1p1, v2p1, v1p2, v2p2], key=lambda p:math.atan2(p[1]-c1[1],p[0]-c1[0]))
                candidateRects.append(dict(points=points))
                if debug:
                    cv2.line(out,(v1p1[0],v1p1[1]),(v2p1[0],v2p1[1]),(0,0,255),1)
                    cv2.line(out,(v1p1[0],v1p1[1]),(v2p2[0],v2p2[1]),(0,0,255),1)
                    cv2.line(out,(v1p2[0],v1p2[1]),(v2p1[0],v2p1[1]),(0,0,255),1)
                    cv2.line(out,(v1p2[0],v1p2[1]),(v2p2[0],v2p2[1]),(0,0,255),1)
                    cv2.circle(out,(c1[0],c1[1]),0,(0,255,0),2)
                    cv2.circle(out,(c2[0],c2[1]),0,(0,255,0),2)
            elif debug:
                print 'Broke Angle Tolerance: ' + str(math.fabs(diff1-90.0))

            if debug:
                print (a1, a2, diff1, math.fabs(diff1-90.0))
            #cv2.imshow('dots', dots)
            #cv2.waitKey(0)

    # Source: https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm

    def doesCollide(circle, line):
        Ax = line[0][0]
        Ay = line[0][1]
        Bx = line[1][0]
        By = line[1][1]
        Cx = circle[0]
        Cy = circle[1]
        R = circle[2]

        # compute the euclidean distance between A and B
        LAB = math.sqrt( (Bx-Ax)**2+(By-Ay)**2 )

        # compute the direction vector D from A to B
        Dx = (Bx-Ax)/LAB
        Dy = (By-Ay)/LAB

        # Now the line equation is x = Dx*t + Ax, y = Dy*t + Ay with 0 <= t <= 1.

        # compute the value t of the closest point to the circle center (Cx, Cy)
        t = Dx*(Cx-Ax) + Dy*(Cy-Ay)

        # This is the projection of C on the line from A to B.

        # compute the coordinates of the point E on line and closest to C
        Ex = t*Dx+Ax
        Ey = t*Dy+Ay

        # compute the euclidean distance from E to C
        LEC = math.sqrt( (Ex-Cx)**2+(Ey-Cy)**2)

        # test if the line intersects the circle
        return LEC < R and t > 0 and t < LAB


    COLOR_VALUES = [
      [59,168,112], # Green
      [177,114,73], # Blue
      [0,150,219], # Orange
    ]
    COLOR_TOLERANCE = 150
    for rect in candidateRects:
        rect['sides'] = []
        rect['values'] = []
        for i in range(-1,3):
            p1 = rect['points'][i]
            p2 = rect['points'][i+1]
            line = [p1,p2]
            side = dict(circles=[])
            for circle in sideCandidates:
                if doesCollide(circle, line):
                    side['circles'].append(circle)
                    # draw the outer circle
                    cv2.circle(out,(circle[0],circle[1]),circle[2],(0,255,0),2)

            side['circles'] = sorted(side['circles'], key=lambda c:math.hypot(p1[1]-c[1],p1[0]-c[0]))

            side['value']=0
            for j in range(len(side['circles'])):
                circle = side['circles'][j]
                color = inputImage[circle[1]][circle[0]]
                shortestDist = COLOR_TOLERANCE
                shortestDistIndex = 100
                for target in range(len(COLOR_VALUES)):
                    targetColor = COLOR_VALUES[target]
                    colorDiff = math.sqrt((color[2]-targetColor[2])**2 + (color[1]-targetColor[1])**2 + (color[0]-targetColor[0])**2)
                    if colorDiff < shortestDist:
                        shortestDist = colorDiff
                        shortestDistIndex = target

                if shortestDistIndex < 100:
                    side['value'] += shortestDistIndex*len(COLOR_VALUES)**j

            rect['sides'].append(side)
            rect['values'].append(side['value'])
        print rect['values']

    savedTemplates = [
        {
            'values':[58,22,22,58],
            'name':'test1'
        },
        {
            'values':[73,73,73,73],
            'name':'test2'
        }
    ]
    validRects = []
    for rect in candidateRects:
        isValid = False
        for template in savedTemplates:
            if len(template['values']) != len(rect['values']):
                continue

            for i in range(-len(rect['values'])+1, 1):
                attempt = [int(rect['values'][i]), int(rect['values'][i+1]), int(rect['values'][i+2]), int(rect['values'][i+3])]
                if attempt == template['values']:
                    validRect = {
                        'values':template['values'],
                        'points':[rect['points'][i], rect['points'][i+1], rect['points'][i+2], rect['points'][i+3]],
                        'name': template['name']
                    }
                    validRects.append(validRect)
                    isValid = True
                    break

            if isValid:
                break

    if debug:
        for rect in validRects:
            print rect
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(out,rect['name'],(rect['points'][0][0],rect['points'][0][1]), font, 0.5,(0,0,0),1,cv2.LINE_AA)

        cv2.destroyAllWindows()
        cv2.imshow('next',out)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return validRects
