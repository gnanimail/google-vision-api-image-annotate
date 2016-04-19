#!/usr/bin/env python
"""
Uses the Google Cloud Vision API to determine what entities are found within the image.
As a further step, annotates the image itself with a parsed version of the API response.

"""

import argparse
import base64
import csv
import httplib2
import datetime
import json
import os
from PIL import Image, ImageDraw, ImageFont
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials


# Globals
timestamp = str(datetime.datetime.now())  # Use timestamp to store data in unique filenames
json_file_name = "output data/" + timestamp + "-vision-api-output.json"
csv_file_name = "output data/" + timestamp + "-vision-api-output.csv"


def process_images(image_input):
    """Determines whether to run the API on a single image or a directory of images """
    image_exts = ['.bmp', '.gif', '.jpg', '.jpeg', '.png']
    ignore_files = ['.DS_Store']  # For Mac OS X 

    # Check if folder
    if image_input[-1] == "/":
        dir_name = image_input

        for file_name in os.listdir(dir_name):
            ext = os.path.splitext(file_name)
        
            if file_name not in ignore_files and ext[1].lower() in image_exts and not os.path.isdir(file_name):
                print(file_name)
                resp = main(dir_name + file_name)
                parse_response(dir_name + file_name, resp)
    else:
        print(image_input)
        resp = main(image_input)
        parse_response(image_input, resp)


def store_json(json_input):
    """Log the full JSON response"""
    with open(json_file_name, "a") as f:
        f.write(json_input + '\n')


def store_csv(csv_input):
    """Log the full data in CSV form"""
    with open(csv_file_name, 'a') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        try:
            csv_writer.writerow(csv_input)
        except UnicodeEncodeError:  # TODO: handle unicode OR just run with Python 3 :)
            csv_writer.writerow(["ERROR"])


def image_annotate(image_input, text=""):
    """Uses PIL library to annotate the image with response data"""
    
    img = Image.open(image_input)
    img_size = img.size
    add_height = 15 * len(text.split('\n'))  # 15 px is a rough estimation of each line
    add_width = 0  # TODO

    new_img = Image.new('RGBA', (img_size[0] + 300, img_size[1] + add_height), color=128)  # New image where old will be copied
    # DONE: fix 'P and 'RGBA' modes
    
    # font = ImageFont.load_default()  # DONE: use better font
    # font = ImageFont.truetype("fonts/UbuntuMono-Regular.ttf", 16)  # Defined font size
    font = ImageFont.truetype("fonts/DroidSansMono.ttf", 14)  # Switched to DroidSansMono

    draw = ImageDraw.Draw(new_img)
    draw.multiline_text((img_size[0] + 10, 10), text, fill=(0,0,255), font=font)  # multiline_text supported in PIL 3.2.x

    # Save in "images output/"
    img_path = image_input.split("/")
    img_name = img_path[len(img_path) - 1]
    img_name_png = img_name.rsplit(".")[0] + ".png"

    new_img.paste(img, (0, 0))
    new_img.save("images-output/" + img_name_png)


def main(photo_file):
    """Run a request on a single image"""

    API_DISCOVERY_FILE = 'https://vision.googleapis.com/$discovery/rest?version=v1'
    http = httplib2.Http()

    credentials = GoogleCredentials.get_application_default().create_scoped(
            ['https://www.googleapis.com/auth/cloud-platform'])
    credentials.authorize(http)

    service = build('vision', 'v1', http, discoveryServiceUrl=API_DISCOVERY_FILE)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(
                body={
                    'requests': [{
                        'image': {
                            'content': image_content
                        },
                        'features': [{
                            'type': 'LABEL_DETECTION',
                            'maxResults': 20,
                        },
                            {
                            'type': 'TEXT_DETECTION',
                            'maxResults': 20,
                            }]
                    }]
                })
    response = service_request.execute()

    return response


def parse_response(photo_file, response):
    """ Parse response into relevant fields"""
    response = response
    query = photo_file
    all_labels = ''
    all_text = ''
    img_labels = '**Labels Found: \n'  # For image annotation
    img_text = '**Text Found: \n'  # For image annotation

    try:
        labels = response['responses'][0]['labelAnnotations']
        for label in labels:
            label_val = label['description']
            score = str(label['score'])
            print('Found label: "%s" with score %s' % (label_val, score))

            all_labels += label_val.encode('utf-8') + ' @ ' + score + ', '
            img_labels += label_val.encode('utf-8') + ' @ ' + score + '\n'
    except KeyError:
        print("N/A labels found")

    print('\n')

    try:
        texts = response['responses'][0]['textAnnotations']
        for text in texts:
            text_val = text['description']
            print('Found text: "%s"' % text_val)

            all_text += text_val.encode('utf-8') + ', '
            img_text += text_val.encode('utf-8') + '\n'
    except KeyError:
        print("N/A text found")
        img_text += "\nN/A text found"

    print('\n= = = = = Image Processed = = = = =\n')

    # Response parsing 
    response["query"] = photo_file
    csv_response = [query, all_labels, all_text]

    response = json.dumps(response, indent=3)
    store_json(response)
    store_csv(csv_response)

    image_annotate(photo_file, img_labels + '\n' + img_text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_input', help='The folder containing images or the image you\'d like to query')
    args = parser.parse_args()
    process_images(args.image_input)
