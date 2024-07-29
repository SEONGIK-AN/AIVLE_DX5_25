import warnings
import threading
import streamlit as st
from annotated_text import annotated_text, annotation
from streamlit_folium import st_folium
from streamlit_extras.stylable_container import stylable_container
from streamlit.runtime.scriptrunner import add_script_run_ctx
from src import *

warnings.filterwarnings('ignore')
style = Style()
custom_time = CustomTime()
water_data = water_quality.Data() 
pred = predict.Predict()

ocean = ['한반도'] + list(water_data.data['생태구'].unique())
to_freq = {'D':'일간', 'W':'주간', 'M':'월간', 'Y':'연간'}
to_initial = {'일간':'D', '주간':'W', '월간':'M', '연간':'Y'}

st.logo(image='./src/img/banner.png', link='https://www.mof.go.kr/index.do')
header = stylable_container(key='header', css_styles=style.block)
body = st.columns([1.3, 1])

with header:
    head_cols = st.columns([style.margin*5, 1.4, 6, 5, style.margin*5])
    with head_cols[1]:
        st.container(height=5, border=False)
        space = st.empty()
        clock_thread = threading.Thread(target=custom_time.clock(space))
        add_script_run_ctx(clock_thread)
        clock_thread.start()

    with head_cols[2]:
        st.container(height=2, border=False)
        selected_subject = st.radio('표시 정보', ['현황', '분석·예측'], horizontal=True, label_visibility='collapsed')
        st.container(height=2, border=False)

if selected_subject=='현황':
    with head_cols[3]:
        st.container(height=2, border=False)
        date_resolution = st.select_slider(label='조회 간격', options=to_initial.keys(), label_visibility='collapsed')
        date_resolution = to_initial[date_resolution]
    st.container(height=2, border=False)
    with body[0]:
        left_body = stylable_container(key='left_body', css_styles=style.block)
        with left_body:
            st.container(height=10, border=False)
            _, padding, _ = st.columns([style.margin, 2, style.margin])
            _, water_quality_map, temperature_map, _ = st.columns([style.margin, 1, 1, style.margin])
            with padding:
                selected_ocean = st.selectbox(label='##### 생태구', options=ocean)

    df = post_processing.convert_date(water_data.data, date_resolution, water_data.date_col, '생태구', ['수질지수', '표층수온', '저층수온'])
    i = 0
    ind = dict()
    while len(ind) != len(df['생태구'].unique()):
        i += 1
        temp = df.iloc[-i, :]
        if temp['생태구'] not in ind.keys():
            ind[temp['생태구']] = len(df)-i
    lastest_df = df.iloc[list(ind.values()), :]
    if selected_ocean != '한반도':
        df = df[df['생태구']==selected_ocean]
    with left_body:
        with water_quality_map:
            st.write('##### 수질 분포')
            temp = water_quality.circle(
                df=lastest_df,
                center=style.map_center[selected_ocean],
                zoom_state=style.zoom_state[selected_ocean],
                circle_loc=style.circle_center,
                data_col='수질지수'
            )
            st_folium(
                temp,
                width=style.map_size[0],
                height=style.map_size[1]
            )

        with temperature_map:
            temp = water_quality.heatmap(
                df=lastest_df,
                center=style.map_center[selected_ocean],
                zoom_state=style.zoom_state[selected_ocean],
                heat_loc=style.circle_center,
                data_col='표층수온',
                categorical_col='생태구'
            )
            st.write('##### 표층수온 분포')
            st_folium(
                temp,
                width=style.map_size[0],
                height=style.map_size[1]
            )

    with body[1]:
        with stylable_container(key='right_body', css_styles=style.block):
            _, padding, _ = st.columns([style.margin, 2, style.margin])
            _, graph, table, _ = st.columns([style.margin, 1, 1.2, style.margin])

            with padding:
                st.container(height=10, border=False)
                selected_data_len = st.selectbox(label='##### 조회 구간', options=[3, 10, 50]) + 1
            df = df.iloc[-selected_data_len:-1, :].set_index(water_data.date_col)
            with table:
                with st.container(border=True):
                    st.write(f'##### {to_freq[date_resolution]} 수질 데이터')
                    st.dataframe(df[['생태구', '수질지수']], width=700, height=140)
                with st.container(border=True):
                    st.write(f'##### {to_freq[date_resolution]} 수온 데이터')
                    st.dataframe(df[['생태구', '표층수온', '저층수온']], width=700, height=140)
            with graph:
                with st.container(border=True):
                    st.write(f'##### {to_freq[date_resolution]} 수질 및 수온 분포')
                    st.line_chart(data=df.reset_index(), x='조사일자', y=['수질지수', '표층수온', '저층수온'], height=376)
            st.container(height=10, border=False)

        with st.container(border=True):
            head_cols = st.columns(5)
            for i, (_, row) in enumerate(lastest_df.iterrows()):
                with head_cols[i]:
                    st.write(f'##### {row["생태구"]}')
                    st.altair_chart(water_quality.donut_chart_quality(row, '수질지수', 90))
                    temp = row['표층수온']
                    st.metric(label='%s의 온도', value='%.2f ℃'%(temp), label_visibility='collapsed')
            st.container(height=5, border=False)

if selected_subject=='분석·예측':
    with body[0]:
        with stylable_container(key='fish_map', css_styles=style.block):
            _, padding, _ = st.columns([style.margin, 2, style.margin])
            with padding:
                st.container(height=3, border=False)
                st.write('##### 어종 분포 예측')
                selected_fish = st.selectbox(
                    label='조회 어종',
                    options=pred.models.keys(),
                    label_visibility='collapsed'
                )
                selected_date = st.select_slider(
                    label='조회 기간',
                    options=pred.data[pred.date_col].unique(),
                    format_func=lambda x: str(x)[:7],
                    label_visibility='collapsed'
                )
                df = pred.predict(selected_fish, selected_date)
                st_folium(
                    predict.heatmap(df=df,
                                    center=style.map_center['한반도'],
                                    zoom_state=style.zoom_state['한반도'],
                                    data_col='개체수'
                    ),
                    width=style.map_size[0]*3,
                    height=style.map_size[1]
                )
                
                st.container(height=3, border=False)
    
    with body[1]:
        df = pred.get_optimal_value(df, 3)
        importances_data = pred.feature_importances(selected_fish)
        trend_data = pred.get_trend(selected_fish)
        with stylable_container(key='right_body', css_styles=style.block):
            st.container(height=2, border=False)
            _, padding, _ = st.columns([style.margin, 2, style.margin])
            with padding:
                with st.container(border=True):
                    st.write(f'##### {selected_fish} 개체수 트렌드')
                    st.line_chart(data=trend_data, y_label='개체수 (톤)', height=200)
            _, col1, col2, _ = st.columns([style.margin, 1, 1,style.margin])

            with col1:
                with st.container(border=True):
                    st.write(f'##### {selected_fish} 개체수의 환경요인 중요도')
                    st.bar_chart(data=importances_data, y_label='중요도', height=465)

            with col2:
                with st.container(border=True):
                    st.write(f'##### ({str(selected_date)[:7]}) {selected_fish} 어업 최적지')
                    st.table(df)

                with st.container(border=True):
                    st.write('##### Heat Map 밀도 색상막대')
                    st.image('./src/img/fish_density.png')
            st.container(height=2, border=False)

annotated_text(annotation('본 페이지는 AIVLE 스쿨 빅프로젝트 간 제작된 가상 페이지 입니다.', font_size='30px'))