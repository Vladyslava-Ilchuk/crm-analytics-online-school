"""
myutils.py
Вспомогательные функции для финального проекта.
Подключается в каждом ноутбуке командой:
    import sys
    sys.path.append('../utils')
    from myutils import display_report, plot_categorical_dual, ...
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# Цветовая палитра проекта (единый стиль)
BLUE   = "#2563EB"
GREEN  = "#16A34A"
RED    = "#DC2626"
GREY   = "#6B7280"
YELLOW = "#F59E0B"

# Настройки графиков
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "white",
    "axes.grid":        True,
    "grid.alpha":       0.3,
    "axes.titlesize":   13,
    "axes.labelsize":   11,
})


# ── ФУНКЦИЯ 1: Сводная таблица по категориальным столбцам ──────────────────
def categorical_summary_df(df):
    """
    Возвращает таблицу с описанием всех категориальных столбцов:
    число уникальных значений, топ-значение, доля пропусков.
    """
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    rows = []
    for col in cat_cols:
        s = df[col]
        vc = s.value_counts(dropna=True)
        null_count = s.isna().sum()
        rows.append({
            "column":      col,
            "dtype":       str(s.dtype),
            "n_unique":    s.nunique(dropna=True),
            "top_value":   vc.index[0] if len(vc) > 0 else None,
            "top_freq":    int(vc.iloc[0]) if len(vc) > 0 else 0,
            "top_pct":     round(vc.iloc[0] / len(s) * 100, 2) if len(vc) > 0 else 0,
            "null_count":  null_count,
            "null_pct":    round(null_count / len(df) * 100, 2),
        })
    return pd.DataFrame(rows)


# ── ФУНКЦИЯ 2: Сводная таблица по числовым столбцам ────────────────────────
def numeric_summary_df(df):
    """
    Возвращает таблицу со статистиками числовых столбцов:
    среднее, медиана, мода, мин, макс, диапазон, пропуски.
    """
    num_cols = df.select_dtypes(include=[np.number]).columns
    rows = []
    for col in num_cols:
        s = df[col].dropna()
        null_count = df[col].isna().sum()
        mode_vals = s.mode()
        rows.append({
            "column":     col,
            "count":      len(s),
            "mean":       round(s.mean(), 2),
            "median":     round(s.median(), 2),
            "mode":       round(mode_vals.iloc[0], 2) if len(mode_vals) > 0 else None,
            "std":        round(s.std(), 2),
            "min":        s.min(),
            "max":        s.max(),
            "range":      s.max() - s.min(),
            "null_count": null_count,
            "null_pct":   round(null_count / len(df) * 100, 2),
        })
    return pd.DataFrame(rows)


# ── ФУНКЦИЯ 3: Полный отчёт о датасете ─────────────────────────────────────
def display_report(df, df_name="DataFrame"):
    """
    Печатает полный отчёт: размер, пропуски, категориальные и числовые итоги.
    """
    print("=" * 65)
    print(f"  ОТЧЁТ: {df_name}")
    print("=" * 65)
    print(f"  Размер : {df.shape[0]:,} строк × {df.shape[1]} столбцов")
    print(f"  Память : {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print()

    nulls = df.isna().sum()
    nulls = nulls[nulls > 0]
    if len(nulls) > 0:
        print("  Пропуски (NaN):")
        for col, cnt in nulls.items():
            print(f"    {col:<40} {cnt:>6} ({cnt/len(df)*100:.1f}%)")
    else:
        print("  Пропусков нет.")
    print()

    cat = categorical_summary_df(df)
    if not cat.empty:
        print("  КАТЕГОРИАЛЬНЫЕ столбцы:")
        print(cat.to_string(index=False))
        print()

    num = numeric_summary_df(df)
    if not num.empty:
        print("  ЧИСЛОВЫЕ столбцы:")
        print(num.to_string(index=False))
    print("=" * 65)


# ── ФУНКЦИЯ 4: Двойной бар-чарт для категориального поля ───────────────────
def plot_categorical_dual(series, col_name, top_n=10, df_name=""):
    """
    Строит два графика рядом:
      Левый  — количество по категориям
      Правый — доля (%) по категориям
    """
    vc = series.value_counts(dropna=False).head(top_n)
    labels = [str(x) for x in vc.index]
    counts = vc.values
    shares = counts / len(series) * 100

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    title = f"[{df_name}] " if df_name else ""

    # Левый: количество
    axes[0].barh(labels[::-1], counts[::-1], color=BLUE, edgecolor="white")
    axes[0].set_title(f"{title}{col_name} — Количество")
    axes[0].set_xlabel("Количество")
    for i, (bar, val) in enumerate(zip(axes[0].patches, counts[::-1])):
        axes[0].text(bar.get_width() + max(counts)*0.01,
                     bar.get_y() + bar.get_height()/2,
                     f"{val:,}", va="center", fontsize=9)

    # Правый: доля
    axes[1].barh(labels[::-1], shares[::-1], color=GREEN, edgecolor="white")
    axes[1].set_title(f"{title}{col_name} — Доля (%)")
    axes[1].set_xlabel("Доля (%)")
    for i, (bar, val) in enumerate(zip(axes[1].patches, shares[::-1])):
        axes[1].text(bar.get_width() + max(shares)*0.01,
                     bar.get_y() + bar.get_height()/2,
                     f"{val:.1f}%", va="center", fontsize=9)

    plt.tight_layout()
    plt.show()


# ── ФУНКЦИЯ 5: Отчёт по числовым полям (гистограмма + боксплот) ────────────
def plot_numeric_report(df, df_name="DataFrame", exclude_cols=None):
    """
    Для каждого числового столбца строит:
      Левый  — гистограмму с линиями среднего и медианы
      Правый — боксплот
    """
    exclude_cols = exclude_cols or []
    num_cols = [
        c for c in df.select_dtypes(include=[np.number]).columns
        if c not in exclude_cols
    ]
    for col in num_cols:
        s = df[col].dropna()
        fig, axes = plt.subplots(1, 2, figsize=(14, 4))

        # Гистограмма
        axes[0].hist(s, bins=40, color=BLUE, edgecolor="white", alpha=0.85)
        axes[0].axvline(s.mean(),   color=RED,   linestyle="--",
                        label=f"Среднее: {s.mean():,.1f}")
        axes[0].axvline(s.median(), color=GREEN, linestyle="-.",
                        label=f"Медиана: {s.median():,.1f}")
        axes[0].set_title(f"[{df_name}] {col} — Распределение")
        axes[0].set_xlabel(col)
        axes[0].set_ylabel("Количество")
        axes[0].legend(fontsize=9)

        # Боксплот
        axes[1].boxplot(s, vert=False, patch_artist=True,
                        boxprops=dict(facecolor=BLUE, alpha=0.5),
                        medianprops=dict(color=RED, linewidth=2))
        axes[1].set_title(f"[{df_name}] {col} — Боксплот")
        axes[1].set_xlabel(col)
        axes[1].set_yticks([])

        plt.tight_layout()
        plt.show()


# ── ФУНКЦИЯ 6: Расчёт конверсии по группе ──────────────────────────────────
def conversion_rate(df, group_col, success_col="is_paid", top_n=15):
    """
    Считает конверсию (%) по группирующему столбцу.
    Возвращает DataFrame с колонками: group_col, total, paid, conversion_pct.
    """
    grouped = (
        df.groupby(group_col, observed=True)[success_col]
        .agg(total="count", paid="sum")
        .reset_index()
    )
    grouped["conversion_pct"] = (
        grouped["paid"] / grouped["total"] * 100
    ).round(2)
    return grouped.sort_values("conversion_pct", ascending=False).head(top_n)