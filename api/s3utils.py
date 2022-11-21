
import io
import uuid
from PIL import Image
import boto3

s3_client = boto3.client("s3", region_name="us-west-2")

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