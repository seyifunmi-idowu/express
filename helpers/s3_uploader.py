import uuid

import boto3
from django.conf import settings


class S3Uploader(object):
    def __init__(self, append_folder=None):
        """
        :params append_folder: the s3 folder to upload file to; starts with '/' (e.g., /resumes)
        """
        self.use_s3 = settings.USE_S3
        self.bucket = settings.AWS_S3_BUCKET
        self.folder = f"backend-{settings.ENVIRONMENT}"
        if append_folder:
            self.folder += append_folder
        if self.use_s3:
            self.s3_resource = boto3.resource(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_DEFAULT_REGION,
            )

    def build_key(self, filename):
        extension = filename.split(".")[-1]
        return f"{uuid.uuid4().hex}.{extension}"

    def upload_file_object(self, file_object, file_name, use_random_key=True):
        key = self.build_key(file_name) if use_random_key else file_name
        key = f"{self.folder}/{key}"
        if self.use_s3:
            self.put_object(key=key, body=file_object)
        return f"https://{self.bucket}.s3.amazonaws.com/{key}"

    def put_object(self, key, body):
        # TODO: put this in a celery task because of lateness
        self.s3_resource.Bucket(self.bucket).put_object(
            Key=key, Body=body, ACL="public-read"
        )

    def hard_delete_object(self, image_url):
        res = (
            self.s3_resource.Bucket(self.bucket)
            .object_versions.filter(Prefix=f"{'/'.join(str(image_url).split('/')[3:])}")
            .delete()
        )
        return res


class SuggestedImageUploader(S3Uploader):
    def build_key(self, filename):
        """
        Appends the filename while uploading to S3 for easier retrieval.
        """
        extension = filename.split(".")[-1]
        file_name = filename.split(".")[0]
        s3_filename = "".join(file_name.split())
        return f"{s3_filename}{uuid.uuid4().hex}.{extension}"
