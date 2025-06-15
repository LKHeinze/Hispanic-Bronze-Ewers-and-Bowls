import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, shapiro, probplot, f_oneway, linregress
from src.utils import cast_data, read_data
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--region", type=str, default="all_regions")
    args = parser.parse_args()
    
    if args.region == "north":
        region = "Nordküste"
        figure_number = "1_45"
    elif args.region == "central":
        region = "Zentralspanien"
        figure_number = "1_47"
    elif args.region == "augusta":
        region = "Vía Augusta"
        figure_number = "1_46"
    elif args.region == "all_regions":
        figure_number = "1_17"



    df = read_data("data/ewers/dimensions_with_region.csv")
    df.set_index("Kat.-Nr.", inplace=True)
    df = cast_data(df)

    handle_height_vs_height_df = pd.DataFrame({
        "region":
        df["Region"],
        "height":
        df["Höhe: insgesamt"],        
    })


    height = handle_height_vs_height_df["height"].dropna(axis=0)

    height = height.loc[list(set(height.index.to_list()) - set([2, 10, 13, 18, 19, 25, 29]))]
    
    handle_height_vs_height_df = handle_height_vs_height_df.loc[list(set(handle_height_vs_height_df.index.to_list()) - set([2, 10, 13, 18, 19, 25, 29]))].dropna(axis=0)


    data = height if args.region == "all_regions" else  handle_height_vs_height_df[handle_height_vs_height_df.region==region]["height"]
    print(f"mean all objects: {np.mean(data)}")
    mean, std = norm.fit(data)
    x = np.linspace(mean-2*std, mean+2*std, 200)

    p = norm.pdf(x, mean, std) * len(data)

    fig, ax = plt.subplots(1,2, gridspec_kw={'width_ratios': [1, 3]}, sharey='row', figsize=(10,6))

    quantiles_norm, quantiles_data = probplot(data, dist="norm", fit=False)

    slope, intercept, r, _, _ = linregress(quantiles_norm, quantiles_data)
    
    result = slope * quantiles_norm + intercept

    crit = norm.ppf(1 - (1 - 0.95) / 2)
    pdf = norm.pdf(quantiles_norm, 0, 1)
    P = norm.cdf(quantiles_norm)
    se = (slope / pdf) * np.sqrt(P * (1 - P) / len(quantiles_norm))

    upper = result + crit * se
    lower = result - crit * se


    ax[1].scatter(quantiles_norm, quantiles_data, color = "lightskyblue")
    ax[1].plot(quantiles_norm, upper, linestyle="--", color="grey")
    ax[1].plot(quantiles_norm, lower, linestyle="--", color="grey")
    ax[1].plot(quantiles_norm, result, color = "black")
    ax[1].set_xlabel("Theoretische Quantile")
    ax[1].set_ylabel("Empirische Quantile")
    ax[1].set_ylim(bottom=np.min(data)-1, top=np.max(data)+1)
    ax[1].set_title("Normal Quantil Plot")


    ax[0].hist(data, bins=11, orientation="horizontal", edgecolor = 'black', color="lightskyblue", align="right", zorder=1)
    ax[0].set_xlabel("Anzahl")
    ax[0].set_ylabel("Höhe in cm")
    ax[0].plot(p,x, color="black")
    ax[0].set_title("Höhen-Histogram")

    fig.savefig(f'results/ewers/normal_distribution/{args.region}_fig_{figure_number}.png')
    plt.show()

    shapiro_wilk = shapiro(data)
    print(f"W: {shapiro_wilk.statistic}, p-value: {shapiro_wilk.pvalue}")




# ANOVA 
all_regions = [handle_height_vs_height_df[handle_height_vs_height_df.region=="Nordküste"]["height"],
               handle_height_vs_height_df[handle_height_vs_height_df.region=="Zentralspanien"]["height"],
               handle_height_vs_height_df[handle_height_vs_height_df.region=="Vía Augusta"]["height"]]

north_mean = np.mean(handle_height_vs_height_df[handle_height_vs_height_df.region=="Nordküste"]["height"])
central_mean = np.mean(handle_height_vs_height_df[handle_height_vs_height_df.region=="Zentralspanien"]["height"])
augusta_mean = np.mean(handle_height_vs_height_df[handle_height_vs_height_df.region=="Vía Augusta"]["height"])

print(f"mean all: {np.mean(pd.concat(all_regions))}")
print(f"mean north: {north_mean}")
print(f"mean central: {central_mean}")
print(f"mean augusta: {augusta_mean}")


medianprops = dict(linestyle=None, linewidth=0., color='firebrick')
meanlineprops = dict(linestyle='-', linewidth=2, color='lightskyblue')


fig = plt.figure()
fig.suptitle("Boxplots nach Region")
ax = fig.add_subplot(111)

ax.boxplot(all_regions,
           tick_labels= ["Nordküste", "Zentralspanien", "Vía Augusta"],
           showmeans= True,
           meanline=True,
           medianprops=medianprops,
           meanprops=meanlineprops)

ax.set_ylabel("Höhe in cm")

ax.hlines(y=np.mean(pd.concat(all_regions)), xmin=0.5, xmax=3.5, linewidth=1.5, color='grey', linestyle="--")
fig.savefig('results/ewers/normal_distribution/boxplot_fig_1_48.png')
plt.show()
print(f_oneway(handle_height_vs_height_df[handle_height_vs_height_df.region=="Nordküste"]["height"],
      handle_height_vs_height_df[handle_height_vs_height_df.region=="Zentralspanien"]["height"],
      handle_height_vs_height_df[handle_height_vs_height_df.region=="Vía Augusta"]["height"]))
