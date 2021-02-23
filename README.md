## Feedback App

This app allows the creation and deletion of user accounts with authentication using bcrypt.

Users may submit feedback, which is viewable to any logged-in user along with the user's account details (not the way I'd do it for a real app!).

Only the logged-in user may edit or delete their own feedback or delete their own account.

### Setup

Create a postgres database named 'flask_feedback' and then run seed.py to set up the database.