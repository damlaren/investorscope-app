from flask import session

# Check if the user is logged into their account, using Flask sessions.
# For this demo, we don't care about the specific user, only that someone
# is logged in-- we don't track any other information specific to a user.
def user_is_logged_in():
    if "logged_in" in session:
        return True
    return False

# Log the user in.
def user_log_in():
    session["logged_in"] = 1

# Log the user out.
def user_log_out():
    session.pop("logged_in", None)
