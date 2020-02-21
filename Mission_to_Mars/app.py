
from flask import Flask, render_template
from scrape_mars import scrape
import pandas as pd

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
x = {}
x = scrape(x)
# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
#print(x)
#print(type(x))
# Connect to a database. Will create one if not already available.
db = client.mars

# Drops collection if available to remove duplicates
db.mars.drop()

# Creates a collection in the database and inserts two documents
db.mars.insert(x)

news_ls = []
cat_ls = []

#Work between db and flask
teams = list(db.mars.find())


teams = list(db.mars.find())
df = pd.DataFrame(data=teams)
for i in teams:
    for j in i:
        news_ls.append(j)

#print(teams)
#print(teams)
#print(i)
#print(j)
#print('news_ls')
#print(news_ls)
for cat in news_ls:
    #print(i[cat])
    cat_ls.append(i[cat])
#for art in teams.news
df_html = df.to_html()

#print(df_html)
print('teams')
print(teams)
print('df')
print(df)
print(df_html)
# Set route
@app.route('/')



def index():
    # Store the entire team collection in a list
    teams = list(db.mars.find())
    df = pd.DataFrame(teams)

    # Return the template with the teams list passed in
    #return render_template('index.html', df=df, teams=df_html, len = 0)
    return render_template('index.html',  tables=[df.to_html(classes='data')], titles='df.columns.values')

if __name__ == "__main__":
    app.run(debug=True)
