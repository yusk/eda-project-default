import os
from pathlib import Path
import traceback
import subprocess

# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

Path('local').mkdir(exist_ok=True)

# https://ipafont.ipa.go.jp/node193#jp
rcParams['font.family'] = 'IPAexGothic'
sns.set(font=["IPAexGothic"])


def median(series):
    if series.dtype == "object":
        vc = series.value_counts()
        return vc.index[0]
    else:
        return series.median()


def eda(df, y_col, no_feature_cols=[], fig_dir="local/figs", max_kind_num=20):
    df2 = pd.DataFrame(columns=df.columns).T
    df2["null_cnt"] = df.isnull().sum()
    df2["cover_rate"] = 100 - (df.isnull().sum() / df.isnull().count() * 100)
    df2["type"] = [df[col].dtype for col in df.columns]

    types = []
    medians = []
    kinds = []
    for column in df.columns:
        print(column)
        series = df[column]
        dtype = series.dtype
        types.append(dtype)
        medians.append(median(series))
        kinds.append(series.nunique())
        if column != y_col and column not in no_feature_cols:
            try:
                if dtype == "object" or df[column].nunique() <= max_kind_num:
                    countplot(df,
                              column,
                              hue=y_col,
                              base_dir=fig_dir,
                              max_kind_num=max_kind_num)
                else:
                    distplot(df.dropna(subset=[column]),
                             column,
                             hue=y_col,
                             base_dir=fig_dir)
            except Exception:
                traceback.print_exc()
    df2["type"] = types
    df2["median"] = medians
    df2["kinds"] = kinds
    print(df2)
    subprocess.run([
        'convert',
        os.path.join(fig_dir, "*.png"),
        os.path.join(fig_dir, "eda.pdf")
    ])
    return df2


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
    Path(base_dir).mkdir(exist_ok=True)
    if title is None:
        title = f"Dist Plot of {x}"
    plt.clf()
    plt.cla()
    if hue:
        for i in df[hue].unique():
            sns.distplot(df[df[hue] == i][x], hist_kws={"label": f"{hue}_{i}"})
        file_path = f"{prefix}{x}_{hue}_dist.png"
        plt.legend()
    else:
        sns.distplot(df[x])
        file_path = f"{prefix}{x}_dist.png"
    plt.title(title)
    plt.tight_layout()
    plt.savefig(Path(base_dir).joinpath(file_path))


def countplot(df,
              y,
              hue=None,
              title=None,
              base_dir="local/figs",
              prefix="",
              max_kind_num=None):
    df = df.copy()
    Path(base_dir).mkdir(exist_ok=True)
    if title is None:
        title = f"Count Plot of {y}"
    plt.clf()
    plt.cla()
    vc = df[y].value_counts()
    if max_kind_num and len(vc) > max_kind_num:
        allowed_indexes = list(vc.index[:max_kind_num])
        df[y] = df[y].fillna("NaN")
        allowed_indexes.append("NaN")
        df[y][~df[y].isin(allowed_indexes)] = "その他"
        print(df[y].value_counts())
        allowed_indexes.append("その他")
    else:
        allowed_indexes = list(vc.index)
        if df[y].isnull().sum() > 0:
            df[y] = df[y].fillna("NaN")
            allowed_indexes.append("NaN")

    sns.countplot(data=df, y=y, hue=hue, order=allowed_indexes)
    if hue:
        file_path = f"{prefix}{y}_{hue}_cnt.png"
        plt.legend()
    else:
        file_path = f"{prefix}{y}_cnt.png"
    plt.title(title)
    plt.tight_layout()
    plt.savefig(Path(base_dir).joinpath(file_path))
