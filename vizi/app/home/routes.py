from . import blueprint
from flask import render_template
from flask_login import login_required, current_user


@blueprint.route('/')
@login_required
def index():
    nav = [{'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'App1', 'url': '/DashExample/app1'},
           {'name': 'App2', 'url': '/DashExample/app2'},
           {'name': 'App3', 'url': '/DashExample/app3'},
           {'name': 'Test1', 'url': '/DashExample/test1'}]
    return render_template('index.html', nav=nav)