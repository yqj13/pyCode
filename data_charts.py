#coding=utf-8
import streamlit as st
import requests

from PIL import Image

from bs4 import BeautifulSoup
import jieba
from collections import Counter
from pyecharts.charts import WordCloud, Bar, Line, Pie, Scatter, Radar, TreeMap
import numpy as np
from pyecharts.globals import SymbolType
from pyecharts import options as opts
import streamlit_echarts

# Helper function to display pyecharts in Streamlit

# Streamlit app
st.title("URL 文章分析器")

# Input URL
url = st.text_input('请输入文章URL:', '')


# Helper function to display pyecharts in Streamlit using streamlit_echarts
def st_pyecharts(chart):
    streamlit_echarts.st_pyecharts(chart)

if url:
    # Fetch and parse the web page content
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()

    # Tokenize the text and calculate word frequency
    words = jieba.lcut(text)
    word_counts = Counter(words)

    # Remove low-frequency words based on user input
    min_frequency = st.sidebar.slider('过滤词频低于:', 1, 10, 1)
    filtered_word_counts = {word: count for word, count in word_counts.items() if count >= min_frequency}

    # Display top 20 words
    top_words = dict(word_counts.most_common(20))
    st.write("词频排名前20的词汇:")
    st.table(top_words)  # 使用表格格式展示

    # Add chart type selection in sidebar
    chart_type = st.sidebar.selectbox(
        "选择图表类型:",
        ["Word Cloud", "Bar Chart", "Line Chart", "Pie Chart", "Scatter Chart", "Radar Chart", "Tree Map"]
    )

    # Depending on the selected chart type, generate the appropriate chart
    if chart_type == "Word Cloud":
        word_cloud = WordCloud()
        word_cloud.add("", list(filtered_word_counts.items()), word_size_range=[20, 100], shape=SymbolType.DIAMOND)
        st_pyecharts(word_cloud)

    elif chart_type == "Bar Chart":
        bar = (
            Bar()
            .add_xaxis(list(top_words.keys()))
            .add_yaxis("词频", list(top_words.values()))
            .set_global_opts(title_opts=opts.TitleOpts(title="词频条形图"))
        )
        st_pyecharts(bar)

    elif chart_type == "Line Chart":
        line = (
            Line()
            .add_xaxis(list(top_words.keys()))
            .add_yaxis("词频", list(top_words.values()))
            .set_global_opts(title_opts=opts.TitleOpts(title="词频折线图"))
        )
        st_pyecharts(line)

    elif chart_type == "Pie Chart":
        pie = (
            Pie()
            .add("", [list(z) for z in zip(top_words.keys(), top_words.values())])
            .set_global_opts(title_opts=opts.TitleOpts(title="词频饼图"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
        )
        st_pyecharts(pie)

    elif chart_type == "Scatter Chart":
        scatter = (
            Scatter()
            .add_xaxis(list(range(len(top_words))))
            .add_yaxis("词频", list(top_words.values()), symbol_size=20)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="词频散点图"),
                xaxis_opts=opts.AxisOpts(name="词汇"),
                yaxis_opts=opts.AxisOpts(name="频率")
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        st_pyecharts(scatter)

    elif chart_type == "Radar Chart":
        max_freq = max(top_words.values())
        radar = (
            Radar()
            .add_schema(
                schema=[
                    opts.RadarIndicatorItem(name=key, max_=max_freq) for key in top_words.keys()
                ]
            )
            .add("词频", [[value for value in top_words.values()]])
            .set_global_opts(title_opts=opts.TitleOpts(title="词频雷达图"))
        )
        st_pyecharts(radar)

    elif chart_type == "Tree Map":
        treemap = (
            TreeMap()
            .add("词频", [dict(value=value, name=key) for key, value in top_words.items()])
            .set_global_opts(title_opts=opts.TitleOpts(title="词频树状图"))
        )
        st_pyecharts(treemap)