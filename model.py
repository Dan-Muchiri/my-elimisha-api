from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
import re
import phonenumbers


# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt()


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(100), nullable=True)
    _password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String(20), nullable=False)

    # Define relationship
    

    def __repr__(self):
        return f'<User {self.username} | Email: {self.email}>'
    
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username is required')
        if len(username) > 50:
            raise ValueError('Username must be less than 50 characters')
        return username
    
    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError('Email is required')
        
        # Check email format using regular expression
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError('Invalid email format')

        return email
    

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number:
            raise ValueError('Phone number is required')

        try:
            # Parse the phone number
            parsed_number = phonenumbers.parse(phone_number, None)

            # Get the country code from the parsed number
            country_code = phonenumbers.region_code_for_country_code(parsed_number.country_code)
            
            # Re-parse the phone number with the detected country code
            parsed_number = phonenumbers.parse(phone_number, country_code)

            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError('Invalid phone number')
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError('Invalid phone number format. Should be:"+254123456789"')

        return phone_number
    
    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password_hash, plaintext_password)