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
            status    TEXT,
            status_last_changed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            image_data   BLOB,
            image_mime TEXT NOT NULL
        )
    """

    SEED_DATA = """
        INSERT INTO instruments (name, status, image_data, image_mime)
        VALUES
            ("12i GNSS", "In R Office", "app/static/images/12i", ".png"),
            ("SX10 Station", "In R Office", "app/static/images/sx10", ".png"),
            ("DiNi Level", "In R Office", "app/static/images/dini", ".png")
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
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            date    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            flexible    BOOLEAN DEFAULT 1,
            in          BOOLEAN DEFAULT 0,
            notes       TEXT,
            
            instrument_booked   INTEGER NOT NULL,
            surveyor_id(s)  INTEGER NOT NULL,

            FOREIGN KEY (instrument_booked) REFERENCES instruments(id),
            FOREIGN KEY (surveyor_id(s)) REFERENCES surveyors(id)
        )
    
    """
    SEED_DATA = "INSERT INTO name (...)" or None
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

