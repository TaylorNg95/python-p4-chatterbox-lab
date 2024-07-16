from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by('created_at').all()
        messages_dict = [message.to_dict() for message in messages]
        return make_response(messages_dict, 200)
    
    elif request.method == 'POST':
        data = request.get_json()
        body = data.get('body')
        username = data.get('username')
        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        db.session.commit()
        return make_response(new_message.to_dict(), 201)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if request.method == 'PATCH':
        message.body = request.get_json().get('body')
        message.username = request.get_json().get('username')
        db.session.add(message)
        db.session.commit()
        return make_response(message.to_dict(), 200)
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return {'message': 'record successfully deleted!'}

if __name__ == '__main__':
    app.run(port=5555)
