from ...visualization.interfaces.ivisualizer import IVisualizer
import plotly.express as px
import pandas as pd
from flask import Markup
from typing import List, Dict, Any


class Visualizer(IVisualizer):
    def generate_plot(self, sensor_data: List[Dict[str, Any]]) -> str:
        if not sensor_data:
            return "<p>No data available.</p>"

        df = pd.DataFrame(sensor_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Assuming 'data' field contains a dict with sensor readings
        data_records = []
        for index, row in df.iterrows():
            for sensor_type, value in row['data'].items():
                data_records.append({
                    'timestamp': row['timestamp'],
                    'sensor_type': sensor_type,
                    'sensor_value': value
                })
        data_df = pd.DataFrame(data_records)
        fig = px.line(data_df, x='timestamp',
                      y='sensor_value', color='sensor_type')
        return Markup(fig.to_html(full_html=False))
