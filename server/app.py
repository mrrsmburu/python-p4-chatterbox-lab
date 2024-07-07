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

@app.route('/messages')
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([{
            'id': message.id,
            'username': message.username,
            'body': message.body,
            'created_at': message.created_at,
            'updated_at': message.updated_at
        } for message in messages]), 200

    elif request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        body = data.get('body')

        if not username or not body:
            return make_response(jsonify({"error": "Username and body are required"}), 422)

        new_message = Message(username=username, body=body)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({
            'id': new_message.id,
            'username': new_message.username,
            'body': new_message.body,
            'created_at': new_message.created_at,
            'updated_at': new_message.updated_at
        }), 201

    

@app.route('/messages/<int:id>')
def messages_by_id(id):
    message = Message.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify({
            'id': message.id,
            'username': message.username,
            'body': message.body,
            'created_at': message.created_at,
            'updated_at': message.updated_at
        }), 200

    elif request.method == 'PATCH':
        data = request.get_json()
        body = data.get('body')

        if not body:
            return make_response(jsonify({"error": "Body is required"}), 422)

        message.body = body
        db.session.commit()

        return jsonify({
            'id': message.id,
            'username': message.username,
            'body': message.body,
            'created_at': message.created_at,
            'updated_at': message.updated_at
        }), 200

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    app.run(port=5555)
