import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect Existing Database Into a New Model
Base = automap_base()
# Reflect the Tables
Base.prepare(engine, reflect=True)

# Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)


# Flask Routes
# Home Route
@app.route("/")
def welcome():
        return """<html>
<h1>Hawaii Climate App (Flask API)</h1>
<p>Precipitation Analysis:</p>
<ul>
  <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
</ul>
<p>Station Analysis:</p>
<ul>
  <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
</ul>
<p>Temperature Analysis:</p>
<ul>
  <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
</ul>
<p>Start Day Analysis:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14">/api/v1.0/2017-03-14</a></li>
</ul>
<p>Start & End Day Analysis:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2017-03-14/2017-03-28</a></li>
</ul>
</html>
"""

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        prcp_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        prcp_data_list = dict(prcp_data)
        return jsonify(prcp_data_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        stations_all = session.query(Station.station).all()
        station_list = list(stations_all)
        stations = list(np.ravel(station_list))
        return jsonify(stations=stations)

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        tobs_data = session.query(Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        tobs_data_list = list(np.ravel(tobs_data))
        return jsonify(tobs_data_list=tobs_data_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        start_day_list = list(np.ravel(start_day))
        return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        return jsonify(start_end_day_list)

# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)