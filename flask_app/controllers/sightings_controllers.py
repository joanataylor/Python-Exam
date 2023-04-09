from flask_app.models.sighting_model import Sighting
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user_model

# *******- routes to page that shows all sightings -****************
@app.route("/sightings")
def dashboard():
    if not 'uid' in session:
        flash("access denied")
        return redirect("/")
    results = user_model.User.all_sightings_with_users()
    print(results)
    print(session['uid'])
    return render_template('dashboard.html', results=results)

@app.route("/sighting/all")
def all_sightings():
    return render_template('create_sightings.html', all_sightings=Sighting.get_all())

@app.route('/sightings/destroy/<int:id>')
def distroy_sightings(id):
    data = {
        "id": id
    }
    sightings = Sighting.destroy(data)
    return redirect("/sightings")

@app.route('/sightings/display/<int:id>')
def display_sightings(id):
    data = {
        "id": id
    }
    sightings = Sighting.get_one(data)
    return render_template('show_sightings.html', sightings = sightings)

@app.route('/sightings/edit/<int:id>')
def edit_sightings(id):

    data = {
        "id": id
    }
    result = Sighting.get_sighting_by_id(data)
    return render_template('edit_sightings.html', result = result)


@app.route("/create_sighting", methods=["POST"])
def new_sighting():

    if not Sighting.validates_sighting_creation_updates(request.form):
        return redirect("/sighting/all")

    data={
        **request.form,
        "num_views": int(request.form['num_views']),
        "user_id": session['uid']
    }
    Sighting.save(data)
    return redirect("/sightings")

@app.route("/edit_sightings/<int:id>", methods=["POST"])
def updated_sighting(id):

    if not Sighting.validates_sighting_creation_updates(request.form):
        return redirect("/sightings/edit/"+str(id))

    data={
        **request.form,
        "num_views": int(request.form['num_views']),
        "id": id
    }
    Sighting.update(data)
    return redirect("/sightings")