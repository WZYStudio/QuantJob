import numpy as np
import matplotlib.pyplot as plt

my_matrix = np.eye(4)
print(my_matrix)

x = np.linspace(-2, 2, 100)
y = np.cos(np.pi * x)

plt.plot(x, y, 'go')
plt.title(r"$y=\cos(\pi \times x)$")
plt.show()
