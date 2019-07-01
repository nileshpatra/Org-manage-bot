import argparse
import json
import itertools
import logging
import re
import os
import uuid
import sys
from urllib.request import urlopen, Request
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import time

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('[%(asctime)s %(levelname)s %(module)s]: %(message)s'))
    logger.addHandler(handler)
    return logger

logger = configure_logging()

REQUEST_HEADER = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


def get_soup(url, header):
    response = urlopen(Request(url, headers=header))
    return BeautifulSoup(response, 'html.parser')

def get_query_url(query):
    return "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch" % query

def extract_images_from_soup(soup):
    image_elements = soup.find_all("div", {"class": "rg_meta"})
    metadata_dicts = (json.loads(e.text) for e in image_elements)
    link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
    return link_type_records

def extract_images(query, num_images):
    url = get_query_url(query)
    logger.info("Souping")
    soup = get_soup(url, REQUEST_HEADER)
    logger.info("Extracting image urls")
    link_type_records = extract_images_from_soup(soup)
    return itertools.islice(link_type_records, num_images)

def get_raw_image(url):
    req = Request(url, headers=REQUEST_HEADER)
    resp = urlopen(req)
    return resp.read()

def save_image(raw_image, image_type, save_directory):
    extension = image_type if image_type else 'jpg'
    file_name = uuid.uuid4().hex
    save_path = os.path.join(save_directory, file_name)
    # plt.plot(raw_image)
    # time.sleep(10)
    with open(save_path, 'wb') as image_file:
        image_file.write(raw_image)
    return save_directory + '/' + file_name

def download_images_to_dir(images, save_directory, num_images=1):
    for i, (url, image_type) in enumerate(images):
        try:
            logger.info("Making request (%d/%d): %s", i, num_images, url)
            raw_image = get_raw_image(url)
            return raw_image
            return save_image(raw_image, image_type, save_directory)
        except Exception as e:
            logger.exception(e)

def run(query, save_directory, num_images=100):
    query = '+'.join(query.split())
    logger.info("Extracting image links")
    images = extract_images(query, num_images)
    logger.info("Downloading images")

    return download_images_to_dir(images, save_directory, num_images)

def main(topic='banana'):
    parser = argparse.ArgumentParser(description='Scrape Google images')
    parser.add_argument('-n', '--num_images', default=1, type=int, help='num images to save')
    parser.add_argument('-d', '--directory', default=os.getcwd() + '/imgs', type=str, help='save directory')
    args = parser.parse_args()
    return run(topic, args.directory, args.num_images)

# path = main()
# print(path)

img = main()
print(dir(img))
# plt.plot(img)
# plt.show()
# time.sleep(10)
# im = plt.imread(path)
# plt.imshow(im)
# plt.show()