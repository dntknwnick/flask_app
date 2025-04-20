import random
import time
from datetime import datetime, timedelta
from flask import current_app

# In a real application, use Redis or a database to store OTPs
# For this example, we'll use an in-memory dictionary
otp_store = {}

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp(mobile_number, otp):
    """
    Send OTP to the user's mobile number
    In a real application, this would integrate with an SMS gateway
    """
    # Mock implementation - in a real app, send SMS
    print(f"Sending OTP {otp} to {mobile_number}")
    
    # Store OTP with expiry time
    expiry = datetime.now() + timedelta(minutes=current_app.config['OTP_EXPIRY_MINUTES'])
    otp_store[mobile_number] = {
        'otp': otp,
        'expiry': expiry
    }
    
    return True

def verify_otp(mobile_number, otp):
    """Verify if the provided OTP is valid"""
    if mobile_number not in otp_store:
        return False
    
    stored_data = otp_store[mobile_number]
    
    # Check if OTP has expired
    if datetime.now() > stored_data['expiry']:
        # Clean up expired OTP
        del otp_store[mobile_number]
        return False
    
    # Check if OTP matches
    if stored_data['otp'] != otp:
        return False
    
    # OTP is valid, clean up
    del otp_store[mobile_number]
    return True
