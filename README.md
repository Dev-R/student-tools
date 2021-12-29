# CS50 Final Project - StudentTools 👨‍🎓📚
*StudentTools* is a web app using Flask and Bootstrap where students can find all of the tools they need to succeed.

# Features
- [Microsoft Cognitive Services Speech SDK](https://github.com/microsoft/cognitive-services-speech-sdk-js)
- [Microsoft Cognitive Services Computer Vision SDK](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cognitiveservices/azure-cognitiveservices-vision-computervision)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Bootstrap](https://getbootstrap.com/)
- [SQlite3](https://www.sqlite.org/index.html)
- [SQLAlchemy](https://www.sqlalchemy.org/)

# Prerequsites 📃

## Dependancies
The following dependancies are required
- flask 
- flask_session
- azure.cognitiveservices.vision.computervision
- azure.cognitiveservices.vision.computervision.models
- msrest.authentication 
- werkzeug.exceptions
- werkzeug.security
- werkzeug.utils
- uuid
- tempfile
- functools 
- PIL
- requests
- cs50
## Set up

### Change Directory in app.py
python
# Set to the full path of the upload file in static
UPLOAD_FOLDER = '/home/ubuntu/project/static/uploads'
#  Set to the full path of the current Project Directory 
CURRENT_PROJECT_DIR = '/home/ubuntu/project'

### Add Microsoft Computer Vision Token and Endpoint in helpers.py
python
subscription_key = "ENTER YOUR MICROSOFT COMPUTER VISION KEY"
endpoint = "ENTER YOUR MICROSOFT COMPUTER VISION ENDPOINT"

### Add Microsoft Text To Speech Token in SpeechSDK.js 
javascript
subscriptionKey = 'ENTER YOUR MICROSOFT TTS subscriptionKey';
serviceRegion = 'ENTER YOUR MICROSOFT TTS REGION';

### Set up Environment 

export FLASK_APP=app.py

### Run the App
 
flask run

### Access Database

sqlite3 site.db 
.schema

# Project Explaination
## Project Background
The project main idea is to provide a site where students can find all of the tools they need, in such a way
they don't need to visit more than one site for different tools. 
- The students(users) can use *OCR(Optical character recognition)*
to extract text from *images or there hand written notes* 
- The students(users) can *converts text to lifelike speech* using Microsoft Azure TTS SDK
- The students(users) can login and *save and check their upload history*.

# Demonstration
## Main Page
- ![Index](https://github.com/Dev-R/StudentTools/blob/main/show_off/index.gif?raw=true)

## Responsivity
- ![Index](https://github.com/Dev-R/StudentTools/blob/main/show_off/responsive.gif?raw=true)

## History and Signup

| History | Signup |
| :---: | :---: | 
| <img src="show_off/history.gif" width="400"> | <img src="show_off/signup.gif" width = "400">

## Login and Validation

| Login | Validation |
| :---: | :---: | 
| <img src="show_off/login.gif" width="400"> | <img src="show_off/credentials.gif" width = "400">

## Live Demonstration

## Anatomy

### Backend
- Used Flask Framework to run the back end
- Used Azure Microsoft Cognitive Services Computer Vision SDK to process images
### Security
- Use POST request to send data to the server as it is more secure then GET
- Encrypt user password using SHA256 hash function 
![Encrypted Password](https://i.ibb.co/3MLw6vC/A.png)
Where hash is the Encrypted password
- Use UUID to change image name to new secure name
### Database
- The Database use SQlite3 and SQLAlchemy for queries. It is used to stores user credentials and students OCR upload History.
  there are mainly two tables, Users and OCR
- Users Table
 - ![Users Table](https://i.ibb.co/wYqS68C/A.png)

Stores user information such as username, hashed password, membership and their registration date
- OCR Table
 - ![OCR Table](https://i.ibb.co/n8X5H6c/B.png)

Stores  images, text extracted from images, and the execution time
### Sessions
The Webapp use sessions to confirm user identity. Furthemore, it use filesystem sessions and it creates a unique sessions id for each user and store it in the system uniquely using  mkdtemp().
python
# The directory where session files are stored.
app.config["SESSION_FILE_DIR"] = mkdtemp()
# Whether use permanent session or not, default to be True
app.config["SESSION_PERMANENT"] = False
# Specifies which type of session interface to use.
app.config["SESSION_TYPE"] = "filesystem"


## Possible improvements 📃
*Ability to*:
- Change account details
- Delete uploaded files
- Email verification
- Store server errors in a DB
- User profile
- Further tools such as file converters etc.
