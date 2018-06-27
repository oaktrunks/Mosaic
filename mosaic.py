from google_images_download import google_images_download
from PIL import Image

#Some testing values
keyword = "galaxy"
limit = 50
directory = "./temp_images/"
subdirectory = "./temp_{}_images/".format(keyword)

matrix_size = 50

def download_images(keyword, limit, directory, subdirectory):

    response = google_images_download.googleimagesdownload()
    absolute_image_paths = response.download({
                                    "keywords":keyword,
                                    "limit":limit,
                                    "output_directory":directory,
                                    "image_directory":subdirectory,
                                    "socket_timeout":1,
                                    "print_urls": True
                                    })

    return absolute_image_paths

if __name__ == "__main__":
    #Download images
    #download_images(keyword,limit,directory,subdirectory)

    #Create map of average color values in image directory
    avg = []

