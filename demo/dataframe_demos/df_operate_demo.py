import pandas as pd


def get_base_df():
    tuples = [
        ('cobra', 'mark i'), ('cobra', 'mark ii'),
        ('sidewinder', 'mark i'), ('sidewinder', 'mark ii'),
        ('viper', 'mark ii'), ('viper', 'mark iii')
    ]
    index = pd.MultiIndex.from_tuples(tuples)
    values = [[12, 2], [0, 4], [10, 20], [1, 4], [7, 1], [16, 36]]
    df = pd.DataFrame(values, columns=['max_speed', 'shield'], index=index)
    return df


def show_change_demo():
    df = get_base_df()
    # df.loc[:, 'shield'] = 'haha'
    # print(df)
    df.loc[:, 'shield'] = df.loc[:, 'shield'] * 100
    print(df)


if __name__ == "__main__":
    show_change_demo()
    pass
