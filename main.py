import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # dictionary = {}
        # for column in self.__table__.columns:
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary

        # Alternate approach
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record


@app.route('/random', methods=["GET"])
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route('/all')
def get_all_cafe():
    cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


@app.route('/search')
def search_cafe():
    query_location = request.args.get('loc')
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry we don't have a cafe at that location"})

# HTTP POST - Create Record


@app.route('/add', methods=["GET", "POST"])
def add_new_cafe():
    if request.method == "POST":
        new_cafe = Cafe(name=request.form.get('name'),
                        map_url=request.form.get('map_url'),
                        img_url=request.form.get('img_url'),
                        location=request.form.get('location'),
                        seats=request.form.get('seats'),
                        has_toilet=bool(request.form.get('has_toilet')),
                        has_wifi=bool(request.form.get('has_wifi')),
                        has_sockets=bool(request.form.get('has_sockets')),
                        can_take_calls=bool(request.form.get('can_take_calls')),
                        coffee_price=request.form.get('coffee_price')
                        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})

# HTTP PUT/PATCH - Update Record


@app.route('/update-price/<int:id>', methods=["PATCH"])
def update_price(id):
    cafe_to_update = Cafe.query.get(id)
    if cafe_to_update:
        cafe_to_update.coffee_price = request.args.get('new_price')
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


# HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>', methods=["DELETE"])
def delete_cafe(cafe_id):
    if request.method == "DELETE":
        cafe_to_delete = Cafe.query.get(cafe_id)
        if cafe_to_delete:
            if request.args.get('api_key') == "secret":

                db.session.delete(cafe_to_delete)
                db.session.commit()
                return jsonify(response={"success": "successfully deleted the cafe."}), 200
            else:
                return jsonify(
                    error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


if __name__ == '__main__':
    app.run(debug=True)


# MY_FIRST_API = https://documenter.getpostman.com/view/14518931/TzRYdQYZ
