import os, urllib, re, json, os.path, argparse, requests
from os.path import basename
from pprint import pprint
# parse arguments
parser = argparse.ArgumentParser(description='Script to display contents of ARK record, or download content from a url')
parser.add_argument('-a','--ark', help='ark id', default="https://signpost.opensciencedatacloud.org/alias/ark:/31807/DC3-fd206d7f-af73-4095-8348-00cf3c8e5242")
parser.add_argument('-n','--no-parcel', help='Decide not to use Parcel', action='store_true')
args = parser.parse_args()
# remove any trailing newline characters
my_ark = args.ark.rstrip()
def download():
    # download the ARK record
    response = requests.get(my_ark)
    my_json = response.json()
    json_urls = my_json["urls"]
    for x in json_urls:
        if re.match( ("^" + "https://griffin"), x ):
           download_url = x
    # get the filename from the url
    filename = basename(download_url).rstrip()
    # create a string to perform the download
    if not args.no_parcel:
        download_string = "curl -k -O " + str(download_url).replace("griffin-objstore.opensciencedatacloud.org","192.168.20.101:9000")
    else:
        download_string = "curl -k -O " + str(download_url)
    print download_string
    # download the file
    os.system(download_string)
    print("Download of " + str(filename) + " is complete")
    exit(0)

def getJSON():
    response = urllib.urlopen(my_ark)
    data = json.load(response)
    print data
    # print data['urls']
    # print data['urls'][0].split('/')[-1]

if __name__ == "__main__":
    getJSON()
    download()
