# import numpy as np
# import matplotlib.pyplot as plt

# ra = np.loadtxt("C:\\Users\\prosi\\Desktop\\Політех\\ТІС\\ЛАБ2\\lab2.RA.results.dat", delimiter=",")
# pa = np.loadtxt("C:\\Users\\prosi\\Desktop\\Політех\\ТІС\\ЛАБ2\\lab2.PA.results.dat", delimiter=",")
# la = np.loadtxt("C:\\Users\\prosi\\Desktop\\Політех\\ТІС\\ЛАБ2\\lab2.LA.results.dat", delimiter=",")

# t = np.arange(1, len(ra) + 1)

# plt.plot(t, ra[:, 0], label="RA - випадковий агент")
# plt.plot(t, la[:, 0], label="LA - автомат Робінса")
# plt.plot(t, pa[:, 0], label="PA - ідеальний агент")

# plt.xlabel("Крок взаємодії t")
# plt.ylabel("Середній сумарний виграш W1")
# plt.title("Залежність сумарного виграшу W1 від кількості кроків")

# plt.grid()
# plt.legend()
# plt.tight_layout()

# plt.savefig("lab2_graph.png", dpi=300)
# plt.show()



import numpy as np
import matplotlib.pyplot as plt

# Зчитування результатів
ra = np.loadtxt(
    r"C:\Users\prosi\Desktop\Політех\ТІС\ЛАБ3\lab3.RA.results.dat",
    delimiter=","
)

pa = np.loadtxt(
    r"C:\Users\prosi\Desktop\Політех\ТІС\ЛАБ3\lab3.PA.results.dat",
    delimiter=","
)

rl = np.loadtxt(
    r"C:\Users\prosi\Desktop\Політех\ТІС\ЛАБ3\lab3.RL.results.dat",
    delimiter=","
)

# Кроки експерименту
t = np.arange(1, len(ra) + 1)

# Перший стовпець - середній виграш
plt.plot(t, ra[:, 0], label="RA - випадковий агент")
plt.plot(t, rl[:, 0], label="RL - Softmax")
plt.plot(t, pa[:, 0], label="PA - ідеальний агент")

plt.xlabel("Крок взаємодії t")
plt.ylabel("Середній виграш")
plt.title("Залежність середнього виграшу від кількості кроків")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()