from flask import Flask, Blueprint, flash, render_template_string
from flask_login import login_required

helloworld = Blueprint("helloworld", "helloworld")


def configure(app: Flask):
    app.register_blueprint(helloworld)


template = """
<html>
<body>
    <p>Hello, world!</p>
    <div>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <ul class=flashes>
                {% for message in messages %}
                <li>{{ message }}</li>
                {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
    </div>
    <DIV>
    {{current_user}}
    </div>
</body>
</html>
"""


@helloworld.route("/hello")
@login_required
def hello():
    flash("Whoops!")
    return render_template_string(template)
