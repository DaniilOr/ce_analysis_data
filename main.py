import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import CountVectorizer


data = pd.read_csv('processed_data.csv')


def plot_unigrams(data):
  vectorizer = CountVectorizer()
  X = vectorizer.fit_transform(data['comment_text'])
  fig = px.bar(data_frame=pd.DataFrame(sorted(list(zip(X.toarray().sum(axis=1), vectorizer.get_feature_names_out())),
       key=lambda x: x[0]), columns=['count', 'word']),
       x='word',
       y='count')
  return fig


def page_1():
    option = st.selectbox(
        'What to visualize?',
        data['Name of media'].unique().tolist() + ['All'])
    if option == 'All':
        fig = px.bar(
            data_frame=data,
            x="Name of media",
            color="Sentiment",
            barmode="group",
            hover_data=['prepared_text'],
        )
    else:
        fig = px.bar(
            data_frame=data.loc[data['Name of media']==option],
            x="Name of media",
            color="Sentiment",
            barmode="group",
            hover_data=['prepared_text'],
        )
    st.plotly_chart(fig, use_container_width=True)


def page_2():
    option = st.selectbox(
        'Which sentiment to show?',
        data['Sentiment'].unique().tolist() + ['All'])
    if option == 'All':
        st.plotly_chart(plot_unigrams(data), use_container_width=True)
    else:
        st.plotly_chart(plot_unigrams(data.loc[data['Sentiment']==option]), use_container_width=True)


if __name__ == "__main__":
    selected_page = st.sidebar.selectbox("Select widget", ['Media', 'Unigrams'])
    if selected_page == "Media":
        page_1()
    else:
        page_2()
