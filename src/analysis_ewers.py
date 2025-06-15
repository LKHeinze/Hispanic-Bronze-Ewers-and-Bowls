import matplotlib.pyplot as plt
import statsmodels.api as sm
from src.utils import read_data
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--feature", type=str, default="Fusshöhe")
    parser.add_argument("--target", type=str, default="Höhe insg.")
    args = parser.parse_args()


    df = read_data("data/ewers/dimensions.csv")
    df.set_index("Kat.-Nr.", inplace=True)

    if args.feature == "Fusshöhe" and args.target == "Höhe insg.":
        figure_number = "_fig_1_20"
    elif args.feature == "⌀ Bauch" and args.target == "⌀ Basis":
        figure_number = "_fig_1_21"
    else:
        figure_number = "_note_335"

    model = sm.OLS(df[args.target],
                   sm.add_constant(df[args.feature]))

    result = model.fit()
    pvalue = result.pvalues[args.feature]
    print(result.summary())

    prediction = result.predict(sm.add_constant(df[args.feature].sort_values()))


    plt.scatter(df[args.feature], df[args.target])
    plt.plot(df[args.feature].sort_values(), prediction, color="red")
    plt.xlabel(f"{args.feature} (in cm)")
    plt.ylabel(f"{args.target} (in cm)")
    plt.annotate(f"p-value: {round(pvalue,4)}", (df[args.feature].min(),df[args.target].max()))
    plt.savefig(f"results/ewers/linear_dependencies/{args.feature},{args.target}{figure_number}.png")
    plt.show()
