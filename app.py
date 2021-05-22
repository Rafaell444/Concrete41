from flask import Flask, render_template, request, Response, session, redirect, url_for
from flask_babel import Babel, get_locale, gettext
from mysql import connector

from config import Config

app = Flask(__name__)
babel = Babel(app)

config_instance = Config()
app.config["secret_key"] = "mysecreto"

db_config = {"user": config_instance.USER, "password": config_instance.PASSWORD,
             "host": config_instance.HOST,
             "database": config_instance.DATABASE}


# multilingual translation
@babel.localeselector
def localselector():
    return request.accept_languages.best_match(["en_US", "ka_GE"])
    # return "en"


def fetch_from_database(table_name, columns: list):
    columns = ", ".join(columns)
    # ბაზასთან დაკავშირება
    conn = connector.connect(**db_config)
    cursor = conn.cursor()

    # sql-ის ბრძანება
    _SQL = f"SELECT {columns} FROM {table_name}"
    cursor.execute(_SQL)

    fetch = cursor.fetchall()
    cursor.close()
    conn.close()

    return fetch


@app.route('/')
def hello_world():
    return render_template("index.html", locale=get_locale(), )


@app.route('/terms')
def terms():
    return render_template("terms.html")


@app.route('/policy')
def policy():
    return render_template("policy.html")


@app.route('/care')
def care():
    return render_template("care.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/flowerpot')
def flowerpot():
    product_dict = {}

    products = fetch_from_database("products", ["id", "price", "code", "height", "inner_diameter", "outer_diameter"])
    colors = fetch_from_database("colors", ["product_id", "color"])

    for product in products:
        product_id = product[0]
        product_dict[product_id] = list(product[1:])

    for i in colors:
        product_id = i[0]
        color_name = i[1]

        if product_id in product_dict:
            product_dict[product_id].append(color_name)

    print(product_dict)
    return render_template("flowerpot.html", product_dict=product_dict)


@app.route('/ashtray')
def ashtray():
    return render_template("ashtray.html")


@app.route('/chess')
def chess():
    return render_template("chess.html")


@app.route('/lamp')
def lamp():
    return render_template("lamp.html")


@app.route('/sale')
def sale():
    return render_template("sale.html")


@app.route('/save_response', methods=["POST"])
def save_response():
    with open("mails.txt", "a") as write_email:
        print(request.form)
        write_email.write(request.form["email_data"] + "\n")

        return Response("successful")


@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/admin/aflowerpot')
def aflowerpot():
    return render_template("adminflowerpot.html")


@app.route('/admin/anashtray')
def anashtray():
    return render_template("anashtray.html")


@app.route('/admin/achess')
def achess():
    return render_template("achess.html")


@app.route('/admin/alamp')
def alamp():
    return render_template("alamp.html")


@app.route('/admin/asale')
def asale():
    return render_template("asale.html")


if __name__ == '__main__':
    app.run(debug=True)

# 3pybabel compile -d translations
# 2pybabel init -i messages.pot -d translations -l ka
# 1pybabel extract -F babel.cfg -o messages.pot .
