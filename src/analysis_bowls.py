import matplotlib.pyplot as plt
import statsmodels.api as sm
from src.utils import read_data, cast_data
from argparse import ArgumentParser


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--feature", type=str, default="⌀: insgesamt (in cm)")
    parser.add_argument("--target", type=str, default="Gewicht: insgesamt (in g)")

    args = parser.parse_args()


    df = read_data("data/bowls/dimensions.csv")
    df = cast_data(df)
    df.set_index("Kat.-Nr.", inplace=True)
    df.dropna(axis=0, inplace=True)

    model = sm.OLS(df[args.target],
                   sm.add_constant(df[args.feature]))

    result = model.fit()
    pvalue = result.pvalues[args.feature]
    print(result.summary())

    prediction = result.predict(sm.add_constant(df[args.feature].sort_values()))


    plt.scatter(df[args.feature], df[args.target])
    plt.plot(df[args.feature].sort_values(), prediction, color="red")
    plt.xlabel(f"{args.feature}")
    plt.ylabel(f"{args.target}")
    plt.annotate(f"p-value: {round(pvalue,4)}", (df[args.feature].min(),df[args.target].max()))
    plt.savefig(f"results/bowls/linear_dependencies/{args.feature},{args.target}")
    plt.show()
