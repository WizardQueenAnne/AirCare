from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configure Flask
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'school']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Extract form data
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone', '')
        school = data.get('school')
        message = data.get('message', '')
        
        # Log the submission (in production, save to database or send email)
        print(f"""
        New Contact Form Submission:
        ----------------------------
        Name: {name}
        Email: {email}
        Phone: {phone}
        School: {school}
        Message: {message}
        """)
        
        # In production, you would:
        # 1. Save to database
        # 2. Send confirmation email to customer
        # 3. Send notification email to sales team
        # 4. Add to CRM system
        
        # Example email sending (uncomment and configure for production):
        """
        from flask_mail import Mail, Message
        
        msg = Message('New AirCare Demo Request',
                      sender='noreply@aircare.com',
                      recipients=['sales@aircare.com'])
        msg.body = f'''
        New demo request from {name}
        
        Email: {email}
        Phone: {phone}
        School: {school}
        Message: {message}
        '''
        mail.send(msg)
        """
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your interest! We will contact you shortly.'
        }), 200
        
    except Exception as e:
        print(f"Error processing contact form: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again later.'
        }), 500

@app.route('/api/pricing', methods=['GET'])
def pricing():
    """Return pricing information"""
    pricing_data = {
        'starter': {
            'name': 'Starter',
            'price': 199,
            'description': 'Perfect for small schools',
            'features': [
                'Real-time vape detection',
                'Air quality monitoring',
                'Email & SMS alerts',
                'Basic reporting',
                '1-year warranty'
            ]
        },
        'professional': {
            'name': 'Professional',
            'price': 299,
            'description': 'For growing campuses',
            'features': [
                'Everything in Starter',
                'Advanced analytics',
                'Custom alert rules',
                'Priority support',
                '3-year warranty',
                'Free training'
            ],
            'popular': True
        },
        'enterprise': {
            'name': 'Enterprise',
            'price': 'Custom',
            'description': 'For large districts',
            'features': [
                'Everything in Professional',
                'Volume discounts',
                'Dedicated account manager',
                'Custom integrations',
                'On-site training',
                '5-year warranty'
            ]
        }
    }
    
    return jsonify(pricing_data), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Run the app
    # In production, use a proper WSGI server like gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)
