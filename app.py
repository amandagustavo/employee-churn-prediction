from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import traceback

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    logger.info(f'Request: {request.method} {request.url}')
    logger.info(f'Response Status: {response.status}')
    return response

@app.route('/')
def home():
    logger.info('Accessing home page')
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test():
    try:
        logger.info('Testing server connection')
        return jsonify({'status': 'ok', 'message': 'Server is running'})
    except Exception as e:
        logger.error(f"Error in server test: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'error': 'Lỗi kết nối máy chủ. Vui lòng thử lại sau.'
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        logger.info('Received prediction request')
        
        if not request.is_json:
            raise ValueError("Dữ liệu gửi lên phải ở định dạng JSON")
            
        data = request.get_json()
        if not data:
            raise ValueError("Không nhận được dữ liệu")
            
        logger.info(f"Received data: {data}")
        
        # Kiểm tra các trường dữ liệu bắt buộc
        required_fields = ['Age', 'Gender', 'Years_at_Company', 'Job_Role', 'Monthly_Income']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise ValueError(f"Thiếu các trường dữ liệu: {', '.join(missing_fields)}")
        
        # Temporary response for testing
        test_response = {
            'predictions': {
                'Logistic Regression': 0.3,
                'Decision Tree': 0.4
            },
            'best_model': {
                'name': 'Logistic Regression',
                'probability': 0.3
            }
        }
        logger.info('Sending test response')
        return jsonify(test_response)
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}", exc_info=True)
        error_details = traceback.format_exc()
        logger.error(f"Error details:\n{error_details}")
        return jsonify({
            'error': 'Có lỗi xảy ra khi xử lý dự đoán. Vui lòng thử lại sau.',
            'details': str(e) if app.debug else None
        }), 500

if __name__ == '__main__':
    logger.info('Starting Flask server...')
    try:
        app.run(host='0.0.0.0', port=8000, debug=True)
    except Exception as e:
        logger.error(f"Server startup error: {str(e)}", exc_info=True)