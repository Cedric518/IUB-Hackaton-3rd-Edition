import os
from dotenv import load_dotenv
import google.generativeai as genai
from DatabaseManager import DatabaseManager
from geminichat import ChatModel
from flask import Flask, request, jsonify, g
from flask_cors import CORS

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # Load environment variables
    load_dotenv()
    INSTRUCTION = os.getenv("INSTRUCTION")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    CHATBOT_VERSION = os.getenv('CHATBOT_VERSION')
    
    # Initialize chat_bot and database manager
    app.config['chat_bot'] = ChatModel(CHATBOT_VERSION, GEMINI_API_KEY, INSTRUCTION)
        

    def get_db():
        if 'db' not in g:
            g.db = DatabaseManager(DATABASE_NAME)
        return g.db
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    



    @app.route('/chat', methods=['POST'])
    def process_message():
        try:
            # Get data from request
            data = request.json

            if not data:
                return jsonify({
                    'status': 'error',
                    'message': 'No JSON data received'
                }), 400
        
            user_input = data.get('message')

            if not user_input:
                return jsonify({
                    'status': 'error',
                    'message': 'No message found in request'
                }), 400
            
            manager = get_db()
            model_response = app.config['chat_bot'].send_message(user_input)

            # Extract parameters
            query = model_response['sql']
            parameters = model_response['parameters']
            action = model_response['action']
            value = model_response['value']

            # Process database action
            result = None
            if action == 'INSERT':
                result = manager.push_data(query, parameters)
                current_data = manager.show_data()
                return jsonify({
                    'status': 'success',
                    'action': action,
                    'result': result,
                    'current_data': current_data
                })
                
            elif action == 'UPDATE':
                result = manager.update_data(query, parameters)
                current_data = manager.show_data()
                return jsonify({
                    'status': 'success',
                    'action': action,
                    'result': result,
                    'current_data': current_data
                })
                
            elif action == 'SELECT':
                result = manager.select_data(query, parameters)
                return jsonify({
                    'status': 'success',
                    'action': action,
                    'result': result
                })
                
            elif action == 'DELETE':
                result = manager.delete_data(query, parameters)
                current_data = manager.show_data()
                return jsonify({
                    'status': 'success',
                    'action': action,
                    'result': result,
                    'current_data': current_data
                })
                
            elif action == 'DELETE_ALL':
                result = manager.delete_all(query)
                return jsonify({
                    'status': 'success',
                    'action': action,
                    'result': result,
                    'message': 'All records deleted'
                })
                
            elif action == 'CLOSE':
                manager.close()
                return jsonify({
                    'status': 'success',
                    'action': action,
                    'result': result,
                    'message': 'Database connection closed'
                })
            
            else:
                return jsonify({
                    'status': 'error',
                    'message': f'Unknown action: {action}'
                }), 400

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500



    return app

def main():
    app = create_app()
    print("Starting Flask server...")
    app.run(debug=True)

if __name__ == '__main__':
    main()