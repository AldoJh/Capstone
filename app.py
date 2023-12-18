from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(app)

# Set up database configuration
basedir = os.path.dirname(os.path.abspath(__file__))
database_uri = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def as_dict(self):
        return {
                'id': self.id, 
                'nama': self.nama, 
                'email': self.email
                }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

class HelloWorld(Resource):
    def get(self):
        users = User.query.all()
        response = [user.as_dict() for user in users]
        return jsonify(response)


    def post(self):
        data_email = request.form['email']
        data_password = request.form['password']
        data_nama = request.form['nama']

        model = User(nama=data_nama, email=data_email, password=data_password)
        model.save()

        response = {'msg': 'Data berhasil disimpan', 'code': '200'}
        return response
    
class Update(Resource):
    def put(self, id):
        query = User.query.filter_by(id=id).first()

        editNama = request.form['nama']
        editEmail = request.form['email']
        editPassword = request.form['password']

        query.nama = editNama
        query.email = editEmail
        query.password = editPassword
        db.session.commit()

        response = {'msg': 'Data berhasil diupdate', 'code': '200'}
        return response
    
    def delete(self, id):
        query = User.query.get(id)
        db.session.delete(query)
        db.session.commit()

        response = {'msg': 'Data berhasil dihapus', 'code': '200'}
        return response

class Login(Resource):
    def post(self):
        data_email = request.form['email']
        data_password = request.form['password']

        query = User.query.filter_by(email=data_email, password=data_password).first()
        if query is not None:
            response = {'msg': 'Login berhasil', 'code': '200'}
        else:
            response = {'msg': 'Login gagal', 'code': '400'}
        return response


api.add_resource(HelloWorld, '/', methods=['GET', 'POST'])
api.add_resource(Update, '/<id>', methods=['PUT', 'DELETE'])
api.add_resource(Login, '/login', methods=['POST'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True, port=5000)
