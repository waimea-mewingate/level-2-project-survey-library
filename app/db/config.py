#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#----------------------------------------------------------------------------
# Define your tables with a name, a schema and optional seed/sample data,
# using this format, and then add the tables to the Table Registry below:
#
# class TableName:
#     NAME      = "name"
#     SCHEMA    = "CREATE TABLE name (...)"
#     SEED_DATA = "INSERT INTO name (...)" or None
#----------------------------------------------------------------------------

class InstrumentTable:

    NAME = "instruments"

    SCHEMA = """
        CREATE TABLE instruments (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name   TEXT NOT NULL,
            status    TEXT NOT NULL,
            status_last_changed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes       TEXT
        )
    """

    SEED_DATA = """
        INSERT INTO instruments (name, status, notes)
        VALUES
            ("12i GNSS", "In R Office", "Check for damage"),
            ("SX10 Station", "In R Office", "[sample note]"),
            ("DiNi Level", "In R Office", "PLEASE watch where you leave this!")
    """

class SurveyorTable:

    NAME      = "surveyors"
    SCHEMA    = """
        CREATE TABLE surveyors (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL
    )
    """
    SEED_DATA = """
        INSERT INTO surveyors (name)
        VALUES   
            ("Nick"),
            ("Ben"),
            ("Fred"),
            ("Mike"),
            ("Matt"),
            ("Grant"),
            ("Kirsten")
    """

class BookingTable:
    NAME      = "bookings"
    SCHEMA    = """
        CREATE TABLE bookings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            created     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_booked DATE NOT NULL,
            booking_end DATE NOT NULL,
            flexible    BOOLEAN DEFAULT 1,
            in_out      BOOLEAN DEFAULT 1,
            notes       TEXT,
            
            instrument_booked   INTEGER NOT NULL,
            person_booking      INTEGER NOT NULL,

            FOREIGN KEY (instrument_booked) REFERENCES instruments(id),
            FOREIGN KEY (person_booking)    REFERENCES surveyors(id)
        )
    
    """
    SEED_DATA = """
        INSERT INTO bookings (date_booked, booking_end, instrument_booked, person_booking, notes)
        VALUES 
            ( "2026-08-22", "2026-08-27" , 1, 2, "" ),
            ( "2026-08-27", "2026-08-28" , 1, 5, "[sample note]" ),
            ( "2026-08-27", "2026-09-01" , 3, 1, "Past Booking!" ),
            ( "2026-08-24", "2026-08-25" , 3, 2, "" ),
            ( "2027-04-18", "2027-04-23" , 2, 3, "Remember to give Maia feedback- any is appreciated!")
    """
#----------------------------------------------------------------------------
# Table registry
#----------------------------------------------------------------------------
# Register all of your tables by adding them to the TABLES list here:
#
# TABLES = [
#     Table1Name,
#     Table2Name,
#     etc.
# ]
#
# Note: The table order is important - Create the tables that have
# foreign keys *after* the tables they link to have been created
#----------------------------------------------------------------------------

TABLES = [
    InstrumentTable,
    SurveyorTable,
    BookingTable
]

