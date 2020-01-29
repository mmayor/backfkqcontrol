from flask_sqlalchemy import SQLAlchemy
import os, sys, enum
from sqlalchemy import func


from datetime import datetime, timezone



db = SQLAlchemy()

# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<Person %r>' % self.username

#     def serialize(self):
#         return {
#             "username": self.username,
#             "email": self.email
#         }

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    dpto = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="profile")
    # recetas = db.relationship("Receta", back_populates="autor")

    def __repr__(self):
         return '<Profile %r>' % self.id


    def serializeProfiles(self):
            return {
             "id": self.id,
             "dpto": self.dpto,
             "status": self.status,
             "nivel": self.nivel,
             "user_id": self.user_id
            }
            


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(25), unique=False, nullable=False)
    profile = db.relationship("Profile", uselist=False, back_populates="user")
    test = db.relationship('Test', lazy=True)
    

    def __repr__(self):
         return '<User %r>' % self.username

    def serializeUsers(self):
        return {
            "id":self.id,
            "username": self.username,
            "email": self.email,
            # "profile":   (lambda x: x.serializeProfiles(), self.profile)
          #  "profile": self.profile.serializeProfiles()
           # "testTemp": list(map(lambda x: x.serializeTests(), self.test)),
}  

class Dpto(db.Model):
    __tablename__ = 'dpto'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
         return '<User %r>' % self.name


class Motor(db.Model):
      __tablename__ = 'motor'   
      id = db.Column(db.Integer, primary_key=True)
      serial = db.Column(db.String(80), unique=True, nullable=False)  
      status = db.Column(db.Boolean, unique=False, nullable=False)
      test = db.relationship('Test', lazy=True)

      def __repr__(self):
         return '<User %r>' % self.serial

      def serializeMotors(self):
        return {
            "id":self.id,
            "serial": self.serial,
            "status": self.status,
            # "profile":   (lambda x: x.serializeProfiles(), self.profile)
            "testTemp": list(map(lambda x: x.serializeTests(), self.test)),
        }




class Test(db.Model):
      
      

      __tablename__ = 'test'  
      id = db.Column(db.Integer, primary_key=True)
      voltaje = db.Column(db.String(60), unique=False, nullable=False) 
      corriente = db.Column(db.String(60), unique=False, nullable=False) 
      ruido = db.Column(db.String(60), unique=False, nullable=False) 
      vibracion = db.Column(db.String(60), unique=False, nullable=False)
      status = db.Column(db.String(6), unique=False, nullable=False) 
      statusCorriente = db.Column(db.String(6), unique=False, nullable=False) 
      statusVoltaje = db.Column(db.String(6), unique=False, nullable=False) 
      statusRuido = db.Column(db.String(6), unique=False, nullable=False) 
      statusVibracion = db.Column(db.String(6), unique=False, nullable=False) 
      motor_id = db.Column(db.Integer, db.ForeignKey("motor.id"))
      user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
      dateNew = db.Column(db.TIMESTAMP,  nullable=False)
      user = db.relationship("User", uselist=False)

      
      
      def __repr__(self):
         return '<User %r>' % self.id

      def serializeTests(self):
            return {
             "id": self.id,
             "voltaje": self.voltaje,
             "corriente": self.corriente,
             "ruido": self.ruido,
             "vibracion": self.vibracion,
             "status": self.status,
             "statusCorriente": self.statusCorriente,
             "statusVoltaje": self.statusVoltaje,
             "statusRuido": self.statusRuido,
             "statusVibracion": self.statusVibracion,
             "motor_id": self.motor_id,
             "user_id": self.user_id,
             "user": self.user.serializeUsers(),
             "dateNew": self.dateNew
             
            }   







