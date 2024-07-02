from random import randint
from faker import Faker
import random
import phonenumbers
from datetime import datetime, timedelta



# Local imports
from app import app  # Import Flask app 
from model import db, User

def generate_valid_phone_number():
    kenya_country_code = '+254'
    while True:
        national_number = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        phone_number = f'{kenya_country_code}{national_number}'
        
        # Ensure that the phone number is valid
        try:
            # Parse the phone number
            parsed_number = phonenumbers.parse(phone_number, None)
            
            # Check if the parsed number is valid
            if phonenumbers.is_valid_number(parsed_number):
                return phone_number
        except phonenumbers.phonenumberutil.NumberParseException:
            pass

if __name__ == '__main__':
    fake = Faker()

    # Initialize Flask app context
    with app.app_context():
        print("Starting seed...")
        
        # Clear existing data (optional)
        db.drop_all()
        db.create_all()

        # Create admin
        admin = User(
            username='admin',
            email='admin@gmail.com',
            password='@Admin1',
            phone_number='+254706318757',
            role='admin' 
        )
        db.session.add(admin)
        db.session.commit()

        # Create user Dan
        dan = User(
            username='dan',
            email='danspmunene@gmail.com',
            password='dan',
            phone_number='+254706318757',
            role='tutor' 
        )
        db.session.add(dan)
        db.session.commit()

        # Seed data
        for _ in range(10):
            # Create users
            phone_number = generate_valid_phone_number()
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                phone_number=phone_number,
                role='tutor' if randint(0, 1) else 'learner'
            )
            db.session.add(user)
            db.session.commit()

        print("Seed complete!")