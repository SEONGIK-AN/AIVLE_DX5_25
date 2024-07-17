import streamlit as st
import time
from datetime import datetime

class CustomTime:
    def __init__(self) -> None:
        return
    
    def get_time(self) -> datetime:
        return datetime.now()
    
    def clock(self, watch: st.empty) -> object:
            def update_clock():
                while True:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
                    watch.markdown(
                        '''
                        <style>
                            .time {
                                @import url("https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100..900&display=swap");
                                font-size: 20px;
                                font-weight: 800;
                                font-family: "Noto Sans KR";
                            }
                        </style>
                        <p class="time">
                            %s
                        </p>
                        '''%(current_time), unsafe_allow_html=True)
                    time.sleep(1)
            return update_clock