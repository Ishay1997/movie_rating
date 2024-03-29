**Project Description:**
# Movie Rating and Review Website
**Overview:**

The Movie Rating and Review Website is a Flask-based web application that allows users to explore and rate movies. It integrates with the [The Movie Database (TMDb) API](https://developer.themoviedb.org/) to fetch movie data and provides a platform for users to add their reviews and ratings.



**Acknowledgements:**
- Thanks to the creators of Flask, SQLAlchemy, and Bootstrap for their excellent tools and documentation.
- Special thanks to [The Movie Database (TMDb) API](https://developer.themoviedb.org/) for providing movie data.


**photos with explanation:**
On the home page, all movies are sorted by ranking from the most recommended

![front card](photos/Front_Card.PNG)



When I point at the card, he shows me the information about this movie.

![back card](photos/Back_Card.PNG)



When I write a movie name, I want to add it to the movies on the website.

![api results](photos/Add.PNG)



When I write a movie name, I get all the movies with this name in (TMDb) API](https://developer.themoviedb.org/) and choose the one I want to add.

![api results](photos/Api_Results.PNG)


**Key Features:**
1. **Explore Movies:** Users can browse through a collection of movies fetched from the [TMDb API](https://developer.themoviedb.org/).

2. **View Details:** Each movie entry displays details such as title, description, release year, and associated image.

3. **Add reviews and ratings: ** Users can add their reviews and ratings for movies listed on the website.

4. **Sort by Rating:** Movies are sorted based on their ratings, allowing users to quickly identify highly rated movies.

5. **Search Movies by Actor:** Users can search for all the movies that an actor has appeared in by clicking the "Search Movies by Actor" button. This feature integrates with the TMDb API to fetch movies related to the actor.

 
**Technologies Used:**
- **Flask:** The web application is built using Flask, a lightweight Python web framework.
  
- **SQLAlchemy:** SQLAlchemy is used to interact with the SQLite database, storing information about movies, reviews, and ratings.

- **External API Integration:** The application connects to the [The Movie Database (TMDb) API](https://developer.themoviedb.org/) to fetch movie data, including titles, descriptions, release years, and images.

- **Bootstrap:** Bootstrap is utilized for frontend design and layout, ensuring a responsive and visually appealing user interface.


**Usage:**
1. **Browse Movies:** Users can navigate through the list of movies displayed on the website.
  
2. **Add Reviews:** Users can share their opinions by adding reviews and ratings for movies they have watched.

3. **Sort Movies:** Movies are sorted based on their ratings, making it convenient for users to discover top-rated movies.


**Installation:**
1. Clone the repository to your local machine.
  
2. Install the required dependencies using `pip install -r requirements.txt`.

3. Run the Flask application using `python app.py`.

4. Access the website through your web browser at the provided URL.


**Contributing:**
Contributions to the movie rating and review website project are welcome! Feel free to fork the repository, make improvements, and submit pull requests.


**License:**
This project is licensed under the MIT License. See the LICENSE file for more details.


**Contact:**
For questions or inquiries, please contact Ishay at ishaylevy8@gmail.com.
