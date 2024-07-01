import boto3
import csv
from PIL import Image, ImageDraw, ImageFont
import io

with open('credentials.csv', 'r') as file:
    next(file)
    reader = csv.reader(file)

    for line in reader:
        access_key_id = line[0]
        secret_access_key = line[1]


client = boto3.client('rekognition', region_name='ap-south-1',
                        aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

photo = 'cats.jpg'

with open(photo, 'rb') as image_file:
    source_bytes = image_file.read()


detect_objects = client.detect_labels(Image={'Bytes': source_bytes})

image = Image.open(io.BytesIO(source_bytes))
draw = ImageDraw.Draw(image)

for label in detect_objects['Labels']:
    print(label["Name"])
    print("Confidence: ", label["Confidence"])

    for instances in label['Instances']:
        if 'BoundingBox' in instances:

            box = instances["BoundingBox"]

            left = image.width * box['Left']
            top = image.height * box['Top']
            width = image.width * box['Width']
            height = image.height * box['Height']

            points = (
                        (left,top),
                        (left + width, top),
                        (left + width, top + height),
                        (left , top + height),
                        (left, top)
                    )
            draw.line(points, width=5, fill = "#e60202")

            shape = [(left - 2, top - 25), (width + 2 + left, top)]
            draw.rectangle(shape, fill = "#e60202")

            font = ImageFont.truetype("arial.ttf", 20)

            draw.text((left + 80, top - 25), label["Name"], font=font, fill='#ffffff')


image.show()
