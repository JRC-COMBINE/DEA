#!/usr/bin/python
# -*- coding:utf-8 -*-

from time import sleep

import os
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
from flask import Flask, flash, redirect, render_template, request, url_for
from dea.cohort import Cohort
import logging
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.palettes import Category20
from bokeh.models import ColumnDataSource, HoverTool
logging.basicConfig(level=logging.INFO)

COHORT = None

def filter_short_stay(e):
    """Filter encounters with a length of stay of less than 3 days"""
    if e.dynamic.index[-1] < pd.Timedelta(days=3):
        return True
    return False

ACTIVE_FILTERS = []
FILTERS = {
    "Short Stay": filter_short_stay
}

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev'
)
app.logger.info("Scanning for available cohorts...")
try:
    available_cohorts = [str(c) for c in Path(os.path.dirname(__file__)+"/data").iterdir() if c.is_dir()]
    app.logger.info("Found the following cohorts:")
    for c in available_cohorts:
        app.logger.info(f" - {c}")
except:
    available_cohorts = []
    app.logger.warning("No cohorts found! Place some in data/!")


@app.route('/')
def index():
    """Flask Route for "/".
    
    Entrypoint for the webserver. Lists all available Cohorts as defined in app.py.  
    Renders a cohort-selection screen. 
    
    Returns:
        Renders the index.html template
    """
    return render_template("index.html", available_cohorts=available_cohorts)

@app.route('/set_cohort', methods=['POST'])
def set_cohort():
    """Flask Route for "/set_cohort".
    
    Run when a cohort is selected either on the starting page, or later on through the menu.  
    
    Internally changes the COHORT and loads the relevant data into COHORT.
    
    Returns:
        Redirects to /overview
    """
    global COHORT
    cohort_choice = request.form["cohort"]
    app.logger.info(f"Set cohort to {cohort_choice}")
    COHORT = Cohort.from_path(cohort_choice)
    return redirect(url_for("overview"))

@app.route('/search', methods=['POST'])
def search():
    """Flask Route for "/search".
    
    Used to quickly navigate to individual encounters.
    
    Returns:
        Redirects to the searched encounter if available, or to the /overview page if an error occurs.
    """
    query = request.form["query"]
    app.logger.info(f"Searching for {query} ...")
    try:
        eid = int(query)
        return route_encounter(eid)
    except ValueError:
        # This is only valid for our specific use case as we ID by integer
        flash("Invalid query. Could not convert to integer.", "alert-secondary")
        return redirect(url_for("overview"))
    except IndexError:
        flash(f"Invalid query. Could not find encounter: {query}", "alert-secondary")
        return redirect(url_for("overview"))

@app.route('/process')
def process():
    if COHORT is None:
        return redirect(url_for("index"))
    app.logger.info(f"Processing cohort {COHORT}")
    COHORT.process()
    flash("Processing finished.", "alert-success")
    return redirect(url_for("overview"))

@app.route('/process/<int:id>', methods=['POST'])
def process_encounter(id):
    """Flask Route for "/process/<id>".
    
    *Redirects to the index page for cohort selection if no cohort is currently selected.*
    
    **Processes an individual encounter.**
    
    Returns:
        Redirects to /encounter/<id>
    """
    if COHORT is None:
        return redirect(url_for("index"))
    e = [e for e in COHORT.encounters if e.id == int(id)][0]
    app.logger.info(f"Processing encounter {e.id}")
    e.process()
    flash(f"Encounter {e.id} processed.", "alert-success")
    return redirect(url_for(f"encounter_list"))

def plot_cohort_hist():
    """Plot a histogram of the cohort's length of stay"""
    
    p = figure(plot_width=800, plot_height=400, sizing_mode="scale_width", toolbar_location=None)
    p.background_fill_color = "#f8f9fa"
    p.border_fill_color = "#f8f9fa"
    p.xaxis.axis_label = 'Length of stay (hours)'
    p.yaxis.axis_label = 'Count'

    # Histogram
    los_list = [e.dynamic.index[-1] for e in COHORT.encounters]
    los_h = [xi/np.timedelta64(1, 'h') for xi in los_list]  # convert to hours
    arr_hist, edges = np.histogram(los_h, bins="auto")

    # Column data source
    arr_df = pd.DataFrame({'count': arr_hist, 'left': edges[:-1], 'right': edges[1:]})
    arr_df['f_count'] = ['%d' % count for count in arr_df['count']]
    arr_df['f_interval'] = ['%d to %d ' % (left, right) for left, right in zip(arr_df['left'], arr_df['right'])]
    arr_src = ColumnDataSource(arr_df)

    # Add a quad glyph with source this time
    p.quad(bottom=0, top='count', left='left', right='right', source=arr_src)

    # Add a hover tool referring to the formatted columns
    hover = HoverTool(tooltips = [('LOS', '@f_interval'),
                                  ('Count', '@f_count')])

    # Add the hover tool to the graph
    p.add_tools(hover)
    los_plot = file_html(p, CDN, "LOS distribution")
    return los_plot

@app.route('/overview')
def overview():
    """Flask Route for "/overview".
    
    *Redirects to the index page for cohort selection if no cohort is currently selected.*

    Otherwise renders the cohort overview.

    **You can add custom plots for the cohort.**
    
    Returns:
        Renders the overview.html template
    """
    if COHORT is None:
        return redirect(url_for("index"))
    app.logger.info(f"Rendering overview for cohort {COHORT}")
    los_list = [e.dynamic.index[-1] for e in COHORT.encounters]
    LOS = pd.Series(los_list).median()
    LOS = f"{LOS.days} days and {LOS.seconds // 3600} hours"
    return render_template("overview.html", COHORT=COHORT, available_cohorts=available_cohorts, LOS=LOS, los_plot=plot_cohort_hist())

@app.route('/encounter_list')
def encounter_list():
    """Flask Route for "/encounter_list".
    
    *Redirects to the index page for cohort selection if no cohort is currently selected.*

    Otherwise shows a list of encounters in the current cohort.  

    **Custom filters can be added here, as well as additional information that should be shown, such as length of stay or age**
    
    Returns:
        Renders the encounter_list.html template
    """
    if COHORT is None:
        return redirect(url_for("index"))
    app.logger.info(f"Rendering encounter list for cohort {COHORT}")
    filtered = COHORT
    global ACTIVE_FILTERS
    if ACTIVE_FILTERS is not None or len(ACTIVE_FILTERS) == 0:
        filtered_encounters = []
        for e in COHORT.encounters:
            for filter_name in ACTIVE_FILTERS:
                if not FILTERS[filter_name](e):
                    break
            else:
                filtered_encounters.append(e)
        c = Cohort()
        c.encounters = filtered_encounters
        c.static = COHORT.static
    else:
        c = COHORT
    return render_template("encounter_list.html", COHORT=c, FILTERS=sorted(FILTERS), ACTIVE_FILTERS=sorted(ACTIVE_FILTERS))

@app.route('/set_filters', methods=['POST'])
def set_filters():
    """Currently not used."""
    global ACTIVE_FILTERS
    ACTIVE_FILTERS = []
    for filter_name in FILTERS:
        if request.form.get(filter_name) == "on":
            ACTIVE_FILTERS.append(filter_name)
    return redirect(url_for("encounter_list"))

@app.route('/encounter/<id>', methods=['POST', 'GET'])
def route_encounter(id):
    """Flask Route for "/encounter/<id>".
    
    *Redirects to the index page for cohort selection if no cohort is currently selected.*
    
    **Custom plots for individual encounters can be added here. Custom computations can be executed on encounter level here as well.**
    
    Returns:
        Renders the encounter.html template
    """
    if COHORT is None:
        return redirect(url_for("index"))
    e = [e for e in COHORT.encounters if e.id == int(id)][0]
    app.logger.info(f"Creating plots for encounter {e.id}")

    X = e.dynamic.index
    features = ["Horowitz-Quotient_(ohne_Temp-Korrektur)", "individuelles_Tidalvolumen_pro_kg_idealem_Koerpergewicht", "AF_spontan", "AF", "PEEP", "Compliance", "SpO2", "PCT", "Leukozyten", "paCO2_(ohne_Temp-Korrektur)", "paO2_(ohne_Temp-Korrektur)", "FiO2"]
    p = figure(plot_width=800, plot_height=400, x_axis_type="datetime", title="Horowitz Relevant Parameters", sizing_mode="scale_width")
    for y in features:
        p.line(X, e.dynamic[y], line_width=2, legend_label=y, color=Category20[len(features)][features.index(y)])
    p.legend.click_policy="mute"
    p_html_str = file_html(p, CDN)
    
    plots = [p_html_str]

    import pygwalker as pyg
    pygplot = pyg.walk(e.dynamic, return_html=True)

    return render_template("encounter.html", e=e, plots=plots, pygplot=pygplot)
