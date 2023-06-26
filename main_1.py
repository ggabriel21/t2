#%%
#Importing libraries
from dagster import asset, op,job, get_dagster_logger, repository
import os
from retinaface import RetinaFace
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt
import natsort


#%%
#Declaring global variables
imageCount = 0
#%%
#Declaring OPs
@op
def get_data():
    path,folder,imagesList = next(os.walk("input/"))
    return(imagesList)

@op
def detect_face(imagesList):
    for image in imagesList:
        imageCount=imageCount+1
        if imageCount > 10: break
        print(f"extracting {image}")
        faces = RetinaFace.extract_faces(img_path = f"input/{image}", align = True)
        for face in faces:
            plt.imsave(f"output/{image}",face)
    return(imagesList)

@job
def face_detection():
    imagesList = get_data()
    detect_face(imagesList)

@repository
def my_repository():
    return [face_detection]
