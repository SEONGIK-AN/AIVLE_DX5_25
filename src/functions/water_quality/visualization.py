import pandas as pd
import altair as alt
import folium
from folium.plugins import HeatMap

def circle(df: pd.DataFrame, center: tuple, zoom_state: int, circle_loc: dict, data_col: str) -> folium.Map:
    circle_map = folium.Map(location=center, zoom_start=zoom_state)
    colors = ['#0066ff', '#00b050', '#ffff00', '#ffc000', '#ff0000']
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=circle_loc[row['생태구']],
            stroke=False,
            radius=10,
            color=colors[int(row[data_col])-1],
            fill=True,
            fill_opacity=.6
        ).add_to(circle_map)
        folium.Marker(
                location=circle_loc[row['생태구']],
                tooltip=f"<i>{row['생태구']}</i>",
        ).add_to(circle_map)
    return circle_map

def donut_chart_quality(row: pd.Series, data_col: str, size: int) -> alt.Chart:
    cleanliness = 100 - ((row[data_col]-1)/4 * 100)
    if cleanliness>=100:
        colors = ['#4f96ff', '#005fea']
        grade = 'I(1등급)'
    elif cleanliness>=75:
        colors = ['#25ff88', '#00cc5c']
        grade = 'II(2등급)'
    elif cleanliness>=50:
        colors = ['#ffff8b', '#d7d200']
        grade = 'III(3등급)'
    elif cleanliness>=25:
        colors = ['#ffe07d', '#eeb500']
        grade = 'IV(4등급)'
    else:
        colors = ['#ff8b8b', '#da0000']
        grade = 'V(5등급)'
    
    percent_info = pd.DataFrame({
        'Data':['청결도', '오염도'],
        "Value(%)":[cleanliness, 100-cleanliness]
    })
    
    percent_background = pd.DataFrame({
        'Data':['청결도', '오염도'],
        "Value(%)":[100, 0]
    })
    
    plot = alt.Chart(percent_info).mark_arc(innerRadius=30, cornerRadius=15).encode(
        theta="Value(%)",
        color= alt.Color(
            'Data:N',
            scale=alt.Scale(range=colors),
            legend=None
        )
    ).properties(width=size, height=size)
    
    background = alt.Chart(percent_background).mark_arc(innerRadius=30, cornerRadius=15).encode(
        color = alt.Color(
            'Data:N',
            scale=alt.Scale(range=colors),
            legend=None
        )
    )
    text = alt.Chart(percent_info).mark_text(
        align='center',
        color=colors[1],
        font='Noto Sans KR',
        fontSize=12,
        fontWeight=800).encode(
            text=alt.value(f'{grade}'
        )
    )
    return background + plot + text

def heatmap(df: pd.DataFrame, center: tuple, zoom_state: int, heat_loc: dict, data_col: str, categorical_col: str) -> folium.Map:
    data = []    
    for _, row in df.iterrows():
        temp = (row[data_col]-5)/20
        temp = 1 if temp > 1 else temp
        data.append([*heat_loc[row[categorical_col]], temp])
    
    heat_map = folium.Map(location=center, zoom_start=zoom_state)
    HeatMap(
        data,
        gradient={.0: '#0066ff', .25: '#00b050', .5: '#ffff00', .75: '#ffc000', 1:'#ff0000'},
        min_opacity=.6,
        max_opacity=.8,
        radius=20,
        use_local_extrema=False,
    ).add_to(heat_map)
    
    return heat_map