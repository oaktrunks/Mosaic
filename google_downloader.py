from google_images_download import google_images_download

LIMIT = 100
DIRECTORY = "./temp_images/"
CHROMEDRIVER = "./chromedriver.exe"

def google_download(keyword, limit = LIMIT, directory = DIRECTORY):
    """
    google_download uses google_images_download library to download a set
        amount of images off of google images. Due to errors with some
        image hosting, it is not guaranteed to download the specified
        amount of images. So, the limit should be used as a maximum amount.

    Args:
        keyword: Keyword to search google for
        limit: Maximum amount of images to download
        directory: Directory to download the images to

    Returns:
        The directory the images were downloaded to
    """
    subdirectory = "./{}_images/".format(keyword)
    response = google_images_download.googleimagesdownload()
    absolute_image_paths = response.download({
                                        "keywords":keyword,
                                        "limit":limit,
                                        "output_directory":directory,
                                        "image_directory":subdirectory,
                                        "socket_timeout":1,
                                        "print_urls": True,
                                        "chromedriver": CHROMEDRIVER
                                        })
    return '{}/{}'.format(directory,subdirectory)