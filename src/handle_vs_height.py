import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from src.utils import cast_data, read_data


if __name__ == "__main__":
    df = read_data("data/ewers/dimensions_with_region.csv")
    df.set_index("Kat.-Nr.", inplace=True)
    df = cast_data(df)

    handle_height_vs_height_df = pd.DataFrame({
        "handle_height":
        df["Griff: Länge"],
        "height":
        df["Höhe: insgesamt"]
    })


    handle_height_to_predict_height =pd.concat([handle_height_vs_height_df.loc[56], handle_height_vs_height_df.loc[59]], axis=1).transpose()
    handle_height_to_predict_height.index.name= "Kat.-Nr." 

    handle_height_vs_height_df.dropna(axis=0, inplace=True)

    model = sm.OLS(handle_height_vs_height_df["height"],
                   sm.add_constant(handle_height_vs_height_df["handle_height"]))

    result = model.fit()


    print(result.summary())

    test_predicted = result.predict(sm.add_constant(handle_height_to_predict_height["handle_height"].sort_values()))
    x  = pd.concat([handle_height_vs_height_df["handle_height"].sort_values(), handle_height_to_predict_height["handle_height"].sort_values()], axis=0)
    x_min = x.min() - 0.5
    x_max = x.max() + 0.75
    x = x.to_list() + [x_min] + [x_max]

    x.sort()

    alpha = 0.1
    y_pred = result.get_prediction(sm.add_constant(x)).summary_frame(alpha=alpha)
    print("\n prediction confidence interval: " + str(1-alpha) + "\n")
    print(result.get_prediction(sm.add_constant(handle_height_to_predict_height["handle_height"].sort_values())).summary_frame(alpha=alpha))

    plt.figure(figsize=(15,8))
    plt.fill_between(x, y_pred["obs_ci_lower"], y_pred["obs_ci_upper"], alpha=0.15, zorder=1, color="orange")
    plt.plot(x, y_pred["mean"], c="orange", zorder=1, label="Schätzung")

    plt.scatter(handle_height_vs_height_df["handle_height"], handle_height_vs_height_df["height"], color="gold", zorder=2, label="Vollständige Objektmaße verfügbar")
    texture_df = pd.concat([handle_height_vs_height_df["handle_height"],  handle_height_vs_height_df["height"]], axis=1)
    for index,row  in texture_df.iterrows():
        text=str(index)
        if text == "4":
            plt.annotate(str(index), (row["handle_height"]-0.05,  row["height"]+ 0.25))
        elif text =="27":
            plt.annotate(str(index), (row["handle_height"]+0.01,  row["height"]-1.1))  
        elif text =="28":
            plt.annotate(str(index), (row["handle_height"]+0.01,  row["height"]-1.1))  
        else:
            plt.annotate(str(index), (row["handle_height"]+0.1,  row["height"]-0.05))


    plt.scatter(handle_height_to_predict_height["handle_height"], test_predicted, zorder=2, label="Nur Grifflänge verfügbar")
    test_predicted.rename("height", inplace=True)

    texture__target_df = pd.concat([handle_height_to_predict_height["handle_height"], test_predicted], axis=1)
    for index,row  in texture__target_df.iterrows():
        text=str(index)
        plt.annotate(str(index), (row["handle_height"]+0.01,  row["height"]+0.45))


    plt.xlabel("Grifflänge (in cm)")
    plt.ylabel("Kannenhöhe (in cm)")
    plt.legend(loc="upper left")
    plt.margins(x=0)
    plt.savefig("results/ewers/estimate_missing_values/handle_vs_height_fig_1_30.png")
    plt.show()
