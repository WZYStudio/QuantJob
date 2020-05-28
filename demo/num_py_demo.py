import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def show_demo1():
    my_matrix = np.eye(4)
    print(my_matrix)

    x = np.linspace(-2, 2, 100)
    y = np.cos(np.pi * x)

    plt.plot(x, y, 'go')
    plt.title(r"$y=\cos(\pi \times x)$")
    plt.show()


def show_demo2():
    my_array = np.random.randn(10)
    print(str(my_array))
    print('-------------')
    # 每一项，是本项与之前的累加和，看结果就明白了
    print(str(my_array.cumsum()))
    my_index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    my_index2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    plt.plot(my_index2, my_array, 'ko--')
    plt.show()


def show_demo3():
    # fig, axes = plt.subplots(2, 1)
    n_array = np.random.randn(16)
    data = pd.Series(n_array, index=list('abcdefghijklmnop'))
    # data.plot(kind='bar', ax=axes[0], color='k', alpha=0.7)
    data.plot(kind='bar', color='k', alpha=0.7)
    plt.show()


if __name__ == '__main__':
    # show_demo1()
    # show_demo2()
    show_demo3()
