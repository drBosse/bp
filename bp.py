import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


def key_string(time):
    result = "empty"

    if time == "m":
        result = "Morning"
    if time == "e":
        result = "Evening"

    return result

def sorted_data(df_data):
    df_sorted = df_data.groupby(["date", "time"], as_index=False)[["upper", "lower", "pulse"]].mean()
    df_std = df_data.groupby(["date", "time"], as_index=False)[["upper", "lower", "pulse"]].std()

    df_std["upper"] = df_std["upper"].fillna(0)
    df_std["lower"] = df_std["lower"].fillna(0)
    df_std["pulse"] = df_std["pulse"].fillna(0)

    print(df_std)

    return df_sorted


def bpdist_figure(df_data, time):
    figure = px.histogram(
        df_data.loc[df_data["time"] == time],
        x=["upper", "lower"],
        marginal="box",
        nbins=20,
        template="simple_white",
    )
    figure.update_layout(
        legend=dict(
            title=key_string(time),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        )
    )
    return figure


def bpvp_figure(df_data, time):
    figure = px.scatter(
        df_data.loc[df_data["time"] == time],
        x="pulse",
        y=["upper", "lower"],
        marginal_x="box",
        marginal_y="box",
        trendline="ols",
        template="simple_white",
    )
    figure.update_layout(
        legend=dict(
            title=key_string(time),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        )
    )
    return figure


def bp_figure(df_data, time):
    figure = px.scatter(
        df_data.loc[df_data["time"] == time],
        x="date",
        y=["upper", "lower", "pulse"],
        marginal_y="box",
        trendline="ols",
    )
    figure.update_layout(
        legend=dict(
            title=key_string(time),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        )
    )
    if time == "m":
        figure.add_hline(y=130,line_color="blue",line_dash="dash",
              annotation_text="VC 06-10 Upper",
              annotation_position="bottom right")
        figure.add_hline(y=80,line_color="orange",line_dash="dash",
              annotation_text="VC 06-10 Lower",
              annotation_position="bottom right")
        figure.add_hline(y=72,line_color="green",line_dash="dash",
              annotation_text="VC 06-10 Pulse",
              annotation_position="bottom right")

    figure.add_hrect(y0=140, y1=160, line_width=0, fillcolor="red", opacity=0.2)
    figure.add_hrect(y0=60, y1=90, line_width=0, fillcolor="green", opacity=0.2)
    return figure


def main():
    df = pd.read_csv("bp.csv")
    df["date"] = pd.to_datetime(df["date"])
    print(df.to_string())
    print(sorted_data(df))
    fig_m = bp_figure(sorted_data(df), "m")
    fig_m.write_image("images/bp-m.png")
    fig_e = bp_figure(sorted_data(df), "e")
    fig_e.write_image("images/bp-e.png")
    fig_bpvp_m = bpvp_figure(sorted_data(df), "m")
    fig_bpvp_m.write_image("images/bpvp-m.png")
    fig_bpvp_e = bpvp_figure(sorted_data(df), "e")
    fig_bpvp_e.write_image("images/bpvp-e.png")
    fig_bpdist_m = bpdist_figure(sorted_data(df), "m")
    fig_bpdist_m.write_image("images/bpdist-m.png")
    fig_bpdist_e = bpdist_figure(sorted_data(df), "e")
    fig_bpdist_e.write_image("images/bpdist-e.png")


if __name__ == "__main__":
    main()
