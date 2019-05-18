from google.cloud import vision
from google.cloud.vision import types
import sys

client = vision.ImageAnnotatorClient.from_service_account_file('./research-pill-google_service_account_key.json')

image_path = sys.argv[1]
with open(image_path, 'rb') as image_file: content = image_file.read()
image = vision.types.Image(content=content)
text_response = client.text_detection(image=image)
texts = [text.description for text in text_response.text_annotations]
print(texts)