#   7/17/2020, rakokuko
#   Extracts img data from lofter exported xml file.
#   Not applicable for images embeded in text blog entries (those with <img> tags)

import os
import re
import ast
import requests


def main():
    count = 0
    for file in os.listdir():
        if not file.endswith(".xml"):
            continue

        content = open(file, 'r').readlines()
        for line in content:
            if (re.search("photoLinks", line)):
                links = re.findall("\[\[(.*)\]\]\]", line)

                try:
                    #   convert string to dict (or tuple if there is more than one image in a single blog entry)
                    entry = ast.literal_eval(links[0])
                        
                    try:
                        print(entry["raw"])
                        count += 1
                        download_img(entry["raw"], count)
                        print("downloaded")
                    
                    except TypeError:
                        for item in entry:
                            count += 1
                            print(item["raw"])
                            download_img(item["raw"], count)
                            print("downloaded")
                        
                except:
                    print("shit happened!")
                    pass


def download_img(url, num):

    img_data = requests.get(url).content
    f_name = "img_" + str(num) + ".jpg"

    with open(f_name, "wb") as handler:
        handler.write(img_data)


if __name__ == '__main__':
    main()
