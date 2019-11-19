import json
from postTrack_app.tracker import Track

from postTrack_app import db, app, login_manager
from flask import render_template, url_for, redirect, flash, request

from postTrack_app.forms import BookmarkForm, ItemForm
from postTrack_app import models
from flask_login import login_required, login_user, logout_user, current_user
from postTrack_app.forms import LoginForm, SignupForm


global_count = 0
messages = []


@login_manager.user_loader
def load_user(userid):
    return models.User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():
    ans = render_template('index.html', top_url=models.URL.newest(5))
    return ans


@app.route('/user/<username>')
def user(username):
    user_obj = models.User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user_obj)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ItemForm()
    if form.validate():

        tracking = form.tracking.data
        description = form.description.data
        tracking_item = models.Item(description=description, tracking_id=tracking, user=current_user)
        db.session.add(tracking_item)
        db.session.commit()
        return render_template('user.html', user=current_user)
    return render_template('add.html', form=form)


@app.route('/track', methods=['GET', 'POST'])
@login_required
def track():
    pkg = 'LO252674388CN'
    urlStr = ""
    data = dict(tracking_number=pkg)
    requestData = json.dumps(data)
    result = Track.trackingmore(requestData, urlStr, "carriers/detect")
    json_res = json.loads(result.decode())
    if json_res['meta']['code'] == 200:
        carrier = json_res['data'][0]['code']
        data["carrier_code"] = carrier
        # requestData = json.dumps(data)
        # result = Track.trackingmore(requestData, urlStr, "post")
        urlStr = f"/{carrier}/{pkg}"
        requestData = ''
        result = Track.trackingmore(requestData, urlStr, "codeNumberGet")
        json_res = json.loads(result.decode())
    return json.dumps(str(json_res['data']['destination_info']['trackinfo']))
    # return str(json_res['data']['destination_info']['trackinfo'])
    # return json_res


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_obj = models.User.get_by_username(form.username.data)
        if user is not None:
            login_user(user_obj, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user_obj.username))
            return redirect(request.args.get('next') or #url_for('index'))
                            url_for('user', username=user_obj.username))
        flash('Incorrect username or password.')
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user_obj = models.User(email=form.email.data,
                    username=form.username.data,
                    password = form.password.data)
        db.session.add(user_obj)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user_obj.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.route("/remove", methods=["GET", "POST"])
def remove():
    try:
        obj_to_delete = db.session.query(models.Item).\
            filter(models.Item.tracking_id == request.get_json()["tracking_number"]).first()
        db.session.delete(obj_to_delete)
        db.session.commit()
    except Exception as e:
        print (e)
    return render_template('user.html', user=current_user)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_404(e):
    return render_template('500.html'), 500
