from PIL import Image
import os
import math

Images = "./temp_images/temp_galaxy_images/"


number_images = len(os.listdir(Images))
resize_size = 500
new_img = Image.new('RGB', (resize_size*int(math.sqrt(number_images)), resize_size*int(math.sqrt(number_images))))
xcoord = 0
ycoord = -1 * resize_size
iteration = 0



def get_avg_colors(image_data):
    temp = image_data.copy()
    temp.thumbnail((1,1))
    return temp.getpixel((0,0))

'''
euclid2 and closestTuple copied  from John Coleman's answer on
https://stackoverflow.com/questions/41088773/how-can-i-find-a-tuple-from-a-group-of-tuples-with-the-values-closest-to-a-given
'''
def euclid2(x,y):
    return sum((xi-yi)**2 for xi,yi in zip(x,y))

def closestTuple(target,tuples, dist = euclid2):
    return min((dist(t,target),t) for t in tuples)[1]

color_averages = {}
#Iterating through files in Images directory
for image_name in os.listdir(Images):
    if os.path.isfile('{}/{}'.format(Images, image_name)):
        im = Image.open('{}/{}'.format(Images, image_name))
        im = im.convert('RGB')
        #im.save('test_{}.png'.format(image_name))

        #Resize the images down to a reasonable size
        #Keep proper scaling, so crop the image
        if im.size[0] > im.size[1]: #Width is bigger than height
            #Resize is so that smaller part is <resize_size> long
            height = int(im.size[0]* resize_size / im.size[1])
            im = im.resize((height, resize_size))
            #Crop it so that the image becomes square
            border = (height - resize_size) // 2
            im = im.crop((border, 0, height - border, resize_size))

        elif im.size[1] > im.size[0]: #Height is bigger than width
            #Resize is so that smaller part is <resize_size> long
            width = int(im.size[1]* resize_size / im.size[0])
            im = im.resize((resize_size, width))
            #Crop it so that the image becomes square
            border = (width - resize_size) // 2
            im = im.crop((0, border, resize_size, width - border))
        
        else: #Image is already square
            im = im.resize((resize_size, resize_size))

        print(im)
        print(type(im))

        # #img = Image.new('RGB', (100,100))
        # #im = im.getdata()
        # #img.putdata(im)
        # #im.save('test_{}.png'.format(image_name))

        #Find the average color of the image
        color_averages[get_avg_colors(im)] = image_name
        # im.thumbnail((1,1))
        # im = im.resize((resize_size,resize_size))

        #Concatenate all the tiles together
        if iteration < (int(math.sqrt(number_images)) * int(math.sqrt(number_images))):
            if iteration % int(math.sqrt(number_images)) == 0:
                print("incrementing y")
                ycoord += resize_size
                xcoord = 0
            new_img.paste(im, (xcoord,ycoord))
            xcoord += resize_size
        iteration += 1

# #Try to find closest color match to current tile
# for i in range(0,25):
#     for j in range(0,50):
#         for k in range(0,25):
#             print('{} closest to {} which is {}'.format((i,j,k), closestTuple((i,j,k),color_averages), color_averages[closestTuple((i,j,k),color_averages)]))
            


new_img.save('thumb_test_galaxy.png')
#print(color_averages)