"""
myutils.py
Helper functions for the final project.
Imported in each notebook with the command:
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

# Project color palette (consistent style)
BLUE   = "#2563EB"
GREEN  = "#16A34A"
RED    = "#DC2626"
GREY   = "#6B7280"
YELLOW = "#F59E0B"

# Plot settings
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "white",
    "axes.grid":        True,
    "grid.alpha":       0.3,
    "axes.titlesize":   13,
    "axes.labelsize":   11,
})


# ── FUNCTION 1: Summary table for categorical columns ──────────────────
def categorical_summary_df(df):
    """
    Returns a table describing all categorical columns:
    number of unique values, top value, missing value percentage.
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


# ── FUNCTION 2: Summary table for numerical columns ────────────────────────
def numeric_summary_df(df):
    """
    Returns a table with statistics for numerical columns:
    mean, median, mode, min, max, range, missing values.
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


# ── FUNCTION 3: Full dataset report ─────────────────────────────────────
def display_report(df, df_name="DataFrame"):
    """
    Prints a full report: size, missing values, categorical and numerical summaries.
    """
    print("=" * 65)
    print(f"  REPORT: {df_name}")
    print("=" * 65)
    print(f"  Size   : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"  Memory : {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print()

    nulls = df.isna().sum()
    nulls = nulls[nulls > 0]
    if len(nulls) > 0:
        print("  Missing values (NaN):")
        for col, cnt in nulls.items():
            print(f"    {col:<40} {cnt:>6} ({cnt/len(df)*100:.1f}%)")
    else:
        print("  No missing values.")
    print()

    cat = categorical_summary_df(df)
    if not cat.empty:
        print("  CATEGORICAL columns:")
        print(cat.to_string(index=False))
        print()

    num = numeric_summary_df(df)
    if not num.empty:
        print("  NUMERICAL columns:")
        print(num.to_string(index=False))
    print("=" * 65)


# ── FUNCTION 4: Dual bar chart for categorical field ───────────────────
def plot_categorical_dual(series, col_name, top_n=10, df_name=""):
    """
    Creates two charts side by side:
      Left  — count by categories
      Right — percentage share by categories
    """
    vc = series.value_counts(dropna=False).head(top_n)
    labels = [str(x) for x in vc.index]
    counts = vc.values
    shares = counts / len(series) * 100

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    title = f"[{df_name}] " if df_name else ""

    # Left: count
    axes[0].barh(labels[::-1], counts[::-1], color=BLUE, edgecolor="white")
    axes[0].set_title(f"{title}{col_name} — Count")
    axes[0].set_xlabel("Count")
    for i, (bar, val) in enumerate(zip(axes[0].patches, counts[::-1])):
        axes[0].text(bar.get_width() + max(counts)*0.01,
                     bar.get_y() + bar.get_height()/2,
                     f"{val:,}", va="center", fontsize=9)

    # Right: percentage share
    axes[1].barh(labels[::-1], shares[::-1], color=GREEN, edgecolor="white")
    axes[1].set_title(f"{title}{col_name} — Share (%)")
    axes[1].set_xlabel("Share (%)")
    for i, (bar, val) in enumerate(zip(axes[1].patches, shares[::-1])):
        axes[1].text(bar.get_width() + max(shares)*0.01,
                     bar.get_y() + bar.get_height()/2,
                     f"{val:.1f}%", va="center", fontsize=9)

    plt.tight_layout()
    plt.show()


# ── FUNCTION 5: Numerical fields report (histogram + boxplot) ────────────
def plot_numeric_report(df, df_name="DataFrame", exclude_cols=None):
    """
    For each numerical column creates:
      Left  — histogram with mean and median lines
      Right — boxplot
    """
    exclude_cols = exclude_cols or []
    num_cols = [
        c for c in df.select_dtypes(include=[np.number]).columns
        if c not in exclude_cols
    ]
    for col in num_cols:
        s = df[col].dropna()
        fig, axes = plt.subplots(1, 2, figsize=(14, 4))

        # Histogram
        axes[0].hist(s, bins=40, color=BLUE, edgecolor="white", alpha=0.85)
        axes[0].axvline(s.mean(),   color=RED,   linestyle="--",
                        label=f"Mean: {s.mean():,.1f}")
        axes[0].axvline(s.median(), color=GREEN, linestyle="-.",
                        label=f"Median: {s.median():,.1f}")
        axes[0].set_title(f"[{df_name}] {col} — Distribution")
        axes[0].set_xlabel(col)
        axes[0].set_ylabel("Count")
        axes[0].legend(fontsize=9)

        # Boxplot
        axes[1].boxplot(s, vert=False, patch_artist=True,
                        boxprops=dict(facecolor=BLUE, alpha=0.5),
                        medianprops=dict(color=RED, linewidth=2))
        axes[1].set_title(f"[{df_name}] {col} — Boxplot")
        axes[1].set_xlabel(col)
        axes[1].set_yticks([])

        plt.tight_layout()
        plt.show()


# ── FUNCTION 6: Conversion rate by group ──────────────────────────────────
def conversion_rate(df, group_col, success_col="is_paid", top_n=15):
    """
    Calculates conversion rate (%) by grouping column.
    Returns a DataFrame with columns: group_col, total, paid, conversion_pct.
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
