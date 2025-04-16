#!/usr/bin/env python3

import argparse
#import pandas as pd
import os
import cv2
#import numpy as np

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description="A simple program to visualize image collections")
    parser.add_argument("--images", type=str, default="None", help="CSV with images; the first field is the image name")
    parser.add_argument("--root_path", type=str, default=None)
    parser.add_argument("--scale_factor", type=float, default=1.0, help="Scale factor for visualization")
    return parser.parse_args()

def draw_text(image, text, x=50, y=50, color =(0,255,0)):
    text_color = color  # Red text
    fontscale = 1
    thickness = 2
    cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, fontscale, text_color, thickness)
    return image

def draw_filename(image, text, x=50, y=200, color=(0,255,0)):
    return image
    text_color = color  # Red text
    fontscale = 1
    thickness = 2
    cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, fontscale, text_color, thickness)
    return image

class Vfich:
    def __init__(self, image_collection, root_path=None, labels_filename=None, scale_factor=0.25):
        self.image_collection = image_collection
        self.index = 0
        self.num_images = len(self.image_collection)
        self.root_path = root_path
        self.labels = {}
        self.labels_filename = labels_filename if labels_filename is not None else "images"
        self.scale_factor = scale_factor
        self.color =(0,255,0) # Green text
        self.possible_keys = ['a', 'b', 'c'] + [chr(v) for v in range(ord('0'),ord('9')+1)]
        self.load_labels()
        self.show_image(self.index)

    def load_image(self, index):
        nimags=len(self.image_collection)
        image_path = self.image_collection[index] if self.root_path is None else  os.path.join(self.root_path, self.image_collection[index] ) 
        print(f"{index}/{nimags} ** Loading image: {image_path}")
        
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error loading image {image_path}")
            return None
        
        # Rescale image
        if self.scale_factor != 1.0:
            height, width = image.shape[:2]
            new_size = (int(width * self.scale_factor), int(height * self.scale_factor))
            image = cv2.resize(image, new_size)
        
        
        label = self.labels.get(image_path, None)
        label_text = f"Label = {label}" if label else "Unlabeled"
        image = draw_text(image, label_text, color=self.color)
        image = draw_filename(image, image_path.split("/")[-1], y = image.shape[0] - 50, color=self.color)
        return image

    def load_labels(self):
        print("Loading previous labels")
        possible_keys = self.possible_keys
        for key in possible_keys:
            filename = f"{self.labels_filename}_{key}.txt"
            if os.path.exists(filename):
                print(f"Loading labels from {filename}")
                with open(filename, "r") as f:
                    for line in f:
                        image_name = line.strip()
                        self.labels[image_name] = key

    def save_labels(self):
        possible_keys = self.possible_keys
        for key in possible_keys:
            filename = f"{self.labels_filename}_{key}.txt"
            if os.path.exists(filename):
                os.remove(filename)
        for image_name, label in self.labels.items():
            if label == 'r':  # skip deleted
                continue
            filename = f"{self.labels_filename}_{label}.txt"
            with open(filename, "a") as f:
                f.write(f"{image_name}\n")

    def show_image(self, index):
        image = self.load_image(index)
        if image is not None:
            cv2.imshow("Frame", image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

    def update_index(self, index):
        index = max(0, min(self.num_images - 1, index))
        self.index = index
        self.show_image(index)

    def handle_key_event(self, key):
        print("Key pressed:", key)
        image_key = self.image_collection[self.index]
        if key >= ord('0') and key <=ord('9'):
            print(f"Saving {image_key} into group {chr(key)}"	)
            self.labels[image_key]=chr(key)
        
        if key == ord('a'):
            print(f"Saving {image_key} into group A")
            self.labels[image_key] = "a"
        elif key == ord('b'):
            print(f"Saving {image_key} into group B")
            self.labels[image_key] = "b"
        elif key == ord('c'):
            print(f"Saving {image_key} into group C")
            self.labels[image_key] = "c"


            
        elif key == ord('s'): #start
            print("First image")
            self.update_index(0)
        elif key == ord('e'):#end
            print("Last image")
            self.update_index(0)  
                      
        elif key == ord('r') or key == ord('d'): # remove or delete
            print(f"Deleting {image_key}")
            
            self.labels.pop(image_key, None)
        elif key == ord('p')   or key==85 or key ==82 : # previa p RePag o <-
            self.update_index(self.index - 1)
            print(f"Image {image_key}")
        elif key == ord('n') or key==86 or key == 83:#next n AvPag o ->
            print(f"Image {image_key}")
            self.update_index(self.index + 1)
        self.save_labels()

def main(args):
    with open(args.images, "r") as f:
        images = sorted([line.strip() for line in f.readlines()])
    
    labels_filename = os.path.splitext(args.images)[0]
    vfich = Vfich(images, root_path=args.root_path, labels_filename=labels_filename, scale_factor=args.scale_factor)

    while True:
        vfich.show_image(vfich.index)
        key = cv2.waitKey(0) & 0xFF  # Capture key press
        print("key=", key)
        if key == 27 or key==ord('q') :  # Escape key
            print("Exit key=", key)
            break
        vfich.handle_key_event(key)

if __name__ == "__main__":
    args = parse_args()
    print('Called with args:')
    print(args)
    main(args)
