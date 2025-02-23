""" Script to preprocess the omniglot dataset and pickle it into an array that's easy
    to index my character type.
    Usage: python load_data.py --path {omniglot_location} --save {pickles_location} """

import sys
import numpy as np
import cv2
import pickle
import os
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--path", help = "Path where omniglot folder resides")
parser.add_argument("--save", help = "Path to pickle data to.", default=os.getcwd())

args = parser.parse_args()

# the paths below are inside the original omniglot project
data_path = os.path.join(args.path, "python")
train_folder = os.path.join(data_path,'images_background')
valpath = os.path.join(data_path,'images_evaluation')

save_path = args.save

lang_dict = {}

def loadimgs(path,n=0):
    #if data not already unzipped, unzip it.
    if not os.path.exists(path):
        print("unzipping")
        os.chdir(data_path)
        os.system("unzip {}".format(path+".zip" ))
    X=[]
    y = []
    cat_dict = {}
    lang_dict = {}
    curr_y = n
    #we load every alphabet seperately so we can isolate them later
    for alphabet in os.listdir(path):
        print("loading alphabet: " + alphabet)
        lang_dict[alphabet] = [curr_y,None]
        alphabet_path = os.path.join(path,alphabet)
        #every letter/category has it's own column in the array, so  load seperately
        for letter in os.listdir(alphabet_path):
            cat_dict[curr_y] = (alphabet, letter)
            category_images=[]
            letter_path = os.path.join(alphabet_path, letter)
            for filename in os.listdir(letter_path):
                image_path = os.path.join(letter_path, filename)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                category_images.append(image)
                y.append(curr_y)
            try:
                X.append(np.stack(category_images))
            #edge case  - last one
            except ValueError as e:
                print(e)
                print("error - category_images:", category_images)
            curr_y += 1
            lang_dict[alphabet][1] = curr_y - 1
    y = np.vstack(y)
    X = np.stack(X)
    return X,y,lang_dict


X,y,c=loadimgs(train_folder)

with open(os.path.join(save_path,"train.pickle"), "wb") as f:
    pickle.dump((X,c),f)

X,y,c=loadimgs(valpath)

with open(os.path.join(save_path,"val.pickle"), "wb") as f:
	pickle.dump((X,c),f)
