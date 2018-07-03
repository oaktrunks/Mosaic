"""
Daniel Tomei
Image Processing Summer I 2018

Final Project

Description:
    This script turns an image into a mosaic consisting of other images.

Requirements:
    PIL and google_images_download libraries
"""
from google_downloader import google_download
from PIL import Image
import os, shutil

#Directory where our processed pieces will be placed
PIECE_DIRECTORY = './temp_images/pieces/'

'''
euclid2 and closestTuple taken from John Coleman's answer on
https://stackoverflow.com/questions/41088773/how-can-i-find-a-tuple-from-a-group-of-tuples-with-the-values-closest-to-a-given
'''
def euclid2(x,y):
    """
    euclid2 returns the distance between two tuples

    Args:
        x: tuple to be compared
        y: other tuple to be compared

    Returns:
        integer distance between two tuples
    """
    return sum((xi-yi)**2 for xi,yi in zip(x,y))

def closestTuple(target,tuples, dist = euclid2):
    """
    closestTuple returns the tuple in the iteratable tuples object
        that is closest to our target tuple

    Args:
        target: target tuple to find closest tuple to
        tuples: iteratable object containing our possible tuples

    Returns:
        The tuple in tuples that is closest to the target
    """
    return min((dist(t,target),t) for t in tuples)[1]

def get_avg_color(image_data):
    """
    returns average color of an image

    Args:
        image_data: image data to be processed

    Returns:
        tuple containing average rgb color of image
    """
    temp = image_data.copy()
    temp.thumbnail((1,1))
    return temp.getpixel((0,0))

def process_pieces(piece_directory, piece_size):
    """
    process_pieces resizes all of our pieces to be squares of piece_size
        length and width. It also creates a dictionary which maps the
        average color of every piece to the file name of the piece.

    Args:
        piece_directory: Relative or absolute directory to be used as pieces
            for our mosaic creation
        piece_size: Integer pixel size which our pieces will be resized to be
            squares of

    Returns:
        A dictionary mapping the average colors of images to their file names
    """
    #Setting new directory for the pieces to be saved
    new_piece_directory = PIECE_DIRECTORY

    #Supported image formats
    formats = ['JPG', 'JPEG', 'PNG']

    #Dictionary holding average colors of images
    color_averages = {}

    #If folder already exists, delete it
    #This prevents pieces being re-used from previous iterations of the script
    if os.path.exists(new_piece_directory):
        shutil.rmtree(new_piece_directory)

    #Make the directory to be used
    os.makedirs(new_piece_directory)

    #Iterating through files in piece directory
    for image_name in os.listdir(piece_directory):
        if os.path.isfile('{}/{}'.format(piece_directory, image_name)):
            #Open the image
            im = Image.open('{}/{}'.format(piece_directory, image_name))

            #Only use the supported formats
            if(im.format not in formats):
                continue

            #Convert image to RGB incase it is not already
            im = im.convert('RGB')

            #Resize the images down to proper piece size
            #Also make the images square by cropping them
            if im.size[0] > im.size[1]: #Width is bigger than height
                #Resize it so that height is <piece_size> long
                height = int(im.size[0]* piece_size / im.size[1])
                im = im.resize((height, piece_size))
                #Crop it so that the image becomes square
                border = (height - piece_size) // 2
                im = im.crop((border, 0, height - border, piece_size))

            elif im.size[1] > im.size[0]: #Height is bigger than width
                #Resize it so that width is <piece_size> long
                width = int(im.size[1]* piece_size / im.size[0])
                im = im.resize((piece_size, width))
                #Crop it so that the image becomes square
                border = (width - piece_size) // 2
                im = im.crop((0, border, piece_size, width - border))
            
            else: #Image is already square
                im = im.resize((piece_size, piece_size))

            #Find the average color of the image
            color_averages[get_avg_color(im)] = image_name

            #Save the processed image in our processed images directory
            im.save('{}/{}'.format(new_piece_directory, image_name))
    
    return color_averages

def create_mosaic(image, averages, piece_size, sample_size):
    """
    create_mosaic creates our mosaic for us. This is done by taking samples
        of our image and finding the closest color match for that sample
        in our folder of pieces.

    Args:
        image: The original image data to turn into a mosaic
        averages: Dictionary containing tuple color averages mapped to
            the filenames of the pieces associated to them
        piece_size:
            The pixel length that our square pieces will be on the final
                mosaic
        sample_size:
            The pixel length of squares to sample from the original image and 
                convert into the closest color matching pieces

    Returns:
        The completed mosaic image data
    """
    #Set the directory that our pieces are in
    piece_directory = PIECE_DIRECTORY

    #Get our sizes
    image_width, image_height = image.size

    #Set our iteration limitations
    x_limit = (image_width - image_width % sample_size) 
    y_limit = (image_height - image_height % sample_size)

    #Crop our image to be divisible by our sample size
    image = image.crop((0, 0, x_limit, y_limit))

    #Define our new image
    mosaic = Image.new('RGB', (x_limit // sample_size * piece_size, y_limit // sample_size * piece_size))

    #Start iterating over image and finding closest matching pieces
    x_piece = y_piece = 0
    x_sample = y_sample = 0
    while y_sample < y_limit:
        while x_sample < x_limit:
            #Crop a segment and find its average color
            avg = get_avg_color(image.crop((x_sample, y_sample, x_sample + sample_size, y_sample + sample_size)))

            #Find the segment's closest color matching piece
            best_piece = averages[closestTuple(avg,averages)]

            #Insert the best_piece into our image
            best_piece = Image.open('{}/{}'.format(piece_directory, best_piece))
            mosaic.paste(best_piece, (x_piece, y_piece))

            #Incrementent our iteration values
            x_sample += sample_size
            x_piece += piece_size

        #Increment and reset our iteration values
        y_sample += sample_size
        y_piece += piece_size
        x_sample= x_piece = 0

    return mosaic


if __name__ == "__main__":
    #Output a header letting user know how to use program
    print("****************************************************************************\n")
    print("**                   Mosaic written by Daniel Tomei                       **\n")
    print("**                                                                        **\n")
    print("**                        Explanation:                                    **\n")
    print("**  This script turns an existing image into a mosaic consisting of       **\n")
    print("**  other images. This is done by splitting the original image into       **\n")
    print("**  samples, each sample's color average is then compared to our          **\n")
    print("**  potential mosaic pieces and the best match is found. The most         **\n")
    print("**  important parts of this process are the sampling size and piece size  **\n")
    print("**  The sample size specifies the size of the rectangles sampled from the **\n")
    print("**  original image. And the piece size speicifies the rectangle size of   **\n")
    print("**  our pieces in the final mosaic. If these values multiplied together   **\n")
    print("**  creates an image that is too large we run into memory issues.         **\n")
    print("**  So play around with these values, and don't be afraid to stray from   **\n")
    print("**  my recommended values and experiment some.                            **\n")
    print("**                                                                        **\n")
    print("****************************************************************************\n")
    print('\n\n')

    #Promt user to see if they want to download images to be used as pieces
    ans = input("Would you like to download some images to be used? (Y / N)\n")
    if ans.upper() == 'Y':
        word = input("What keyword would you like to search for?\n")
        amount = input("What is the maximum amount of images you would like to download?\n")
        print("Downloading images, don't close program.")
        dir = google_download(keyword = word, limit = amount)
        print("Your images have been downloaded to {}\n\n".format(dir))
    
    #Select image to be used
    imagename =  input("\nEnter the name or path of the image you would "
                        "like to turn into a mosaic.\n"
                        "Include the extension. "
                        "If you do not have good images, use the included\n"
                        "./test_images/usaflag.jpg or ./test_images/grand_canyon.jpg\n")
    image = Image.open(imagename)
    # imagename = 'usaflag.jpg'
    # image = Image.open('./usaflag.jpg')

    #Select pieces to be used
    pieces_directory =  input("\nEnter the path of the directory containing the"
                        " images to be used \nas pieces for the mosaic. "
                        "If you do not have a good directory, use\n the included "
                        "./test_images/pieces/ which consists of galaxy images\n")

    #Select desired piece size
    piece_size =  int(input("\nEnter the square pixel length you would like the"
                        " pieces to be in the final mosaic.\n"
                        "CAUTION: If this value is too big, it can cause memory issues.\n"
                        "A higher number will result in the mosaic pieces "
                        "being higher resolution.\n"
                        "Recommended values are between 5 and 50\n"))

    #Select desired sample size
    sample_size =  int(input("\nEnter the square pixel length you would like the"
                        " original image to be sampled by.\n"
                        "CAUTION: If this value is too small, it can cause memory issues.\n"
                        "A lower number will result in the mosaic better "
                        "matching the original image.\n"
                        "Recommended values are between 5 and 20\n"))

    #Output to show that program is busy
    print("\nProcessing pieces. This might take a while.")

    #Get the color averages of our pieces
    averages = process_pieces(pieces_directory, piece_size)
    print("Done processing pieces.\n")

    #Output to show that program is busy
    print("Creating the mosaic. This might take a while too.")
    print("Please don't close the program.\n")

    #Create our mosaic consisting of pieces
    mosaic = create_mosaic(image, averages, piece_size, sample_size)

    #Save our mosaic
    mosaic.save("{}_mosaic.png".format(os.path.basename(imagename).split('.')[0]))

    #Output to let user know we're done
    print("Creation complete, mosaic saved as {}.".format("{}_mosaic.png".format(os.path.basename(imagename).split('.')[0])))