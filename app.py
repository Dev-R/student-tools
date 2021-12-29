# Importing the necessary Libraries
import os
import datetime
import uuid
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session,  url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import allowed_file, get_text_OCR, apology, login_required, get_image_path
from PIL import Image
from datetime import datetime

# Get Local time
LOCAL_TIMEZONE = (datetime.now()).strftime("%m-%d-%Y, %H:%M:%S")
# Set to the full path of the upload file in static
UPLOAD_FOLDER = '/app/static/uploads'
#  Set to the full path of the current Project Directory 
CURRENT_PROJECT_DIR = '/app'

# Configure application
app = Flask(__name__)
app.secret_key = 'A0AKR5TGD\ R~XHH!jmN]LWX/,?RT'
# app.config['SECRET_KEY'] = os.urandom(24)
# this is important or wont work
app.config['SESSION_COOKIE_NAME'] = "my_session"
# Configure Database
db = SQL(os.getenv("DATABASE_URL"))
# Membership types
MEMBER_SHIP = {'A': 'ADMIN', 'G': 'GUEST'}
# redis configuration 
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis = redis.from_url(redis_url)


"""Configure session to use filesystem (instead of signed cookies) and other app configuration"""
# The directory where session files are stored.
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# Whether use permanent session or not, default to be True
app.config["SESSION_PERMANENT"] = False
# Specifies which type of session interface to use.
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Configure uploading file
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Redirect to index
@app.route('/', methods=["GET", "POST"])
def redirect_homepage():
    return redirect('/index')

# Render index
@app.route('/index', methods=["GET", "POST"])
def homepage():
    return render_template('index.html')


# Redirect to index
@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template('about.html')

# Redirect to signup
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Sign Up User"""
    if request.method == "POST":
        # Get user info
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('confirmation')
        error = None
        # Check if username is valid and a string
        if not username or not isinstance(username, str):
            error = "Please enter a valid user name"
            
        # Check for password errors
        elif not password:
            error = "Please enter a valid password"
        
        # Check if password confirmation match
        elif password != password_confirm:
            error ="Password confirmation doesn't match"
        
        # TO-DO: password len > 10:

        # Check for matching username
        elif db.execute("SELECT * FROM users WHERE username = ?" , username):
            error = "Username taken"
            
        if error is None:
            # Add user to data base
            add_user_to_db(username, password)
            flash("Registered 😁")
            return render_template('index.html')
            
        flash(error)
        return render_template("signup.html")
        
        
    else:
        return render_template('signup.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    """Login User"""
    # Forget any user_id
    session.clear()
    if request.method == 'POST':
        # Get user info
        username = request.form.get('username')
        password = request.form.get('password')
        error = None
        # Ensure username was entered
        if not request.form.get('username'):
            error  = "must provide username"

        # Ensure password was entered
        elif not request.form.get('password'):
            error  = "must provide password"

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        # Check if username exist and password is correct in DB
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            error = 'Invalid credentials'
            
        if error is None:
           # Remember which user has logged in
           session["user_id"] = rows[0]["id"]
           return render_template('index.html', user=username)
          
        flash(error)
        return render_template("login.html")
        
    else:
        # Redirect to login page
        return render_template('login.html')


@app.route('/text_reader', methods=["GET", "POST"])
def text_reader():
    """Redirect User to text reader page"""
    if request.method == "POST":
        return render_template('text_reader.html')
        
    else:
        return render_template('text_reader.html')


@app.route('/ocr', methods=["GET", "POST"])
def ocr():
    if request.method == "POST":
        """Process image user uploaded"""
        error = None
        # Check if user uploaded a valid file
        if 'file' not in request.files:
            error ='No file part'
            flash(error)
            return render_template('ocr.html') 
    
        # Get user file and Store it
        file = request.files['file']
        # Check if filename is not malicious
        if file and allowed_file(file.filename):
            # Secure file name and return new file name
            filename = secure_filename(file.filename)
            # Generate a unique image name using UUID
            filename = str(uuid.uuid4())+".jpeg"
            # Store image in the UPLOAD_FOLDER dir
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Extract text in image using Microsoft ComputerVision SDK
        ocr_text = get_text_OCR(filename)
        
        # If the user is logged in, store the file in his db
        if session:
            remember_user_ocr_file(filename, ocr_text)
        # Render and display OCR result of the image
        return render_template('ocr_result.html', text=ocr_text, filename=filename)
    else:
        return render_template('ocr.html')


@app.route('/history', methods=['GET'])
@login_required
def history():
    """Display OCR Image History for the user"""
    if request.method == "GET":
        # Get user data in DB
        user_data = db.execute("SELECT * FROM ocr WHERE user_id = ?", session['user_id'])
        return render_template('history.html', user_data=user_data)


# TO-DO rate_limiter
""" 
@app.route('/reader', methods=["GET", "POST"])
def rate_limiter():
    if request.method == "POST":
        '''
        TO DO: Rate limiting, to Prevents web scraping/bots/spam users.
        '''
    else:
        return render_template('ocr.html')
"""


@app.route('/display/<filename>')
def display_image(filename):
    """Get Image and Display it"""
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


def remember_user_ocr_file(filename, ocr_text)-> None:
    """Remeber what image user uploaded for History"""
    db.execute("INSERT INTO ocr (user_id, img_dir, img_text, execution_date) VALUES(?, ?, ?, ?)", session['user_id'], 
               get_image_path(filename).replace(CURRENT_PROJECT_DIR, ""), ocr_text, str(LOCAL_TIMEZONE))
    

def errorhandler(error):
    """Handle error"""
    if not isinstance(error, HTTPException):
        error = InternalServerError()
        error = str(error.name) + str(error.code)
    if error:
        
        error = 'Please Try again, Error: ' + str(error.code) + ' Reported' 
        flash(error)
        # TO-DO: Create an Error table in database to keep track of user errors
        return render_template('index.html')


def add_user_to_db(username, password) -> None:
    """Add user to database"""
    db.execute("INSERT INTO users (username, hash, member_ship,registration_date) VALUES(?, ?, ?, ?)", username, generate_password_hash(password), MEMBER_SHIP['A'], 
               str(LOCAL_TIMEZONE))
    
# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
 port = int(os.environ.get("PORT", 8080))
 app.run(host="0.0.0.0", port=port)
