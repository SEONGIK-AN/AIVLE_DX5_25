import streamlit as st
import pandas as pd

class Style:
    def __init__(self) -> None:
        st.set_page_config(
            page_title="국내 연안 정보",
            page_icon="./src/img/icon.png",
            layout="wide",
        )
        self.block = """
        {
            background-color: #3d4b51;
            border-radius: 0.5rem;
        }
        """
        self.margin = .05
        self.map_size = (420, 650)
        self.map_center = {
            '한반도':(37.5, 128),
            '동해':(37.2, 131),
            '대한해협':(35, 130.5),
            '서남해역':(35, 125),
            '서해중부':(37, 125),
            '제주':(33, 126.5)
        }
        self.circle_center = {
            '동해':(37.2, 131),
            '대한해협':(35, 130.5),
            '서남해역':(35, 125),
            '서해중부':(37, 125),
            '제주':(33, 126.5)
        }
        self.zoom_state = {
            '한반도':6,
            '동해':7,
            '대한해협':7,
            '서남해역':7,
            '서해중부':7,
            '제주':7
        }
        self.alarm = """
            button {
                width:80px;
                height: 30px;
                color: #ff5959;
                border-radius: 5px;
                font-weight: 800;
            }
        """