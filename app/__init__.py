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
            SELECT id, name, status, status_last_changed
            FROM instruments
            ORDER BY id DESC
        """
        params = ()
        instruments = db.execute(sql, params).fetchall()

        flash("Test message")

        return render_template("pages/instruments.jinja", instruments=instruments)
#----------------------------------------------------------
# Instrument page
#-----------------------------------------------------------
@app.get('/instrument/<int:id>')
def get_instrument(id):
    with connect_db() as db:
        sql = "SELECT name FROM instruments WHERE id=?"
        params = (id,)
        instrument = db.execute(sql, params).fetchone()

        return render_template("pages/instrument.jinja", instrument=instrument)
    


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

