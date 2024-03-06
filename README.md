# CS50 Game Reviews

## About
CS50 Game Reviews is a web application built using Python via the Flask framework, JavaScript for some interactive elements, SQLite for the database that stores users and their reviews, and the [Tailwind CSS](https://tailwindcss.com/) framework to style the application's front-end. It also uses the [IGDB](https://www.igdb.com/) [API](https://api-docs.igdb.com) in order to pull data such as cover art, genres, and platforms on most published video games.

I built this application as my final project for CS50x.

## Installation
Note that these instructions are based on a Windows setup (since it's what I'm using) so the commands may differ for other setups.

1. Clone the repository to your local machine and ensure that you have Python and Node.js installed.
2. In a terminal, navigate to the repository folder and create a virtual environment by running `py -m venv venv`.
3. Activate the virtual environment by running `venv\Scripts\activate`.
5. Go to the [Getting Started](https://api-docs.igdb.com/#getting-started) section of the IGDB docs and set up your account to use the API.
6. Back to the virtual environment terminal, set up your environment variables to use your Client ID and Client Secret by running `$env:FLASK_CLIENT_ID = "<your_client_id>"` and `$env:FLASK_CLIENT_SECRET = "<your_client_secret>"`. See the [Configuring from Environment Variables](https://flask.palletsprojects.com/en/latest/config/#configuring-from-environment-variables) section of the Flask docs for more details.
7. To start the application, run `flask run`.
8. To set up Tailwind CSS, open another terminal in the repository folder and run `npm install`, then run `npm run css` to have Tailwind CSS watch for changes and regenerate the output CSS.
