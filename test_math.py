import math

Mf = (-100 * 0.305 + 366 * 0.939 * 0.604) / (0.358 * 0.077)
print(Mf)

Rx = Mf * 0.934 + 366 * 0.342
print(Rx)
Ry = 100 + Mf * 0.358 - 366 * 0.939
print(Ry)

R = math.sqrt(pow(Rx, 2) + pow(Ry, 2))
print(R)

tga = Ry / Rx
print(tga)
a = math.atan(tga)
print(a)

Fy = Mf * 0.358
print(Fy)
Fx = Mf * 0.934
print(Fx)
