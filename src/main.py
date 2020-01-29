"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Request, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
import requests
from models import User, Motor, Test
import copy
from sqlalchemy import desc
import random
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)




## SACAN  ID-MOTOR

def scanIDMotor():
    
    return("FKI000" + str(random.randrange(2,92)))



## STATUS GOOD-BAD
def validarStatus(test, NoTest):
    flag = True
    if (NoTest == 0):
        for i in test:
        
            if int(i) < 50 or int(i) > 150:
                flag = False
                break
    
    if (NoTest == 1):
        for i in test:
        
            if int(i) < 5 or int(i) > 15:
                flag = False
                break

    if flag:
        return "GOOD" 
    else:
        return "BAD"    


## SIMULAR RANDOM GOOD-BAD
def ranDOM():
    tempCorriente = []
    tempVoltaje = []
    tempRuido = []
    tempVibracion = []
    stCorriente =""
    stVoltaje = ""
    stRuido = ""
    stVibracion = ""
    
    statusNumber = random.randrange(0,2)
    if statusNumber == 0:
        status = 'GOOD' 
    else:
        status = 'BAD'

    
    
    if status is "GOOD":
    
        for i in range(0, 10):
            # tmpRandom = random.randrange(5)
            tempCorriente.append(str(random.randrange(50,150)))
    
        for i in range(0, 10):
            # tmpRandom = random.randrange(5)
            tempVoltaje.append(str(random.randrange(5,15)))

        for i in range(0, 10):
            # tmpRandom = random.randrange(5)
            tempRuido.append(str(random.randrange(5,15)))
    
        for i in range(0, 10):
            # tmpRandom = random.randrange(5)
            tempVibracion.append(str(random.randrange(5,15)))

    else:

        for i in range(0, 10):
            # tmpRandom = random.randrange(5)
            tempCorriente.append(str(random.randrange(2, 200)))
    
        for i in range(0, 10):
            # tmpRandom = random.randrange(5)
            tempVoltaje.append(str(random.randrange(2,200)))

        for i in range(0, 10):
            # tmpRandom = random.randrange(5)
            tempRuido.append(str(random.randrange(2,200)))
    
        for i in range(0, 10):
            # tmpRandom = random.randrange(5)
            tempVibracion.append(str(random.randrange(2,200)))


    
    statusCorriente = validarStatus(tempCorriente, 0)
    statusVoltaje = validarStatus(tempVoltaje, 1)
    statusRuido = validarStatus(tempRuido, 1)
    statusVibracion = validarStatus(tempVibracion, 1)

    
    stCorriente = ','.join(tempCorriente)
    stVoltaje = ','.join(tempVoltaje)
    stRuido = ','.join(tempRuido)
    stVibracion = ','.join(tempVibracion)       


    return tempCorriente, tempVoltaje, tempVibracion, tempVoltaje, status, stCorriente, stVoltaje, stRuido, stVibracion, status, statusCorriente, statusVoltaje, statusRuido, statusVibracion           

    

## PROCESAR DATA
def procesarData(corriente, voltaje, ruido, vibracion):
    statusCorriente = "GOOD"
    statusVoltaje = "GOOD"
    statusRuido = "GOOD"
    statusVibracion = "GOOD"

    if corriente:
        for c in corriente:
            if c < 50 and c > 150:
                statusCorriente =  "BAD"
                break

    if voltaje:
        for c in voltaje:
            if c < 5 and c > 15:
                statusVoltaje = "BAD"
                break

    if ruido:
        for c in ruido:
            if c < 5 and c > 15:
                statusRuido = "BAD"
                break
    if vibracion:
        for c in vibracion:
            if c < 5 and c > 15:
                statusVibracion = "BAD"
                break
 
    if statusCorriente is "GOOD" and statusVoltaje is "GOOD" and statusRuido is "GOOD" and statusVibracion is "GOOD": 
        return True 
    else: 
        return False


#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

# GET Motor
@app.route('/motor', methods=['GET'])
def handle_motor():

        motorsTemp = Motor()

        # get all the people
        motors_query = motorsTemp.query.all()

        # get only the ones named "Joe"
        # receta_query = recetasTemp.query.filter_by(name='pollo')
        # map the results and your list of people its now inside all_people variable
        all_motors = list(map(lambda x: x.serializeMotors(), motors_query))

        return jsonify(all_motors), 200


# GET Test
@app.route('/tests', methods=['GET'])
def handle_tests():

        testsTemp = Test()

        # get all the people
        tests_query = testsTemp.query.all()


        # get only the ones named "Joe"
        # receta_query = recetasTemp.query.filter_by(name='pollo')
        # map the results and your list of people its now inside all_people variable
        all_tests = list(map(lambda x: x.serializeTests(), tests_query))

        return jsonify(all_tests), 200

# GET Test
@app.route('/users', methods=['GET'])
def handle_users():

        usersTemp = User()

        # get all the people
        users_query = usersTemp.query.all()
        

        # get only the ones named "Joe"
        # receta_query = recetasTemp.query.filter_by(name='pollo')
        # map the results and your list of people its now inside all_people variable
        all_Users = list(map(lambda x: x.serializeUsers(), users_query))

        return jsonify(all_Users), 200

##MOTOR  GET ID
@app.route('/motorId/<id>', methods=['GET'])
def handle_motorId(id):

        motoridTemp = Motor()

        # get all the people
        motorId_query = motoridTemp.query.filter_by(serial=id)
        # User.query.limit(1).all()
        # get only the ones named "Joe"
        # receta_query = recetasTemp.query.filter_by(name='pollo')
        # map the results and your list of people its now inside all_people variable
        # all_ingrediente = list(map(lambda x: x.serializeContact(), contacts_query))
        all_motor = list(map(lambda x: x.serializeMotors(), motorId_query))

        # return arrIngrediente

        return jsonify(all_motor), 200


##TEST  GET LAST ID
@app.route('/testIdLast/', methods=['GET'])
def handle_testIdLast():

        testidTemp = Test()
        testMotor = Motor()

        # get all the people
        testId_query = testidTemp.query.order_by(desc(Test.id)).first()
        
        testMotor_query = testMotor.query.filter_by(id=testId_query.motor_id).first()
        print(testMotor_query)
        # User.query.limit(1).all()
        # get only the ones named "Joe"
        # receta_query = recetasTemp.query.filter_by(name='pollo')
        # map the results and your list of people its now inside all_people variable
        # all_ingrediente = list(map(lambda x: x.serializeContact(), contacts_query))
        # all_test = list(map(lambda x: x.serializeTests(), testId_query))
        all_test = testId_query.serializeTests()
        all_motor = testMotor_query.serializeMotors()

        # return arrIngrediente

        return jsonify(all_test, all_motor), 200


# ADD TEST NEW

@app.route('/add_testNew', methods=['POST'])
def add_testNew():
    
    
    # statusNew = "GOOD"
    # statusNew = "BAD"
    tempMotor = None
    body = request.get_json()
    
    tempMotorNew = scanIDMotor()
    # tempMotor = db.session.query(Motor).filter(Motor.serial == body["motor_id"]).first()
    tempMotor = db.session.query(Motor).filter(Motor.serial == tempMotorNew).first()
    tempUser = db.session.query(User).filter(User.username == body["user_id"]).first()
    
    tempVariables = ranDOM()


    # test1 = Test(voltaje=body["voltaje"], corriente=body["corriente"], ruido=body["ruido"], vibracion=body["vibracion"], motor_id=body["motor_id"], user_id=tempUser.id, status=body["status"])
    test1 = Test(voltaje=tempVariables[6], corriente=tempVariables[5], ruido=tempVariables[7], vibracion=tempVariables[8], motor_id=tempMotor, user_id=tempUser.id, 
    status=tempVariables[9], statusCorriente=tempVariables[10], statusVoltaje=tempVariables[11], statusRuido=tempVariables[12], statusVibracion=tempVariables[13])
    
    if tempMotor is None:

        motorSerial = Motor(serial=tempMotorNew, status=0)   
        motorSerial.test.append(test1)   
        db.session.add(motorSerial)
    else:
        #test1 = Test(voltaje=body["voltaje"], corriente=body["corriente"], ruido=body["ruido"], vibracion=body["vibracion"], motor_id=tempMotor.id, user_id=tempUser.id, status=body["status"])
        test1 = Test(voltaje=tempVariables[6], corriente=tempVariables[5], ruido=tempVariables[7], vibracion=tempVariables[8], motor_id=tempMotor.id, user_id=tempUser.id, 
        status=tempVariables[9], statusCorriente=tempVariables[10], statusVoltaje=tempVariables[11], statusRuido=tempVariables[12], statusVibracion=tempVariables[13])
        db.session.add(test1)
    db.session.commit()
    return "ok", 200


# ADD Test
@app.route('/add_test', methods=['POST'])
def add_test():
    tempMotor = None
    body = request.get_json()
    
    
    tempMotor = db.session.query(Motor).filter(Motor.serial == body["motor_id"]).first()
    tempUser = db.session.query(User).filter(User.username == body["user_id"]).first()
    
    test1 = Test(voltaje=body["voltaje"], corriente=body["corriente"], ruido=body["ruido"], vibracion=body["vibracion"], motor_id=body["motor_id"], user_id=tempUser.id, status=body["status"])
    if tempMotor is None:

        motorSerial = Motor(serial=body["motor_id"], status=0)   
        motorSerial.test.append(test1)   
        db.session.add(motorSerial)
    else:
        test1 = Test(voltaje=body["voltaje"], corriente=body["corriente"], ruido=body["ruido"], vibracion=body["vibracion"], motor_id=tempMotor.id, user_id=tempUser.id, status=body["status"])
        db.session.add(test1)
    print(test1)
    db.session.commit()
    return "ok", 200


# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


@app.route('/login', methods=['POST'])
def login():

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    usercheck = User.query.filter_by(email=email, password=password).first()
    if usercheck == None:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=email),'id': usercheck.id, 'name': usercheck.username}
    return jsonify(ret), 200    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
