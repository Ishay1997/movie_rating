from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from sqlalchemy import desc

base_url = "https://api.themoviedb.org/3"
endpoint = "/search/movie"
api_key = "08e59cab0e956e5281488721d1f42d4d"
# api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwOGU1OWNhYjBlOTU2ZTUyODE0ODg3MjFkMWY0MmQ0ZCIsInN1YiI6IjY1Zjg1MWRkMThiNzUxMDE2NWY2YzI3OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vHErORiBK6dr_h552_wJOOiuNBpfnLp3kQrKdC54_CY"
'''
Red underlines? Install the required packages first:
Open the Terminal in PyCharm (bottom left).

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE TABLE

##CREATE DB
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)



# New Find Movie Form
class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

# New Find Movie Form
class FindMoviesFormByActor(FlaskForm):
    name = StringField("Actor Name", validators=[DataRequired()])
    submit = SubmitField("Search")

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=True)
    # unique=True
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # Query the movies from the database and sort them by rating
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_results = result.scalars().all()
    for movie in all_results:
        movie.ranking = None
    db.session.commit()

    # Assign unique rankings to movies
    for i, movie in enumerate(all_results):
        movie.ranking = len(all_results) - i

    # Commit the changes to the database
    db.session.commit()

    return render_template("index.html", movies=all_results)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    print(id)
    if request.method == "POST":
        movie_to_update = Movie.query.get_or_404(id)
        if request.form["rating"] != "":
            movie_to_update.rating = request.form["rating"]
        if request.form["review"] != "":
            movie_to_update.review = request.form["review"]
        db.session.commit()
        return redirect(url_for('home'))
    movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    print(movie_to_update.title)
    return render_template("edit.html", movie=movie_to_update)


@app.route("/find_movie")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_api_id}", params={"api_key": api_key, "language": "en-US"}).json()
        new_movie = Movie(
            id=data['id'],
            title=data['title'],
            year=data['release_date'].split('-')[0],  # Extracting the year from release date
            description=data['overview'],
            rating=data['popularity'],  # You might want to handle this differently
            ranking=None,  # You might want to handle this differently
            review="",  # You might want to handle this differently
            img_url=f"https://image.tmdb.org/t/p/w500/{data['poster_path']}" if data['poster_path'] else ""
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('edit', id=new_movie.id))


# New Add Route
@app.route("/add", methods=["GET", "POST"])
def add():
    form = FindMovieForm()

    if form.validate_on_submit():

        movie_title = form.title.data

        # Define the base URL and endpoint

        # Parameters for the search query
        params = {
            "api_key": api_key,
            "query": movie_title
        }

        # Make the GET request to search for movies
        response = requests.get(f"{base_url}{endpoint}", params=params)
        data = response.json()["results"]
        if data!=None:
            return render_template("select.html", movies=data)
    return render_template("add.html", form=form)


@app.route("/delete/<int:id>")
def delete(id):
    movie = db.get_or_404(Movie, id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/movies_by_actor", methods=["GET", "POST"])
def movies_by_actor():
    form = FindMoviesFormByActor()
    list = []
    if form.validate_on_submit():

        actor_name = form.name.data
        params = {
            "api_key": api_key,
            "query": actor_name,
            "language": "en-US"
        }

        # Make the GET request to search for movies
        response = requests.get(f"{base_url}{endpoint}", params=params)
        movies = response.json()["results"]
        for index, data in enumerate(reversed(movies), start=1):
            new_movie = Movie(
                id=data['id'],
                title=(data['title'].split('/')[1].strip() if '/' in data['title'] else
                             data['title'].split(':')[1].strip() if ':' in data['title'] else
                             data['title']),
                year=data['release_date'].split('-')[0],  # Extracting the year from release date
                description=data['overview'],
                rating=data['popularity'],  # You might want to handle this differently
                ranking=0,  # You might want to handle this differently
                review="",  # You might want to handle this differently
                img_url=f"https://image.tmdb.org/t/p/w500/{data['poster_path']}" if data['poster_path'] else ""
            )
            list.append(new_movie)
            list = sorted(list, key=lambda x: x.rating)
            for index, movie in enumerate(list, start=1):
                movie.ranking = len(list) - index + 1
        return render_template("index.html", movies=list)
    return render_template("get_actor_name.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
