from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

Path('local').mkdir(exist_ok=True)


class Counter:
    def __init__(self):
        self.cnt_dict = {}

    def add(self, key, value=1):
        if key not in self.cnt_dict:
            self.cnt_dict[key] = 0
        self.cnt_dict[key] += value

    def __dict__(self):
        return self.cnt_dict


def get_clean_columns(columns):
    return [
        "".join(c if c.isalnum() else "_" for c in str(x)) for x in columns
    ]


def distplot(df, x, hue=None, title=None, base_dir="local/figs", prefix=""):
    if title is None:
        title = f"Dist Plot of {x}"
    plt.clf()
    plt.cla()
    if hue:
        for i in df[hue].unique():
            sns.distplot(df[df[hue] == i][x], hist_kws={"label": f"{hue}_{i}"})
        file_path = f"{prefix}{x}_{hue}_dict.png"
    else:
        sns.distplot(df[x])
        file_path = f"{prefix}{x}_dict.png"
    plt.legend()
    plt.title(title)
    plt.savefig(Path(base_dir).joinpath(file_path))


def countplot(df, x, hue=None, title=None, base_dir="local/figs", prefix=""):
    if title is None:
        title = f"Count Plot of {x}"
    plt.clf()
    plt.cla()
    sns.countplot(data=df, x=x, hue=hue)
    if hue:
        file_path = f"{prefix}{x}_{hue}_cnt.png"
    else:
        file_path = f"{prefix}{x}_cnt.png"
    plt.legend()
    plt.title(title)
    plt.savefig(Path(base_dir).joinpath(file_path))
