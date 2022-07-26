from xml.etree import ElementTree
import requests
import xmltodict, json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def get_number(image_path):
    # This function interacts with the platerecognizer api to perform plate recognition
    with open(image_path,'rb') as fp:
        response = requests.post( 
        'https://api.platerecognizer.com/v1/plate-reader/',
        files=dict(upload=fp),
        headers={'Authorization': 'Token d523ae59f0b621eee620ef10200800155167e15e'})
    results = response.json()
    global plate_number 
    plate_number = results['results'][0]['plate'] # the plate number we get after image recognition


def get_car_information(plate_number,user_name):
    # This function gets vehicle information from the regcheck api 
    url = "http://www.regcheck.org.uk/api/reg.asmx/CheckIndia?RegistrationNumber={plate_number}&username={user_name}".format(plate_number=plate_number,user_name=user_name)
    request_response = requests.get(url=url) # send api request
    root = ElementTree.fromstring(request_response.content) # parse xml 
    response = root[0].text
    global json_response
    json_response = json.loads(response) # converts json to python dictonary
    

def display_info_onimage(image_path):
    # This function displays text on the image
    img = Image.open(image_path)
    font = ImageFont.truetype("/Users/deeppatel/Downloads/times-ro.ttf", 20)
    text1 = "Number Plate: "+plate_number+"\n\nVehicle Type: "+json_response['VehicleType']+"\n\nBrand: "+json_response['Description'] +"\n\nEngine: "+json_response['EngineSize']['CurrentTextValue'] +"\n\nRegistration : "+json_response['RegistrationDate'] +"\n\nFuel Type: "+json_response['FuelType']['CurrentTextValue'] # This paragraph 1 on image
    text2 = "Insurance: "+json_response['Insurance']+"\n\nPUCC: "+json_response['PUCC']+"\n\nNumber of Seats: "+json_response['NumberOfSeats']['CurrentTextValue'] +"\n\nLocation: "+json_response['Location']+"\n\nOwner: "+json_response['Owner']+"\n\nFitness: "+json_response['Fitness'] # This is paragraph 2 on image
    image_editable = ImageDraw.Draw(img)
    image_editable.text((200,630),text1,font=font, fill =(50,205,50)) # places paragraph 1 on 200,300 on the image
    image_editable.text((600,630),text2,font=font, fill =(50,205,50)) # place paragraph 2 on 600,630 on the image
    img.save("finalCarImage.jpeg")

get_number("/Users/deeppatel/Desktop/DSA/Java/photo1.jpeg") # calls the image recognition api function; the url as parameter in this function is my internal computer link if you want to test it then change the link 
get_car_information(plate_number,"Deep160301")# calls the car_information fetching api function
display_info_onimage("/Users/deeppatel/Desktop/DSA/Java/photo1.jpeg") # calls the display function; the url as parameter in this function is my internal computer link if you want to test it then change the link 
