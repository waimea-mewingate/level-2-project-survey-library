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
            ("SX10 Station", "In Office - Mot", "[sample note]"),
            ("DiNi Level", "In R Office", "PLEASE watch where you leave this!"),
            ("R10 GNSS", "In Office - Mot", ""),
            ("S6 Station", "Out For Servicing", ""),
            ("Mavic Drone", "In Use - In Field", "")
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
            startdate   DATETIME NOT NULL,
            enddate     DATETIME NOT NULL,
            flexible    BOOLEAN DEFAULT 1,
            in_out      BOOLEAN DEFAULT 1,
            notes       TEXT,
            
            instrument     INTEGER NOT NULL,
            surveyor         INTEGER NOT NULL,

            FOREIGN KEY (instrument) REFERENCES instruments(id),
            FOREIGN KEY (surveyor)    REFERENCES surveyors(id)
        )
    
    """
    SEED_DATA = """
        INSERT INTO bookings (startdate, enddate, instrument, surveyor, notes)
        VALUES 
            ( "2026-08-22T09:00", "2026-08-27T15:00" , 1, 2, "" ),
            ( "2026-08-27T09:00", "2026-08-28T15:00" , 1, 5, "[sample note]" ),
            ( "2026-08-27T09:00", "2026-09-01T15:00" , 3, 1, "Past Booking!" ),
            ( "2026-08-24T09:00", "2026-08-25T15:00" , 3, 2, "" ),
            ( "2027-04-18T09:00", "2027-04-23T15:00" , 2, 3, "Remember to give Maia feedback- any is appreciated! Also, this site will update after every work session I do :)")
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

