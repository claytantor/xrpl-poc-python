import os
import io
import uuid
from PIL import Image
import boto3


from dotenv import dotenv_values
config = {
    **dotenv_values(os.getenv("APP_CONFIG")),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

s3_session = boto3.Session(
    aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY']
)
s3_client = s3_session.client("s3", region_name="us-west-2")

def save_image(pil_image, s3_bucket_name, image_key):

    # Save the image to an in-memory file
    in_mem_file = io.BytesIO()
    pil_image.save(in_mem_file, format=pil_image.format)
    in_mem_file.seek(0)

    # Upload image to s3
    response = s3_client.upload_fileobj(
        in_mem_file, # This is what i am trying to upload
        s3_bucket_name,
        image_key,
        ExtraArgs={
            'ACL': 'public-read'
        }  
    )
    print(response)

    # create url from response
    return f'https://s3.us-west-2.amazonaws.com/{s3_bucket_name}/{image_key}'