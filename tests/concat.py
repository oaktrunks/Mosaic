from PIL import Image
import os
import math

Images = "../temp_images/temp_galaxy_images/"


number_images = len(os.listdir(Images))
resize_size = 500
new_img = Image.new('RGB', (resize_size*int(math.sqrt(number_images)), resize_size*int(math.sqrt(number_images))))
xcoord = 0
ycoord = -1 * resize_size
iteration = 0

#Iterating through files in Images directory
for image_name in os.listdir(Images):
    if os.path.isfile('{}/{}'.format(Images, image_name)):
        im = Image.open('{}/{}'.format(Images, image_name))
        #im.save('test_{}.png'.format(image_name))

        #Resize the images down to a reasonable size
        #TODO, keep image scaling correctly
        im = im.resize((resize_size,resize_size))
        print(im)

        # #img = Image.new('RGB', (100,100))
        # #im = im.getdata()
        # #img.putdata(im)

        # #im.save('test_{}.png'.format(image_name))

        #Concatenate all the tiles together
        if iteration < (int(math.sqrt(number_images)) * int(math.sqrt(number_images))):
            if iteration % int(math.sqrt(number_images)) == 0:
                print("incrementing y")
                ycoord += resize_size
                xcoord = 0
            new_img.paste(im, (xcoord,ycoord))
            xcoord += resize_size
        iteration += 1

new_img.save('test_galaxy.png')