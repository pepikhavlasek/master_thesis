import pandas as pd
from pathlib import Path
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import scikit_posthocs as sp

path = "results.csv"
df = pd.read_csv(path)  

groups = ["HC", "RBD", "PN", "MSA"]

variables = {
    "subharm_num": "SUBHARM CARDINALITY",
    "subharm_sig_ratio": "SUBHARM-SIGNAL RATIO",
    "subharm_per_second" : "SUBHARMS PER SECOND",
    "density_num_slope" : "NUMBER-DENSITY SLOPE",
    "pct_subharm_num_2nd_half" : "NUMBER-PERCENTAGE IN 2ND HALF", 
    "density_dur_slope": "DURATION-DENSITY SLOPE", 
    "pct_subharm_dur_2nd_half": "DURATION-PERCENTAGE IN 2ND HALF",
    "first_occur": "FIRST SUBHARM OCCURRENCE",
    "avg_dur": "MEAN SUBHARM DURATION",
    "median_dur": "MEDIAN SUBHARM DURATION", 
    "std_dur": "STD SUBHARM DURATION", 
    "CV_dur": "CoV SUBHARM DURATION", 
    "longest_dur": "LONGEST SUBHARM DURATION",
    "mean_inter_intervals": "MEAN INTER-SUBHARM INTERVAL", 
    "median_inter_intervals": "MEDIAN INTER-SUBHARM INTERVAL",  
    "std_inter_intervals": "STD INTER-SUBHARM INTERVAL",  
    "COV_inter_intervals": "CoV INTER-SUBHARM INTERVAL", }

ylabels = ["Number of subharmonic components [-]", 
    "Subharmonic length:total signal length [-]",
    "First subharmonic occcurence [s]",
    "Mean subharmonic duration [s]"]

titles = ["Subharmonic cardinality",
    "Subharmonic-signal ratio",
    "First subharmonic occurence",
    "Mean subharmonic duration"]

"""
fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
axes = axes.ravel()

for i, (ax, var, ydata, title) in enumerate(zip(axes, variables.keys(), ylabels, titles)):
    sns.boxplot(data=df, x="group", y=var, order=groups, ax=ax)
    sns.stripplot(data=df, x="group", y=var, order=groups,
                  color="black", size=3, alpha=0.5, jitter=0.2, ax=ax)

    ax.set_title(title, fontweight="bold")
    ax.set_ylabel(ydata)

    if i < 2:
        ax.set_xlabel("")
        ax.set_xticklabels([])
    else:
        ax.set_xlabel("Group")

plt.savefig("boxplots_labels.png", dpi=300)
plt.show()
"""

df["cell"] = df["group"].astype(str) + "_" + df["sex"].astype(str)


# fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
# axes = axes.flatten()

# fig_rvf, axes_rvf = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
# axes_rvf = axes_rvf.flatten()

for i, (dv, label) in enumerate(variables.items()):
    print(f"---------------- {label} ----------------")
    print("---------------------------------------------------------------")

    df_clean = df.dropna(subset=[dv])

    # Kruskal-Wallis
    print("------------------------ KRUSKAL-WALLIS --------------------------")
    kw = pg.kruskal(data=df_clean, dv=dv, between="group")
    print(kw)
    H = kw["H"].values[0]
    k = len(groups)
    n = len(df_clean)
    eps_sq = (H-k+1)/(n-k)
    print(f"Effect epsilon squared: {eps_sq:.4f}")

    if float(kw["p-unc"].values[0]) <= 0.05:
        print("TIME FOR WHITNEY")
    
    # DUNN OR MANN-WHITNEY TEST !!!!!
    # POST-HOC TEST
    if aov_pg["p-unc"].values[0] <= 0.05:
        print("------------------------ POST-HOC TUKEY TEST ------------------------")
        tukey = pairwise_tukeyhsd(endog=df_clean[dv], groups=df_clean["group"], alpha=0.05)
        print(tukey)
        print()
    dunn = sp.posthoc_dunn(df_clean, val_col=dv, group_col="group", p_adjust="holm")

    # --- Normality diagnostics on residuals ---
    resid = model.resid

    # 1) Shapiro–Wilk test (on residuals)
    W, p = stats.shapiro(resid)
    print(f"\nShapiro–Wilk on residuals: W={W:.4f}, p={p:.4g}")

    # 2) Q–Q plot (on residuals)
    # sm.qqplot(resid, line="45", ax=axes[i], marker="x")
    # ref_line = axes[i].lines[1]
    # ref_line.set_linestyle("--")
    # axes[i].set_title(titles[i], fontweight="bold")
    # # axis labels: only bottom row gets x-labels, left column gets y-labels
    # if i < 2:        # top row
    #     axes[i].set_xlabel("")
    # # if i % 2 == 1:   # right column 
    # if i == 0: # first subplot
    #     axes[i].set_xlim(-3, 3)
    #     axes[i].set_ylabel("")
    # elif i == 2: # third subplot
    #     axes[i].set_xlim(-4, 4)
    #     axes[i].set_ylabel("")

    

    # --- Residuals vs Fitted plot ---
    # fitted = model.fittedvalues

    # axes_rvf[i].scatter(fitted, resid, alpha=0.6)
    # axes_rvf[i].axhline(0, linestyle="--", linewidth=1)
    # axes_rvf[i].set_title(titles[i], fontweight="bold")

    # # axis labels: only bottom row gets x-labels, left column gets y-labels
    # if i < 2:          # top row
    #     axes_rvf[i].set_xlabel("")
    # else:
    #     axes_rvf[i].set_xlabel("Fitted values")

    # if i % 2 == 1:     # right column
    #     axes_rvf[i].set_ylabel("")
    # else:
    #     axes_rvf[i].set_ylabel("Residuals")



    

# plt.tight_layout()
# plt.savefig("qqplots.png", dpi=300)
# plt.show()

# fig_rvf.savefig("residuals_vs_fitted.png", dpi=300)
