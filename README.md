# google-vision-api

This repository includes code originally written during the [Archives Unleashed Hackathon](https://artsweb.uwaterloo.ca/archivesunleashed/) (March 3-5, 2016). 

The "google-vision-api.py" and "google-vision-api-image-annotate.py" are command-line tools to work with the Vision API. 

The latter script creates images that are annotated with the responses from the Google Cloud Vision API. This helps you see what entities and texts (among many other features) were found by the API in one glance.

```
$ python google-vision-api.py [image or path/to/folder]

$ python google-vision-api-image-annotate.py [image or path/to/folder]
```

## Google Cloud Vision API

The [Google Cloud Vision API](https://cloud.google.com/vision/docs/) beta was released earlier this month (I received an email on the beta release on March 01, 2016). The API currently allows for label detection, text detection, and face detection among [many others](https://cloud.google.com/vision/docs/concepts). 

### Setting Up

1. You'll need a Google Developers account to create the API keys and to take care of other authentication details. Google's documentation for setting up this API is [here](https://cloud.google.com/vision/docs/getting-started). This is enough to get set up on your local machine.

Don't forget to set up your credentials for the CLI to work:

```
$ export GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>

$ echo $GOOGLE_APPLICATION_CREDENTIALS
```

2. For the Python script, the [Label Detection Tutorial](https://cloud.google.com/vision/docs/label-tutorial) is a good start. You'll need to run a few "pip install" commands for "google-api-python-client", "oauth2client".

```
$ pip install apiclient
$ pip install oauth2client
$ pip install httplib2
```

3. Run the script. You can have a folder of images you'd like to call the API on or use individual images.

```
$ python google-vision-api.py images/
$ python google-vision-api.py dog.jpg
```

4. Specifiy features you'd like to query. The body portion of the service_request variable can be adjusted to include other data you'd like to get. Currently only label detection and text detection are included in this script but the [documentation](https://cloud.google.com/vision/docs/concepts) includes more.

```
LABEL_DETECTION	Execute Image Content Analysis on the entire image and return
TEXT_DETECTION	Perform Optical Character Recognition (OCR) on text within the image
FACE_DETECTION	Detect faces within the image
LANDMARK_DETECTION	Detect geographic landmarks within the image
LOGO_DETECTION	Detect company logos within the image
SAFE_SEARCH_DETECTION	Determine image safe search properties on the image
IMAGE_PROPERTIES	Compute a set of properties about the image (such as the image's dominant colors)
```

### Samples

The "Getting Started" tutorial provides a dog.jpg image to run in the first API call. 

![dog.jpg](https://github.com/nchah/google-vision-api/blob/master/images/dog.jpg)

It works as intended and correctly identifies the image as a dog. Extending the maxResults returns even more results as follows.
```
{
  "responses": [
    {
      "labelAnnotations": [
        {
          "mid": "/m/0bt9lr",
          "description": "dog",
          "score": 0.89208293
        },
        {
           "score": 0.85700572, 
           "mid": "/m/09686", 
           "description": "vertebrate"
        }, 
        {
           "score": 0.84881896, 
           "mid": "/m/01pm38", 
           "description": "clumber spaniel"
        }, 
        {
           "score": 0.84757507, 
           "mid": "/m/04rky", 
           "description": "mammal"
        }
      ]
    }
  ]
}
```

## Dependencies

In addition to the libraries required to authenticate with the Google APIs, the "google-vision-api-image-annotate.py" script uses the [Pillow 3.2.x library](https://pillow.readthedocs.org/en/3.2.x/index.html). This is different from the PIL library, which will not work with the script.

```
$ pip install Pillow

$ pip install --upgrade Pillow
```


## Data Sets

Fonts are from https://github.com/google/fonts

The Wikimedia Foundation provides regular data dumps at https://dumps.wikimedia.org/

The "Picture of the Year" archives can be found at https://dumps.wikimedia.org/other/poty/


## Image Annotations

Image annotations were succesfully done with the Python PIL version 3.2.x library. 

Sample image and annotations:

This was the first working implementation where text correctly wrote to the image file.

![github.png annotation](https://github.com/nchah/google-vision-api/blob/master/images-output/github-v1.png)

The function was further developed to write the output text to a separate area adjacent to the image. This allows the image and text data to be compared side by side in a single view.

![dog.jpg annotation](https://github.com/nchah/google-vision-api/blob/master/images-output/dog-v2.png)

Using Droid Sans Mono font to improve readability.

![flower.jpg annotation](https://github.com/nchah/google-vision-api/blob/master/images-output/flower-v2.png)

![github.png annotation](https://github.com/nchah/google-vision-api/blob/master/images-output/github-v3.png)


## Gallery


### wiki-pic-of-the-day-feb-2016

This folder contains image annotations for the Wikipedia Picture of the Day images for February 2016. Each image has been renamed by adding the date (YYYY-MM-DD) it was selected to be the Picture of the Day.

![wiki-pick-of-the-day-feb-2016 sample](https://github.com/nchah/google-vision-api/blob/master/gallery/wiki-pic-of-the-day-feb-2016/2016-02-02%20Kaiserin_Augusta_verl%C3%A4sst_Newyork%2C_Chromo-Lithographie_von_C.png)


### tech-companies-logos

This folder contains various logo images. The list of tech compaines was derived from https://en.wikipedia.org/wiki/List_of_largest_Internet_companies. 

![tech-companies-logos sample](https://github.com/nchah/google-vision-api/blob/master/gallery/tech-companies-logos/440px-Google_2015_logo.png)

