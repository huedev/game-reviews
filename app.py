from datetime import datetime
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, igdb_authenticate, igdb_query

app = Flask(__name__)
app.config.from_prefixed_env()
CLIENT_ID = app.config["CLIENT_ID"]
CLIENT_SECRET = app.config["CLIENT_SECRET"]
ACCESS_TOKEN = igdb_authenticate(CLIENT_ID, CLIENT_SECRET)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///game-reviews.db")


# Referred to Flask documentation (https://flask.palletsprojects.com/en/3.0.x/templating/#registering-filters) for registering template filters
@app.template_filter('datetime_format')
def datetime_format(value, format="%b %d, %Y"):
    date = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return date.strftime(format)


@app.route('/')
@login_required
def index():
    recent_reviews = db.execute(
        "SELECT reviews.*, users.username FROM reviews JOIN users ON reviews.user_id = users.id ORDER BY timestamp DESC;",
    )

    games_list = []
    for review in recent_reviews:
        games_list.append(review['game_id'])
    games_list_str = ','.join([str(game_id) for game_id in games_list])

    games = igdb_query(CLIENT_ID, ACCESS_TOKEN, 'games', f'fields name, cover.image_id; where id = ({games_list_str});')
    
    return render_template('index.html', games=games, recent_reviews=recent_reviews)


@app.route('/search/', methods=["GET", "POST"])
@login_required
def search_redirect():
    """Redirect to search results"""
    if request.method == "POST":
        search = request.form.get("search")
        return redirect(f"/search/{search}")
    else:
        return redirect("/")


@app.route('/search/<search>', methods=["GET", "POST"])
@login_required
def search(search):
    """Display search results"""
    games = igdb_query(CLIENT_ID, ACCESS_TOKEN, 'games', f'search "{search}"; fields name, cover.image_id; where category = 0; limit 18;')
    return render_template('search.html', search=search, games=games)


@app.route('/games/<game_id>', methods=["GET", "POST"])
@login_required
def game_details(game_id):
    """View detailed information about a specific game"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        error = False
        # Ensure game_id was submitted
        if not request.form.get("game_id"):
            flash("Game ID required", "error")
            error = True
        
        # Ensure review was submitted
        elif not request.form.get("review"):
            flash("Review content required", "error")
            error = True
        
        # Submit review
        if not error:
            db.execute(
                "INSERT INTO reviews (user_id, game_id, rating, review) values(?, ?, ?, ?);",
                session["user_id"],
                request.form.get("game_id"),
                request.form.get("rating"),
                request.form.get("review"),
            )
            flash("Review published successfully", "success")

    game = igdb_query(CLIENT_ID, ACCESS_TOKEN, 'games', f'fields *, cover.image_id, platforms.name, genres.name; where id = {game_id}; limit 1;')
    if game:
        game = game[0]
    else:
        return redirect("/")

    aggregate_review_data = db.execute(
        "SELECT AVG(rating) as average_rating, COUNT(*) as review_count FROM reviews WHERE game_id = ?;",
        game_id,
    )[0]
    recent_reviews = db.execute(
        "SELECT reviews.*, users.username FROM reviews JOIN users ON reviews.user_id = users.id WHERE game_id = ? ORDER BY timestamp DESC LIMIT 5;",
        game_id,
    )
    return render_template('game.html', game=game, aggregate_review_data=aggregate_review_data, recent_reviews=recent_reviews)


@app.route('/reviews/<game_id>')
@login_required
def game_reviews(game_id):
    """View user reviews for a specific game"""
    game = igdb_query(CLIENT_ID, ACCESS_TOKEN, 'games', f'fields *, cover.image_id, platforms.name, genres.name; where id = {game_id}; limit 1;')
    if game:
        game = game[0]
    else:
        return redirect("/")
    
    reviews = db.execute(
        "SELECT reviews.*, users.username FROM reviews JOIN users ON reviews.user_id = users.id WHERE game_id = ? ORDER BY timestamp DESC;",
        game_id,
    )
    return render_template('game_reviews.html', game=game, reviews=reviews)


@app.route('/users/<username>')
@login_required
def user_profile(username):
    """View reviews from a specific user"""
    user = db.execute(
        "SELECT * FROM users WHERE username = ?;",
        username,
    )
    if user:
        user = user[0]
    else:
        return redirect("/")

    reviews = db.execute(
        "SELECT reviews.*, users.username FROM reviews JOIN users ON reviews.user_id = users.id WHERE user_id = ? ORDER BY timestamp DESC;",
        user['id'],
    )

    games_list = []
    for review in reviews:
        games_list.append(review['game_id'])
    games_list_str = ','.join([str(game_id) for game_id in games_list])

    games = igdb_query(CLIENT_ID, ACCESS_TOKEN, 'games', f'fields name, cover.image_id; where id = ({games_list_str});')
    
    return render_template('user.html', user=user, games=games, reviews=reviews)


@app.route('/users/<username>/review/<review_id>', methods=["GET", "POST"])
@login_required
def user_review(username, review_id):
    """View full review details of a specific review"""
    user = db.execute(
        "SELECT * FROM users WHERE username = ?;",
        username,
    )
    if user:
        user = user[0]
    else:
        return redirect("/")

    review = db.execute(
        "SELECT reviews.*, users.username FROM reviews JOIN users ON reviews.user_id = users.id WHERE reviews.id = ?;",
        review_id,
    )
    if review:
        review = review[0]
    else:
        return redirect("/")
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        error = False
        # Ensure game_id was submitted
        if not request.form.get("review_id"):
            flash("Review ID required", "error")
            error = True
        
        # Ensure review was submitted
        elif not request.form.get("review"):
            flash("Review content required", "error")
            error = True
        
        # Ensure that the user wrote this review
        elif not session["user_id"] == review["user_id"]:
            flash("Permission denied", "error")
            error = True
        
        # Update review
        if not error:
            db.execute(
                "UPDATE reviews SET rating = ?, review = ? WHERE id = ?;",
                request.form.get("rating"),
                request.form.get("review"),
                request.form.get("review_id"),
            )
            flash("Review updated successfully", "success")

            # Get the updated review data
            review = db.execute(
                "SELECT reviews.*, users.username FROM reviews JOIN users ON reviews.user_id = users.id WHERE reviews.id = ?;",
                review_id,
            )
            if review:
                review = review[0]
            else:
                return redirect("/")
    game = igdb_query(CLIENT_ID, ACCESS_TOKEN, 'games', f'fields name, cover.image_id; where id = {review['game_id']};')
    if game:
        game = game[0]
    else:
        return redirect("/")
    
    return render_template('review.html', user=user, game=game, review=review)


@app.route("/login/", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Referred to Problem Set 9 (CS50 Finance) for login logic

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Username required", "error")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Password required", "error")
            return render_template("login.html")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username"),
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("Incorrect username or password", "error")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout/")
def logout():
    """Log user out"""
    # Referred to Problem Set 9 (CS50 Finance) for logout logic
    
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register/", methods=["GET", "POST"])
def register():
    """Register user"""
    # Referred to Problem Set 9 (CS50 Finance) for register logic

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Username required", "error")
            return render_template("register.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Password required", "error")
            return render_template("register.html")

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            flash("Confirm password required", "error")
            return render_template("register.html")

        # Ensure password and confirmation match
        elif not request.form.get("password") == request.form.get("confirmation"):
            flash("Passwords do not match", "error")
            return render_template("register.html")

        # Ensure username does not already exist
        matching_users = db.execute(
            "SELECT id FROM users WHERE username = ?",
            request.form.get("username"),
        )
        if not len(matching_users) == 0:
            flash("Username already taken", "error")
            return render_template("register.html")

        # Insert user record into database
        rows = db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )

        # Redirect user to home page
        return redirect("/login")
    else:
        return render_template("register.html")
