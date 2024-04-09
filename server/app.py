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
        messages = Message.query.order_by(Message.created_at).all()
        message_dict = [message.to_dict() for message in messages ]
         
        return make_response(
            jsonify(message_dict),
            200)
    
    elif request.method == 'POST':
        request_data = request.get_json()
        new_message = Message(
            body = request_data["body"],
            username = request_data["username"]      
        )
       
        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message.to_dict()), 201
    


@app.route('/messages/<int:id>', methods= ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if message == None:
        response_body = {
            "message": "This record doesnot exist in our database. Please try again."
        }
        return make_response(response_body, 404)
    
    else:
        if request.method == 'GET':
            message_dict = message.to_dict()

            return make_response(message_dict, 200)
        
        elif request.method == 'PATCH':
            request_data = request.get_json()
            for attr in request_data:
                setattr(message, attr, request_data[attr])

            db.session.add(message)
            db.session.commit()

            return jsonify(message.to_dict()), 200  
        
        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Message deleted"
            }

            return make_response(response_body, 200)
        

if __name__ == '__main__':
    app.run(port=5555)
