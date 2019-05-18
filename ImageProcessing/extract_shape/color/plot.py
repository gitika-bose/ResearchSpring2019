import matplotlib.pyplot as plt
file = open('blue.txt','r')
rgb = [eval(f) for f in file]
r = [color[0] for color in rgb]
g = [color[1] for color in rgb]
b = [color[2] for color in rgb]
plt.plot(r)
plt.waitforbuttonpress()
plt.plot(g)
plt.waitforbuttonpress()
plt.plot(b)
plt.waitforbuttonpress()
new_file = open('blue2.txt','w')

for i in rgb:
    red,green,blue = i[:]
    if green < 55 or blue < 85: continue
    new_file.write('({},{},{})\n'.format(red,green,blue))
# 55, 85