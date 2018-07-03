from google_images_download import google_images_download

keyword = "galaxy"
limit = 500
directory = "./temp_images/"
subdirectory = "./temp_{}_images/".format(keyword)
chromedriver = "./chromedriver.exe"

response = google_images_download.googleimagesdownload()
absolute_image_paths = response.download({
                                    "keywords":keyword,
                                    "limit":limit,
                                    "output_directory":directory,
                                    "image_directory":subdirectory,
                                    "socket_timeout":1,
                                    "chromedriver": chromedriver
                                    })