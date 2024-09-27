import os
import requests
from bs4 import BeautifulSoup
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Hugging Face API Token
huggingface_token = os.getenv('HuggingFace_API_KEY')

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# S3 Bucket name
bucket_name = os.getenv('AWS_BUCKET')

# Hugging Face GAIA dataset URL
huggingface_url = "https://huggingface.co/datasets/gaia-benchmark/GAIA/tree/main/2023/validation"

# Supported file types
SUPPORTED_FILE_TYPES = ('.json', '.pdf', '.png', '.jpeg', '.jpg', '.txt', '.xlsx', '.csv', '.zip', '.tar.gz', '.mp3', '.pdb', '.pptx', '.jsonld', '.docx', '.py')

# Get Windows Downloads folder path
download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

def get_file_urls_from_li_tags(huggingface_url):
    """Retrieve all file download URLs from the Hugging Face page"""
    headers = {
        "Authorization": f"Bearer {huggingface_token}"
    }
    
    response = requests.get(huggingface_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {huggingface_url}, status code: {response.status_code}")
        return []
    
    # Parse the HTML page
    soup = BeautifulSoup(response.text, 'html.parser')
    file_urls = []
    
    # Find all <li> elements containing <a> tags, extract href attributes
    for li in soup.find_all('li'):
        link = li.find('a', href=True)
        if link:
            href = link.get('href')
            
            # Filter URLs with supported file types
            if href and any(href.endswith(ext) for ext in SUPPORTED_FILE_TYPES):
                full_url = f"https://huggingface.co{href}".replace('/blob/', '/resolve/')
                file_urls.append(full_url)
                print(f"Found matching file URL: {full_url}")  # Debug: print matching file URLs
    
    if not file_urls:
        print("No matching file URLs found on the page.")
    
    return file_urls

def download_file(url, local_path):
    """Download file to local"""
    headers = {
        "Authorization": f"Bearer {huggingface_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {url} to {local_path}")
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# def remove_supported_extensions(file_name):
#     """Remove supported file extensions from the file name"""
#     for ext in SUPPORTED_FILE_TYPES:
#         if file_name.endswith(ext):
#             return file_name[:-len(ext)]  # Strip the extension
#     return file_name

def upload_to_s3(file_path, bucket_name, s3_key):
    """Upload file to AWS S3"""
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded {file_path} to S3 bucket {bucket_name} as {s3_key}")
    except Exception as e:
        print(f"Error uploading {file_path} to S3: {e}")

def process_files_and_upload(huggingface_url, bucket_name):
    """Download Hugging Face files and upload to S3"""
    file_urls = get_file_urls_from_li_tags(huggingface_url)
    
    if not file_urls:
        print("No files found to download.")
        return
    
    for file_url in file_urls:
        # Get the file name and local path
        file_name = file_url.split('/')[-1]
        local_path = os.path.join(download_dir, file_name)  # Specify the Windows Downloads folder
        
        # Download file to local
        download_file(file_url, local_path)
        
        # Check if the file was successfully downloaded
        if os.path.exists(local_path):
            print(f"File {local_path} successfully downloaded.")
            
            # Strip any supported file extensions from the file name
            # file_name_without_extension = remove_supported_extensions(file_name)
            
            # Upload to S3 with the file name without extension
            upload_to_s3(local_path, bucket_name, f"{file_name}")
            
            # Delete the local file
            os.remove(local_path)
            print(f"Deleted local file: {local_path}")
        else:
            print(f"File {local_path} not found, skipping upload.")

# Execute the download and upload process
process_files_and_upload(huggingface_url, bucket_name)