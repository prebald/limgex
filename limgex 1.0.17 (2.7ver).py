#   7/17/2020, rakokuko
#   Extracts img data from lofter exported xml file.
#   Not applicable for images embeded in text blog entries (those with <img> tags)
#   1.0.1 using built-in urllib.request module instead of requests
#   1.0.15 Python2.7 compatible ver

import os
import re
import ast
import urllib

import ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def main():
    count = 0
    err = []
    err_count = 0
    for file in os.listdir(os.getcwd()):
        if not file.endswith(".xml"):
            continue

        f = open(file, 'r')
        content = f.readlines()
        f.close()

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

                    except:
                        for item in entry:
                            count += 1
                            print(item["raw"])
                            download_img(item["raw"], count)
                            print("downloaded")

                except:
                    print("shit happened!")
                    err.append(links[0])
                    err_count += 1
                    pass

    if err_count > 0:
     print ("\n{} Error(s) occured. \nFind failed entries in log.txt".format(err_count))
     log = "\n\n".join(err)
     with open("log.txt", "w") as shame:
         shame.write(log)


def download_img(url, num):
    f_name = "img_" + str(num) + ".jpg"
    img_data = urllib.urlopen(url).read()

    with open(f_name, "wb") as handler:
        handler.write(img_data)

if __name__ == '__main__':
    main()
