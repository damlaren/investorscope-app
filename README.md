investorscope-app
=================

investorscope web application (everything not on the class website).

=== Running Heroku locally ===

Based on instructions at: https://devcenter.heroku.com/articles/getting-started-with-python-o

1. Activate virtualenv:

   $ source venv/bin/activate
   
2. Install dependencies:

   $ pip install Flask gunicorn flask-mongoengine

3. Login to heroku (you'll need a username):

   $ heroku login

4. Run Heroku instance locally or remotely

   a. To run locally:

   $ foreman start

   b. To push to remote instance:

   (TODO-- need to identify instance already running?)

   $ git push heroku master