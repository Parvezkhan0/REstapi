from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name_)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app) 
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

User_args = reqparse.RequestParser()
User_args.add_argument('name', type=str, required=True, help="Name Cannot be Blank")
User_args.add_argument('email', type=str, required=True, help="Email Cannot be Blank")

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = User_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        return user, 201

class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user

    @marshal_with(userFields)
    def put(self, id):
        args = User_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user

    @marshal_with(userFields)
    def patch(self, id):
        args = User_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        if "name" in args:
            user.name = args["name"]
        if "email" in args:
            user.email = args["email"]
        db.session.commit()
        return user

    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        return '', 204

api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

@app.route("/")
def Home():
    return '<h1>Hello world</h1>'

@app.route("/u1")
def Nextpage():
    return '<h1>This is next page</h1>'

if __name__ == '__main__':
    # Create database and tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
