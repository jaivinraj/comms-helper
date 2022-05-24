import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import STOPWORDS


def ser_to_wordcloud(ser,random_state=None):
    text = " ".join(i for i in ser)
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(
        width=3000,
        height=2000,
        random_state=random_state,
        stopwords=stopwords,
        background_color="white",
    ).generate(text)
    return wordcloud

def wordcloud_to_fig(wordcloud,title=None):
    fig, ax = plt.subplots(figsize=(16,9))
    ax.imshow(wordcloud)

    ax.axis("off")
    if title:
        fig.suptitle(title, fontsize=40, fontweight="bold")
    return fig,ax

def ser_to_fig_wordcloud(ser,title=None,*args,**kwargs):
    wordcloud = ser_to_wordcloud(ser,*args,**kwargs)
    return wordcloud_to_fig(wordcloud,title=title)