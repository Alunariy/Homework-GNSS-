import cv2
import numpy as np
import pandas as pd
from PIL import Image
import math
from matplotlib import pyplot as plt
from datetime import datetime
from scipy.optimize import fsolve
import sympy as sym


points = [(-50, 100), (300, 500), (-200, -700), (200, -600), (50, 1000)]
radius = [149.4139, 330.6324, 917.4691, 775.1122, 771.5541]
colors = ['purple', 'green', 'pink','cyan', 'yellow', 'magenta']
satelites = 5


def data():
  points = []
  radius = []
  print("Укажите кол-во спутников:")
  satelites = int(input())
  for i in range(satelites):
    print("Укажите координаты x, y спутника №", i+1)
    x, y = map(float, input().split(', '))
    points.append([x, y])
    print("Укажите расстояние до спутника №", i+1)
    rad = float(input())
    radius.append(rad)
  return points, radius, satelites
points, radius,satelites = data()


from sympy import *


#формула окружности, возвращает уравнение окружности
def equations(x1,y1,r1):
  x = sym.Symbol('x')
  y = sym.Symbol('y')
  return ((x1-x)**2+(y1-y)**2-r1**2)
#расстояние между центрами окружностей
def distance(x1,y1,x2, y2):
  return (math.sqrt((x1-x2)**2+(y1-y2)**2))


#пересечения 2х окружностей, возвращает массив кооринат точек пересечения
def roots(eq1,eq2):
  x, y = symbols('x, y')
  roots = solve([Eq(eq1,0), Eq(eq2,0)], [x, y])
  return roots


#Нахождение точек пересечения всех окружностей(сочетания)
ansv = []
for i in range(satelites-1):  
  for j in range(i + 1, satelites):
    d = distance(points[i][0],points[i][1],points[j][0],points[j][1])
    if d > (radius[j] + radius[i]) or d < (abs(radius[j] - radius[i])):
        print("Two circles have no intersection")
    elif d == 0:
        print("Two circles have same center!")
    else:
      eq1 = equations(points[i][0],points[i][1],radius[i])
      eq2 = equations(points[j][0],points[j][1],radius[j])
      rts = roots(eq1,eq2)
      for k in range(len(rts)):
        ansv.append(rts[k])
print(ansv)


#Предположение 
x =y = 0
for i in range(len(ansv)):
  x += ansv[i][0]
  y += ansv[i][1]
y = float(y/(len(ansv)))
x = float(x/(len(ansv)))
print(x, y)


#Функции отрисовки точек и окружностей
def DrawPoints(x,y, r,color = "blue"):
  circle=plt.Circle((x, y), r, color = color)
  plt.gca().add_artist(circle)
  
def DrawCircle(coord, R, disp = 5, color = "black", alpha=1, fill = False):
  circle=plt.Circle (coord, R, color = color, fill = fill, alpha=alpha)
  plt.gca().add_artist(circle)
#Отрисовка
plt.axis([-1500, 1000, -1500, 650])
plt.axis ("equal")
for i in range(len(ansv)):
  DrawPoints(ansv[i][0], ansv[i][1], 20)
DrawPoints(x, y,20, color = 'red')
print(x, y)


for i in range(satelites):
  DrawCircle(points[i], radius[i], color = colors[i])


#Поиск истинной позиции
length = []
m = []
dx = dy = 0
x0 = x
y0 = y
for i in range(100):
  x0 = x0 + dx
  y0 = y0 + dy
  length = []
  m = []
  for i in range(1,satelites):
    r = math.sqrt((points[i][0]-x0)**2 + (points[i][1]-y0)**2)
    length.append([radius[i]-r])
    m.append([(x0-points[i][0])/r,(y0-points[i][1])/r,1])
  length = np.array(length)
  m = np.array(m)
  n = [[dx], [dy], [tay]] = np.matmul(np.linalg.pinv(m),length)


x0 = x0 + dx
y0 = y0 + dy
print(dx, dy, tay)


#Ответ
plt.axis([-700, 700, -700, 700])
plt.axis ("equal")


for i in range(len(ansv)):
  DrawPoints(ansv[i][0], ansv[i][1], 20)


DrawPoints(x0, y0, abs(tay), color = 'red')
print(x0, y0, tay)


for i in range(1, satelites):
  DrawCircle(points[i], radius[i], color = colors[i])



