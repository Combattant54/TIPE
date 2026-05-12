import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

COLORS = ["red", "green", "b", "purple", "orange", "black"]
X, Y = [1, 1, 2, 2, 3, 3], [1, 2, 1, 2, 1, 2]

fig, axis = plt.subplots()
axis.set_xlim(-1, 10)
axis.set_ylim(-1, 10)

scat = plt.scatter(X, Y, s=20, c=COLORS[:len(X)])

plt.show()

V = [[1, 1]] * len(X)

DT = 0.1

def update(frames):
    for i in range(len(X)):
        X[i] += V[i][0] * DT
        Y[i] += V[i][1] * DT
    scat.set_offsets(list(zip(X, Y)))
    
    return scat, 

anim = FuncAnimation(fig=fig, func=update, frames=50, interval=DT*1000, repeat=False, blit=True)
anim.save("test.gif")
plt.show()