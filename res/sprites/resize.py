# walk in every directory and resize all png images
import os
import pygame

# walk 
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".png"):
            # load image
            image = pygame.image.load(root + "\\" + file)
            # get image size
            width, height = image.get_size()
            # resize image
            image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
            # save image
            pygame.image.save(image, root + "\\" + file)

