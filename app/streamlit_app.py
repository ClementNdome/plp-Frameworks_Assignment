import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers (metadata.csv)")

@st.cache_data
def load_data():
    df = pd.read_csv('data/metadata.csv', low_memory=False)
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    return df.dropna(subset=['year','title'])

df = load_data()

# --- Sidebar filters ---
min_year, max_year = int(df['year'].min()), int(df['year'].max())
year_range = st.slider("Select year range", min_year, max_year, (2020, 2021))
filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.subheader("Sample of Filtered Data")
st.dataframe(filtered[['title','journal','year']].head(10))

# --- Visualization 1: Publications by Year ---
st.subheader("Publications by Year")
fig, ax = plt.subplots()
year_counts = filtered['year'].value_counts().sort_index()
sns.barplot(x=year_counts.index, y=year_counts.values, color='skyblue', ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)
# st.plt.savefig('Most Frequent Words111.jpg')

# --- Visualization 2: Top Journals ---
st.subheader("Top Journals")
fig, ax = plt.subplots()
top_journals = filtered['journal'].value_counts().head(10)
sns.barplot(y=top_journals.index, x=top_journals.values, color='orange', ax=ax)
ax.set_xlabel("Number of Papers")
ax.set_ylabel("Journal")
st.pyplot(fig)

# --- Visualization 3: Word Cloud ---
st.subheader("Word Cloud of Paper Titles")
text = ' '.join(filtered['title'].dropna())
wc = WordCloud(width=800, height=400, background_color='white').generate(text)
fig, ax = plt.subplots(figsize=(10,5))
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)
