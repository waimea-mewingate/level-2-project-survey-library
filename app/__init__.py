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
            SELECT instrument_id, name, status, status_last_changed
            FROM instruments
            ORDER BY instrument_id
        """
        params = ()
        instruments = db.execute(sql, params).fetchall()

        flash("Test message")

        return render_template("pages/home.jinja", instruments=instruments)
#-----------------------------------------------------------
# Single instrument page with status editing
#-----------------------------------------------------------
@app.get('/instrument/<int:id>')
def get_instrument(id):
    with connect_db() as db:
        sql = """
        SELECT name, status, status_last_changed
        FROM instruments 
        WHERE instrument_id=?
        """
        params = (id,)
        instrument = db.execute(sql, params).fetchone()

        return render_template("pages/instrument_single.jinja", instrument=instrument)
    
# Edit ---------------------------
@app.get("/instrument/<int:id>/edit")
def instrument_editing_form(id):
    with connect_db() as db:
        sql = """
            SELECT instrument_id, name, status, status_last_changed
            FROM instruments
            WHERE instrument_id=?
        """
        params = (id,)
        instrument = db.execute(sql, params).fetchone()

        return render_template("pages/edit_instrument_form.jinja", instrument=instrument)
    
# Process ------------------------
@app.post("/instrument/<int:id>")
def update_instrument(id): 

    status = request.form.get('status', '').strip()

    with connect_db() as db:
        sql = """
            UPDATE instruments
            SET status=?, status_last_changed = CURRENT_TIMESTAMP
            WHERE instrument_id=?
        """
        params = (status, id)
        db.execute(sql, params)

        flash("Status updated", "success")
        return redirect(f"/instrument/{id}")
    
#----------------------------------------------------------
# New Instrument
#-----------------------------------------------------------
@app.get('/instrument/new')
def show_instrument_form():
    return render_template("pages/instrument_form.jinja")

# Process new instrument ------------------------------------------

@app.post("/instrument")
def add_instrument():
    name = request.form.get('name', '').strip()
    status = request.form.get('status', '').strip()
    
    if not name:
        flash("Name is required", "error")
        return redirect("/instrument/new")
    
    if not status:
        flash("Status is required", "error")
        return redirect("/instrument/new")


    name = html.escape(name)

    with connect_db() as db:
        sql = """
            INSERT INTO instruments (name, status)
            VALUES (?, ?)
        """
        params = (name, status)
        db.execute(sql, params)

        flash("Instrument added", "success")
        return redirect("/")

#===========================================================
# BOOKINGS
#===========================================================
@app.get("/bookings")
def show_bookings():
    with connect_db() as db:
        sql = """
            SELECT 
                bookings.booking_id, 
                bookings.created, 
                bookings.date_booked,
                bookings.booking_end, 
                bookings.flexible, 
                bookings.in_out, 
                bookings.notes,
                bookings.instrument_booked, 
                bookings.person_booking,
                surveyors.name AS surveyor_name,
                instruments.name AS instrument_name
            
            FROM bookings
            JOIN surveyors ON surveyors.surveyor_id = bookings.person_booking
            JOIN instruments ON instruments.instrument_id = bookings.instrument_booked
            
            ORDER BY date_booked DESC, created DESC
        """
        params = ()
        bookings = db.execute(sql, params).fetchall()

        return render_template("pages/booking_list.jinja", bookings=bookings)
#-----------------------------------------------------------------------    
# New Booking
#----------------------------------------------------------------------- 
@app.get('/booking/new')
def show_booking_form():
    return render_template("pages/booking_form.jinja")

# Process -----------------------------
@app.post("/booking")
def add_booking():
    date_booked = request.form.get('startdate' '').strip()
    booking_end = request.form.get('enddate' '').strip()
    
    flexible = bool(request.form.get('flex'))
    
    booking_notes = request.form.get('notes' '').strip()
        
    instrument_name = request.form.get('instrument', '').strip()
    person_booking = request.form.get('surveyor', '').strip()

    if not instrument_name:
        flash("Instrument is required", "error")
        return redirect("/booking/new")
    
    if not person_booking:
        flash("Surveyor is required", "error")
        return redirect("/booking/new")
    
    if not date_booked:
        flash("Start date is required", "error")
        return redirect("/booking/new")
    
    if not booking_end:
        flash("End date is required", "error")
        return redirect("/booking/new")
    
    notes = html.escape(booking_notes) if not None else null    
    
    # THIS INSERTS A NAME INSTEAD OF AN INSTRUMENT ID - HOW TO MAKE READABLE FOR FORM BUT INPUT ID??

    with connect_db() as db:
        sql = """
            INSERT INTO bookings (date_booked, booking_end, flexible, notes, instrument_booked, person_booking)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (date_booked, booking_end, flexible, notes, instrument_name, person_booking)
        db.execute(sql, params)

        flash("Booking added", "success")
        return redirect("/")
    
# Delete booking ---------------------------------------------
@app.get("/booking/<int:id>/delete")
def delete_booking(id):
    with connect_db() as db:
        sql = """
            DELETE FROM bookings
            WHERE id=?
        """
        params = (id,)
        db.execute(sql, params)

        flash("Booking deleted", "success")
        return redirect("/")   


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

