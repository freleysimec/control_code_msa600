
import pandas as pd
import plotly.express as px
# from plotly import graph_objs as go



def main():
    df = pd.read_excel('canopus_performed_measurements.xlsx')
    fig = px.scatter(df, x='die index', y='structure index')
    fig.update_layout(
    title="My Scatter Plot",
    title_x=0.5,
    font=dict(size=18),
    subtitle="This is a subtitle",
    subtitle_x=0.5,
)
    fig.write_html("plotlyFile.html")


if __name__=='__main__':
    main()
    #exit()