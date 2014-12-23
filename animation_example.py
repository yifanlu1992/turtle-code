import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

fig = plt.figure()
ax = fig.add_subplot(111)
x = np.arange(0, 1.5, 0.01)
line, = ax.plot([], [], 'r-')
def animate(n):
    y = np.power(x, n+1)
    line.set_data(x, y)
    plt.title('y=x**{0}'.format(n+1))
anim = animation.FuncAnimation(fig, animate, frames=6, interval=10)
ax.axis([0, 1, 0, 1])
plt.show()
