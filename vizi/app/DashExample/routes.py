from . import blueprint
from flask import render_template
from flask_login import login_required
from Dashboard import Dash_App1, Dash_App2,Dash_App3, Test1

nav = [{'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'}]

@blueprint.route('/app1')
@login_required
def app1_template():
    return render_template('app1.html', dash_url = Dash_App1.url_base,nav=nav)

@blueprint.route('/app2')
@login_required
def app2_template():
    return render_template('app2.html', dash_url = Dash_App2.url_base,nav=nav)

@blueprint.route('/app3')
@login_required
def app3_template():
    return render_template('app3.html', dash_url = Dash_App3.url_base,nav=nav)

@blueprint.route('/test1')
@login_required
def test1_template():
    return render_template('test1.html', dash_url = Test1.url_base,nav=nav)