import feedparser
from bs4 import BeautifulSoup
from bs4.element import Comment
import json
import datetime
from google.cloud import storage

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

# Define URL of the RSS Feed I want
a_reddit_rss_url = 'https://www.reddit.com/r/cryptocurrency/top/.rss'

feed = feedparser.parse( a_reddit_rss_url )

# Create filename with datetime
filename = "reddit-data-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".json"
#print(filename)

if (feed['bozo'] == 1):
    print("Error Reading/Parsing Feed XML Data")    
else:   
    data = feed['items']
    #print(data)
    
    # Save to a file
    with open(filename, 'w') as f:
        json.dump(data, f)


# Upload the file to 'reddit-data-bucket-jdxqd-2'       
bucket_name = 'reddit-data-bucket-jdxqd-2'
destination_blob_name = filename

def upload_blob(bucket_name, filename, destination_blob_name):
  """Uploads a file to the bucket."""
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)

  blob.upload_from_filename(filename)

  print('File {} uploaded to {}.'.format(
      filename,
      destination_blob_name))
    
# Upload JSON file
upload_blob(bucket_name, filename, destination_blob_name)

# Run analytics, save to txt file, and upload it to your bucket
import subprocess

bashCommand = "gcloud ml language analyze-entity-sentiment --content-file=gs://reddit-data-bucket-jdxqd-2/" + filename
#print(bashCommand)

shell_output = subprocess.getoutput(bashCommand)
#print(shell_output)

filename2 = "analytics -" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

analytics = open('analytics.txt', 'w')
analytics.write(shell_output)
analytics.close()


upload_blob(bucket_name, 'analytics.txt', filename2)