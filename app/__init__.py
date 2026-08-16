#===========================================================
# Survey Instrument Library
# By Maia Wingate
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Home page - Show all instruments
#-----------------------------------------------------------
@app.get("/")
def show_instruments():
    with connect_db() as db:
        sql = """
            SELECT id, name, status, status_last_changed, image_data
            FROM instruments
            ORDER BY id DESC
        """
        params = ()
        instruments = db.execute(sql, params).fetchall()

        flash("Test message")

        return render_template("pages/instruments.jinja", instruments=instruments)
    
#-----------------------------------------------------------
# Instrument Imaging
#-----------------------------------------------------------
@app.post("/image")
def add_image():
    # Get the normal text fields from the form
    name = request.form.get('name', '').strip()
    name = html.escape(name)

    # Get the file selected via the form
    image = request.files.get('name', None)
    if not image or image.filename == '':
        flash("There was a problem uploading the image", "error")
        return redirect("/")

    # Get the file binary data, and the file MIME type
    image_data = image.read()
    image_mime = image.mimetype

    # Add the form data and file binary data to DB
    with connect_db() as db:
        sql = """
            INSERT INTO instruments (name, image_data, image_mime)
            VALUES (?, ?, ?)
        """
        params = (name, image_data, image_mime)
        db.execute(sql, params)

        flash(f"Image {name} added", "success")
        return redirect("/")
#-----------------------------------------------------------
# Instrument page
#-----------------------------------------------------------
@app.get('//<int:id>')
def get_instrument(id):
    with connect_db() as db:
        sql = "SELECT name FROM instruments WHERE id=?"
        params = (id,)
        instrument = db.execute(sql, params).fetchone()

        return render_template("pages/instrument.jinja", instrument=instrument)
    
#-----------------------------------------------------------
# Instrument page w/ image
#-----------------------------------------------------------
@app.get('//<int:id>/image')
def get_instrument_image(id):
    with connect_db() as db:
        sql = "SELECT image_data, image_mime FROM instruments WHERE id=?"
        params = (id,)
        image = db.execute(sql, params).fetchone()

        if not image:
            abort(404)

        return make_response(
            send_file(
                BytesIO(image["image_data"]),
                mimetype=image["image_mime"]
            )
        )

#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

