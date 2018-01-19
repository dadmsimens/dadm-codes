import numpy as np


def rotate(v, rx, ry, rz):

    thetax = np.radians(rx)
    thetay = np.radians(ry)
    thetaz = np.radians(rz)

    cx, sx = np.cos(thetax), np.sin(thetax)
    cy, sy = np.cos(thetay), np.sin(thetay)
    cz, sz = np.cos(thetaz), np.sin(thetaz)

    rox = np.matrix([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    roy = np.matrix([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    roz = np.matrix([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])

    v = np.round(np.array(v * rox * roy * roz).flatten(), 4)

    return v


def transrotateplane(imavol, rotx, roty, rotz, transx, transy, transz):

    v1 = np.array([0, 0, 1])
    v2 = rotate(v1, 90, 0, 0)
    v3 = rotate(v1, 0, -90, 0)

    v1 = rotate(v1, rotx, roty, rotz)
    v2 = rotate(v2, rotx, roty, rotz)
    v3 = rotate(v3, rotx, roty, rotz)

    point = np.array([imavol.shape[0]/2 + transx, imavol.shape[1]/2 + transy, 0 + transz])

    shapes = sorted(imavol.shape)

    meshsize = np.sqrt(np.square(shapes[-1])+np.square(shapes[-2]))

    p, q = np.meshgrid(range(int(1.2 * meshsize)), range(int(1.2 * meshsize)))

    x = point[0] + v2[0] * p + v3[0] * q
    y = point[1] + v2[1] * p + v3[1] * q
    z = point[2] + v2[2] * p + v3[2] * q

    x = x - 1 / 2 * imavol.shape[0]
    y = y - 1 / 2 * imavol.shape[1]

    return [x, y, z]


def interpolatemri(imavol, x, y, z):

   xindmax = imavol.shape[0]
   yindmax = imavol.shape[1]
   zindmax = imavol.shape[2]
   xindmin = 0
   yindmin = 0
   zindmin = 0
   pointsimage = np.zeros(shape=(x.shape[0],x.shape[1]))

   for i in range(x.shape[0]):
       for j in range(x.shape[1]):

           x0 = round(x[i, j], 1)
           y0 = round(y[i, j], 1)
           z0 = round(z[i, j], 1)

           if xindmin <= x0 <= (xindmax - 1) and (yindmax - 1) >= y0 >= yindmin and zindmin <= z0 <= (zindmax - 1):
               x01 = int(np.floor(x0))
               x02 = int(np.ceil(x0))
               y01 = int(np.floor(y0))
               y02 = int(np.ceil(y0))
               z01 = int(np.floor(z0))
               z02 = int(np.ceil(z0))


               if x0 % 1 == 0 and y0 % 1 == 0 and z0 % 1 == 0:

                   pointsimage[i, j] = imavol[int(x0), int(y0), int(z0)]

               else:
                   if x0 % 1 == 0 and z0 % 1 == 0:
                       pointsimage[i, j] = (imavol[int(x0), y01, int(z0)] + imavol[int(x0), y02, int(z0)]) / 2

                   elif x0 % 1 == 0 and y0 % 1 == 0:
                       pointsimage[i, j] = (imavol[int(x0), int(y0), z01] + imavol[int(x0), int(y0), z02]) / 2

                   elif y0 % 1 == 0 and z0 % 1 == 0:
                       pointsimage[i, j] = (imavol[x01, int(y0), int(z0)] + imavol[x02, int(y0), int(z0)]) / 2

                   else:

                       pointsimage[i,j] = imavol[x01, y01, z01] + imavol[x02, y01, z01] + imavol[x01, y02, z01] + imavol[x01, y01, z02] + imavol[x01, y02, z02] + imavol[x02, y01, z02] + imavol[x02, y02, z02] + imavol[x02, y02, z01]

                       nrofpoints = 8
                       d1 = np.sqrt(np.square(x0 - x01) + np.square(y0 - y01) + np.square(z0 - z01))
                       d2 = np.sqrt(np.square(x0 - x02) + np.square(y0 - y01) + np.square(z0 - z01))
                       d3 = np.sqrt(np.square(x0 - x01) + np.square(y0 - y02) + np.square(z0 - z01))
                       d4 = np.sqrt(np.square(x0 - x01) + np.square(y0 - y01) + np.square(z0 - z02))
                       d5 = np.sqrt(np.square(x0 - x01) + np.square(y0 - y02) + np.square(z0 - z02))
                       d6 = np.sqrt(np.square(x0 - x02) + np.square(y0 - y01) + np.square(z0 - z02))
                       d7 = np.sqrt(np.square(x0 - x02) + np.square(y0 - y02) + np.square(z0 - z02))
                       d8 = np.sqrt(np.square(x0 - x02) + np.square(y0 - y02) + np.square(z0 - z01))

                       if d1 > 1 or x01 == x02:
                           nrofpoints = nrofpoints - 1
                           pointsimage[i, j] = pointsimage[i, j] - imavol[x01, y01, z01]

                       if d2 > 1:
                           nrofpoints = nrofpoints - 1
                           pointsimage[i, j] = pointsimage[i, j] - imavol[x02, y01, z01]

                       if d3 > 1 or y01 == y02:
                           nrofpoints = nrofpoints - 1
                           pointsimage[i, j] = pointsimage[i, j] - imavol[x01, y02, z01]

                       if d4 > 1 or z01 == z02:
                           nrofpoints = nrofpoints - 1
                           pointsimage[i, j] = pointsimage[i, j] - imavol[x01, y01, z02]

                       if d5 > 1:
                           nrofpoints = nrofpoints - 1
                           pointsimage[i, j] = pointsimage[i, j] - imavol[x01, y02, z02]

                       if d6 > 1:
                           nrofpoints = nrofpoints - 1
                           pointsimage[i, j] = pointsimage[i, j] - imavol[x02, y01, z02]

                       if d7 > 1:
                           nrofpoints = nrofpoints - 1
                           pointsimage[i, j] = pointsimage[i, j] - imavol[x02, y02, z02]

                       if d8 > 1:
                           nrofpoints = nrofpoints - 1
                           pointsimage[i, j] = pointsimage[i, j] - imavol[x02, y02, z01]

                       pointsimage[i, j] = pointsimage[i, j] / nrofpoints

   maskx = np.all(np.isnan(pointsimage) | np.equal(pointsimage, 0), axis=0)
   pointsimage = pointsimage[:, ~maskx]

   masky = np.all(np.isnan(pointsimage) | np.equal(pointsimage, 0), axis=1)
   pointsimage = pointsimage[~masky]
   return pointsimage

def rotimageleft(image):
    return np.rot90(image)

def rotimageright(image):
    return np.rot90(image,3)