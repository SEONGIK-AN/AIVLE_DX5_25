import pandas as pd
import altair as alt
import folium
from folium.plugins import HeatMap

def heatmap(df: pd.DataFrame, center: tuple, zoom_state: int, data_col: str) -> folium.Map:
    df = df[['위도', '경도', data_col]]
    heat_map = folium.Map(location=center, zoom_start=zoom_state)
    HeatMap(
        df.values.tolist(),
        gradient={.0: '#0066ff', .25: '#00b050', .5: '#ffff00', .75: '#ffc000', 1:'#ff0000'},
        min_opacity=.2,
        max_opacity=.8,
        radius=10,
        use_local_extrema=False,
    ).add_to(heat_map)
    return heat_map