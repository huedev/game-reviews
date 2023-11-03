from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
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


@app.route('/')
@login_required
def index():
    games = igdb_query(CLIENT_ID, ACCESS_TOKEN, 'games', 'fields name, cover.image_id; where rating > 90; limit 6;')
    return render_template('index.html', games=games)


@app.route('/search/', methods=["GET", "POST"])
@login_required
def search_redirect():
    """Redirect to search results"""
    if request.method == "POST":
        print("Go to search!")
        search = request.form.get("search")
        return redirect(f"/search/{search}")
    else:
        print("Go to home!")
        return redirect("/")


@app.route('/search/<search>', methods=["GET", "POST"])
@login_required
def search(search):
    """Display search results"""
    games = igdb_query(CLIENT_ID, ACCESS_TOKEN, 'games', f'search "{search}"; fields name, cover.image_id; where category = 0; limit 18;')
    return render_template('search.html', search=search, games=games)


@app.route('/game/<game_id>', methods=["GET", "POST"])
@login_required
def game_details(game_id):
    """Game details page"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure game_id was submitted
        if not request.form.get("game_id"):
            return False
        
        # Ensure review was submitted
        elif not request.form.get("review"):
            return False
        
        # Submit review
        db.execute(
            "INSERT INTO reviews (user_id, game_id, rating, review) values(?, ?, ?, ?)",
            session["user_id"],
            request.form.get("game_id"),
            request.form.get("rating"),
            request.form.get("review"),
        )

    game = igdb_query(CLIENT_ID, ACCESS_TOKEN, 'games', f'fields *, cover.image_id, platforms.name, genres.name; where id = {game_id}; limit 1;')[0]
    aggregate_review_data = db.execute(
        "SELECT AVG(rating) as average_rating, COUNT(*) as review_count FROM reviews WHERE game_id = ?;",
        game_id,
    )[0]
    recent_reviews = db.execute(
        "SELECT reviews.*, users.username FROM reviews JOIN users ON reviews.user_id = users.id WHERE game_id = ? ORDER BY timestamp DESC LIMIT 5;",
        game_id,
    )
    return render_template('game.html', game=game, aggregate_review_data=aggregate_review_data, recent_reviews=recent_reviews)


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
            return False

        # Ensure password was submitted
        elif not request.form.get("password"):
            return False

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username"),
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return False

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
            return False

        # Ensure password was submitted
        elif not request.form.get("password"):
            return False

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return False

        # Ensure password and confirmation match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return False

        # Ensure username does not already exist
        matching_users = db.execute(
            "SELECT id FROM users WHERE username = ?",
            request.form.get("username"),
        )
        if not len(matching_users) == 0:
            return False

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
