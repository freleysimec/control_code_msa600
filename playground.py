
import altair as alt
import datapane as dp
from vega_datasets import data


def main():
    df = data.iris()

    fig = (
        alt.Chart(df)
        .mark_point()
        .encode(x="petalLength:Q", y="petalWidth:Q", color="species:N")
    )


    v = dp.Blocks("# My report", dp.Plot(fig), dp.DataTable(df))

    dp.save_report(v, path="my_report.html")

if __name__=='__main__':
    main()
    #exit()