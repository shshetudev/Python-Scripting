import json
import time
from datetime import datetime

import requests  # Request image from web
import shutil  # Save image locally
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def extract(json_file, dir):
    # Add execution time
    # Load the json file containing image information

    image_file = open(json_file)
    images = json.load(image_file)
    image_file.close()
    # image_list = []
    product_ids = set()
    total_images = 0
    successful = 0
    # Create dictionaries according to the product_id
    start_time = time.localtime()
    if images:
        for image in images:
            product_ids.add(image['productId'])
        for prod_id in product_ids:
            paths = []
            file_name_counter = 0
            for image in images:
                if prod_id == image['productId']:
                    # Download images
                    total_images = total_images + 1
                    file_name_counter = file_name_counter + 1
                    out = download_image_shortly(image['path'], dir + "/" + str(prod_id),
                                                 str(prod_id) + '-' + str(file_name_counter))
                    if out:
                        successful = successful + 1
                        print('Successful so far:{}'.format(successful))
                    # paths.append(image['path'])
            # image_list.append({prod_id: paths})
    end_time = time.localtime()
    print('Total images:{}, Successful:{}, Time elapsed:{}'.format(total_images, successful, (end_time - start_time)))
    # print(image_list[0])

    # Download these images: 1. Create the directory as the id, 2. download the images as value
    # Print number of successful and unsuccessful downloads


def download_image(url, file_name):
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(file_name, 'wb') as img:
            shutil.copyfileobj(res.raw, img)
        print('Image successfully downloaded: ', file_name)
    else:
        print('Image couldn\'t be retrieved')


def get_image_extension(url):
    extension = '.txt'
    if '.png' in url:
        extension = '.png'
    elif '.jpeg' in url or '.jpg' in url:
        extension = '.jpeg'
    elif '.gif' in url:
        extension = '.gif'
    elif '.tiff' in url:
        extension = '.tiff'
    elif '.psd' in url:
        extension = '.psd'
    elif '.pdf' in url:
        extension = '.pdf'
    elif '.eps' in url:
        extension = '.eps'
    elif '.ai' in url:
        extension = '.ai'
    elif '.raw' in url:
        extension = '.raw'
    return extension


def download_image_shortly(url, directory, file_name):
    result = False
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        if os.path.exists(directory) is False:
            os.mkdir(directory)
        # todo: Add it after getting confirmed from Aminur bhai.
        # file_name = directory + '/' + file_name + get_image_extension(url)
        file_name = directory + '/' + file_name + '.jpeg'
        file = open(file_name, 'wb')
        file.write(res.content)
        print('Saving image:{} at time:{}'.format(file_name, datetime.now().strftime("%H:%M:%S")))
        result = True
        file.close()
    return result
    # print('Image successfully downloaded: ', file_name)


# print('Image couldn\'t be retrieved')


# [{1,['dfd','dfd']},{2,['dfd','dfd']}]
def download(image_list: list, main_dir: str):

    for map in image_list:
        for key in map:
            directory = main_dir + '/' + key
            urls = image_list[key]
            for url in urls:
                file_name = float(key) + 1
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    os.mkdir(directory)
                    file = open(directory + '/' + str(file_name) + '.png', 'wb')
                    file.write(response.content)
                    file.close()
                    print('Image successfully downloaded: ', file_name)
            else:
                print('Image couldn\'t be retrieved')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # todo: Do we need to create a directory by ourself manually?
    dir_name = '/home/shetu/islami-book'
    json_file = '/home/shetu/islamic_book_2_image.json'
    extract(json_file, dir_name)
    # prod_ids = {1, 2, 3}
    # urls = ['https://i.imgur.com/ExdKOOz.png', 'https://i.imgur.com/ExdKOOz.png', 'https://i.imgur.com/ExdKOOz.png']
    # image_list = [{1, urls}]
    # for prod_id in prod_ids:
    #     image_list.append({prod_id, urls})

    # download(image_list, '/home/shetu/demo')
    # download_image('https://i.imgur.com/ExdKOOz.png', '/home/shetu/demo.png', )
    # download_image_shortly('https://i.imgur.com/ExdKOOz.png', '/home/shetu/demo', 'demo')
