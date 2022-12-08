# SkyPro / Homework 12

Flask application to search posts by text and add new posts!

## Usage

Run "app.py" to start the app.

## App features

* The main page "/" shows search page and "Add post" button.
* "/post" shows a page with a button to add an image and a text field for a comment.
* If you try to get a page that doesn't exist, a 404 error will be applied.

## Known issues

* Error catch does not work when uploading a non-existent image file (commented in "loader/views.py", line "if not image:")