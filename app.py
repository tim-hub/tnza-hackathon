from flask import Flask
from flask import render_template

import pandas as pd
from textblob import TextBlob
import indicoio

app = Flask(__name__)


def init():
    pass




@app.route('/')
def index():
    indicoio.config.api_key = 'ca64f795a2d673f848ba9c88f6c88c86'

    # # Processing all videos we have

    # In[36]:

    shows = pd.read_csv("./DataSample.csv", index_col=0)
    # shows.set_index("id")

    # In[37]:

    # # Processing videos' data

    # In[38]:

    descriptions = list(shows['description'].values)

    # In[39]:

    def get_emotion_attributes(descriptions):
        return indicoio.sentiment(descriptions)

    # emotions = get_emotion_attributes(descriptions)
    # shows["Emotion"] = pd.Series(emotions).values

    # In[40]:

    def get_subjectivity_textbloc(descs):
        return list(map(lambda a: TextBlob(a).sentiment.subjectivity, descs))

    subjectivities = get_subjectivity_textbloc(descriptions)
    shows["Subjectivity"] = pd.Series(subjectivities).values

    # In[41]:

    # # Get recomandations through Genre and Emotion Attributes

    # In[42]:

    def get_video(title):
        the_show = shows[(shows.title == title)]
        return the_show

    # In[43]:

    def get_recommandations(title):
        the_show = get_video(title)
        the_genre1 = the_show.genre1.values[0]
        the_genre2 = the_show.genre2.values[0]
        print(title + " is " + the_genre1 + " and " + the_genre2)

        return shows.loc[(shows.genre1 == the_genre1) | (shows.genre2 == the_genre2)]

    # In[44]:

    get_recommandations("2 Broke Girls")

    # # Random functions based on user history

    # In[47]:

    #  user watching history
    # 2, 3, 5 in fact
    # user watched 2 comedy and 1 adventure
    history_watched = [1, 2, 4]

    # In[57]:

    list_watched = shows.iloc[history_watched]

    def get_genre_watched_most(watched):
        df_watched = shows.iloc[watched]
        #     the genre watched most by user
        the_genre = df_watched.genre1.mode().values[0]
        #     the all videos on website data set
        #     shuffle them
        the_shows = shows.loc[(shows.genre1 == the_genre) | (shows.genre2 == the_genre)].sample(frac=1)
        #     and pick top 3 as results
        return the_shows.head(1)

    sugggestions = get_genre_watched_most(history_watched)

    print(list_watched.values)


    return render_template('index.html', result={
        'name': 'TVNZ  Random Suggestion',
        'history': list_watched.values,
        'suggestions': sugggestions.to_json(),
    })




if __name__ == '__main__':
    app.run()
