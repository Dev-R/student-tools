from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import os
import requests
import urllib.parse
from flask import redirect, render_template, request, session
from functools import wraps
from array import array
import os
from PIL import Image
import sys
import time

'''
ENVIRONMENT VARIBLES AND CONSTANTS
'''
# OCR Free 
subscription_key = "a196a1cf6f1c44068ef32af48fff4575"
endpoint = "https://ocrfreecs50.cognitiveservices.azure.com/"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



'''
***************************************************************************************/
*    Title: Azure Read API
*    Author: Microsoft
*    Date: 2021
*    Code version: N/A
*    Availability: https://github.com/Azure-Samples/cognitive-services-quickstart-code
*    
***************************************************************************************/
'''
""""""
def get_text_OCR(image_name):
    '''
    Parameter: Image name
    Return: Text in image
    OCR: Read File using the Read API, extract text - remote
    This example will extract text in an image, then print results, line by line.
    This API call can also extract handwriting style text (not shown).
    '''
    # Get image path
    read_image_path = get_image_path(image_name)
    # Open the image
    read_image = open(read_image_path, "rb")
    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(read_image, raw=True)
    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]
    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
    #print ('Waiting for result...')
    time.sleep(10)
    # Print the detected text, line by line
    str = ""
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                str += line.text
    if str is None:
        return("Image is Low Quality or unsupported")
    return str
    
    
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code



def allowed_file(filename):
    '''Ensure user uploaded a valid file'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# TO-DO: Compress image > 6 MB
"""
def compress_image(img_name):
    '''Reduce image size uploaded by user'''
    # Get image path
    read_image_path = get_image_path(img_name)
    # Open the image
    basewidth = 300
    img = Image.open(read_image_path)
    # print(os.stat(image_name)).st_size
    # wpercent = (basewidth/float(img.size[0]))
    # hsize = int((float(img.size[1])*float(wpercent)) * 4) 
    # Reduce  image to 1/2 of the size
    img = img.resize((int(img.size[0]/2),int(img.size[1]/2)), 0) 
    img.save(img_name.replace('.', '-compressed.'))
"""


def get_image_path(img_name) -> str:
    """Find an image path in system and return it"""
    # Get image directory 
    images_dir = os.path.join (os.path.dirname(os.path.abspath(__file__)), "static/uploads")
    # Get image path
    image_path = os.path.join (images_dir, img_name)
    # Return image path
    return image_path

