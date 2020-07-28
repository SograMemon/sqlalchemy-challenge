import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement= Base.classes.measurement
Station= Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of date and prcp"""
    # Query all dates and prcp
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_measurements = []
    for date, prcp in results:
        measurements_dict = {}
        measurements_dict["date"] = date
        measurements_dict["prcp"] = prcp
        all_measurements.append(measurements_dict)

    return jsonify(all_measurements)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of station and tempreture within last 12 months"""
    lastDay= dt.date(2017,8,23)
    firstDay= lastDay - dt.timedelta(days=365)
    # Query all dates and prcp
    sel = [Measurement.station, 
       Measurement.tobs]

    results = session.query(*sel).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date <= lastDay).\
    filter(Measurement.date >= firstDay).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurements
    all_measurements = []
    for station, tobs in results:
        measurements_dict = {}
        measurements_dict["station"] = station
        measurements_dict["tobs"] = tobs
        all_measurements.append(measurements_dict)

    return jsonify(all_measurements)

@app.route("/api/v1.0/<start>")
def start(start):
    end=dt.date(2017,8,23)
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of station and tempreture within last 12 months"""

    # Query all dates within range
    sel = [ 
       func.min(Measurement.tobs),
       func.avg(Measurement.tobs),
       func.max(Measurement.tobs),
       ]

    results = session.query(*sel).\
    filter(Measurement.date <= end).\
    filter(Measurement.date >= start).all()

    session.close()


    # Create a dictionary from the row data and append to a list of all_measurements
    all_measurements = []
    for tmin, tavg, tmax in results:
        measurements_dict = {}
        measurements_dict["Tmin"] = tmin
        if measurements_dict["Tmin"] == None:
            return jsonify({"error": f"start date {start} not found."}), 404
        measurements_dict["Tavg"] = tavg
        measurements_dict["Tmax"] = tmax
        
        all_measurements.append(measurements_dict)

    return jsonify(all_measurements)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of station and tempreture within last 12 months"""

    # Query all dates within range
    sel = [ 
       func.min(Measurement.tobs),
       func.avg(Measurement.tobs),
       func.max(Measurement.tobs),
       ]

    results = session.query(*sel).\
    filter(Measurement.date <= end).\
    filter(Measurement.date >= start).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurements
    all_measurements = []
    for tmin, tavg, tmax in results:
        measurements_dict = {}
        measurements_dict["Tmin"] = tmin
        if measurements_dict["Tmin"] == None:
            return jsonify({"error": f"start date {start} not found."}), 404
        measurements_dict["Tavg"] = tavg
        measurements_dict["Tmax"] = tmax
        
        all_measurements.append(measurements_dict)

    return jsonify(all_measurements)

    


if __name__ == '__main__':
    app.run(debug=True)

