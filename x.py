import os
import requests
from google.cloud import storage

def download_file(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

def upload_to_gcs(local_filename, bucket_name, gcs_filename):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_filename)
    blob.upload_from_filename(local_filename)
    return blob.public_url

def main():
    url = input("Enter the URL of the file you want to download: ")
    local_filename = url.split("/")[-1]
    print("Downloading file...")
    download_file(url, local_filename)
    print("File downloaded successfully.")
    
    bucket_name = input("Enter the name of the Google Cloud Storage bucket: ")
    gcs_filename = input("Enter the filename to be used in Google Cloud Storage: ")
    print("Uploading file to Google Cloud Storage...")
    public_url = upload_to_gcs(local_filename, bucket_name, gcs_filename)
    print("File uploaded successfully.")
    
    print("Public URL for accessing the file:")
    print(public_url)

    # Delete the local file after uploading to Google Cloud Storage
    os.remove(local_filename)

if __name__ == "__main__":
    main()
