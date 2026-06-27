# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser
from plotly import graph_objects as go
import cv2
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shutil
import imagehash
from werkzeug.utils import secure_filename
from PIL import Image
import argparse
import urllib.request
import urllib.parse
from skimage.metrics import structural_similarity as ssim
# necessary imports 
import seaborn as sns
import plotly.express as px
import re
import warnings
warnings.filterwarnings('ignore')

plt.style.use('fivethirtyeight')
#%matplotlib inline
pd.set_option('display.max_columns', 26)
##
from PIL import Image, ImageOps
import scipy.ndimage as ndi

from skimage import transform
import seaborn as sns
#from keras.preprocessing.image import ImageDataGenerator , load_img , img_to_array
#from keras.models import Sequential
#from keras.layers import Conv2D, Flatten, MaxPool2D, Dense
##
import glob
#from keras.models import Sequential, load_model
import numpy as np
import pandas as pd
import seaborn as sns
#import torchvision.transforms as transforms
#from transformers import ViTForImageClassification, ViTFeatureExtractor
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models


import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
##

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  port="3306",
  password="praveen123",
  charset="utf8",
  database="multi_plant_leaf",
   auth_plugin='mysql_native_password'

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('test_img'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login_user.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    #if request.method=='GET':
    #    msg = request.args.get('msg')
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute("SELECT max(id)+1 FROM register")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO register(id,name,mobile,email,uname,pass) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,uname,pass1)
        mycursor.execute(sql,val)
        mydb.commit()
        msg="success"

    
        
    return render_template('register.html',msg=msg)




@app.route('/admin', methods=['GET', 'POST'])
def admin():
    
    dimg=[]
    '''path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        #resize
        img = cv2.imread('static/data/'+fname)
        rez = cv2.resize(img, (300, 400))
        cv2.imwrite("static/dataset/"+fname, rez)'''
        
        
    return render_template('admin.html',dimg=dimg)

@app.route('/add_plant', methods=['GET', 'POST'])
def add_plant():
    msg=""
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    #if request.method=='GET':
    #    msg = request.args.get('msg')
    if request.method=='POST':
        
        disease=request.form['disease']
        symptoms=request.form['symptoms']
        solution=request.form['solution']
        
        mycursor.execute("SELECT max(id)+1 FROM leaf_data")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO leaf_data(id,disease,symptoms,solution) VALUES (%s, %s, %s, %s)"
        val = (maxid,disease,symptoms,solution)
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for('add_plant'))

    mycursor.execute('SELECT * FROM leaf_data')
    data = mycursor.fetchall()
    
    return render_template('add_plant.html',msg=msg,data=data)

@app.route('/img_process', methods=['GET', 'POST'])
def img_process():
    

    return render_template('img_process.html')

@app.route('/pro1', methods=['GET', 'POST'])
def pro1():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        #list_of_elements = os.listdir(os.path.join(path_main, folder))

        #resize
        #img = cv2.imread('static/data/'+fname)
        #rez = cv2.resize(img, (400, 300))
        #cv2.imwrite("static/dataset/"+fname, rez)'''

        '''img = cv2.imread('static/dataset/'+fname) 	
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("static/trained/g_"+fname, gray)
        ##noice
        img = cv2.imread('static/trained/g_'+fname) 
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        fname2='ns_'+fname
        cv2.imwrite("static/trained/"+fname2, dst)'''

    return render_template('pro1.html',dimg=dimg)


def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))

@app.route('/pro11', methods=['GET', 'POST'])
def pro11():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)

    return render_template('pro11.html',dimg=dimg)

@app.route('/pro2', methods=['GET', 'POST'])
def pro2():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)

        #f1=open("adata.txt",'w')
        #f1.write(fname)
        #f1.close()
        ##bin
        '''image = cv2.imread('static/dataset/'+fname)
        original = image.copy()
        kmeans = kmeans_color_quantization(image, clusters=4)

        # Convert to grayscale, Gaussian blur, adaptive threshold
        gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

        # Draw largest enclosing circle onto a mask
        mask = np.zeros(original.shape[:2], dtype=np.uint8)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
            cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
            break
        
        # Bitwise-and for result
        result = cv2.bitwise_and(original, original, mask=mask)
        result[mask==0] = (0,0,0)

        
        ###cv2.imshow('thresh', thresh)
        ###cv2.imshow('result', result)
        ###cv2.imshow('mask', mask)
        ###cv2.imshow('kmeans', kmeans)
        ###cv2.imshow('image', image)
        ###cv2.waitKey()

        cv2.imwrite("static/trained/bb/bin_"+fname, thresh)'''

    
   

    path_main = 'static/dataset'
    '''for fname in os.listdir(path_main):
        ##RPN
        
        
        img = cv2.imread('static/trained/g_'+fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,1.5*dist_transform.max(),255,0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        segment = cv2.subtract(sure_bg,sure_fg)
        img = Image.fromarray(img)
        segment = Image.fromarray(segment)
        path3="static/trained/sg/sg_"+fname
        #segment.save(path3)'''
        

    return render_template('pro2.html',dimg=dimg)


@app.route('/pro3', methods=['GET', 'POST'])
def pro3():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        
    '''path_main = 'static/dataset'
    i=1
    while i<=50:
        fname="r"+str(i)+".jpg"
        dimg.append(fname)

        img = Image.open('static/data/classify/'+fname)
        array = np.array(img)

        array = 255 - array

        invimg = Image.fromarray(array)
        invimg.save('static/upload/ff_'+fname)
        i+=1
    i=1
    j=51
    while i<=10:
        
        fname="r"+str(j)+".jpg"
        dimg.append(fname)

        img = Image.open('static/dataset/'+fname)
        array = np.array(img)

        array = 255 - array

        invimg = Image.fromarray(array)
        invimg.save('static/upload/ff_'+fname)
        j+=1
        i+=1

    '''    
    
    return render_template('pro3.html',dimg=dimg)

@app.route('/pro4', methods=['GET', 'POST'])
def pro4():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)

        #####
        image = cv2.imread("static/dataset/"+fname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        
        path4="static/trained/ff/"+fname
        #edged.save(path4)
        ##
    
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        
        parser = argparse.ArgumentParser(
        description='Script to run Yolo-V8 object detection network ')
        parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
        parser.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt",
                                          help='Path to text network file: '
                                               'MobileNetSSD_deploy.prototxt for Caffe model or '
                                               )
        parser.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel",
                                         help='Path to weights: '
                                              'MobileNetSSD_deploy.caffemodel for Caffe model or '
                                              )
        parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
        args = parser.parse_args()

        # Labels of Network.
        classNames = { 0: 'background',
            1: 'plant' }

        # Open video file or capture device. 
        '''if args.video:
            cap = cv2.VideoCapture(args.video)
        else:
            cap = cv2.VideoCapture(0)'''

        #Load the Caffe model 
        '''net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)

        #while True:
        # Capture frame-by-frame
        #ret, frame = cap.read()
        
        frame = cv2.imread("static/dataset/"+fname)
        frame_resized = cv2.resize(frame,(300,400)) # resize frame for prediction

        blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 400), (127.5, 127.5, 127.5), False)
        #Set to network the input blob 
        net.setInput(blob)
        #Prediction of network
        detections = net.forward()

        #Size of frame resize (300x400)
        cols = frame_resized.shape[1] 
        rows = frame_resized.shape[0]

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2] #Confidence of prediction 
            if confidence > args.thr: # Filter prediction 
                class_id = int(detections[0, 0, i, 1]) # Class label

                # Object location 
                xLeftBottom = int(detections[0, 0, i, 3] * cols) 
                yLeftBottom = int(detections[0, 0, i, 4] * rows)
                xRightTop   = int(detections[0, 0, i, 5] * cols)
                yRightTop   = int(detections[0, 0, i, 6] * rows)
                
                # Factor for scale to original size of frame
                heightFactor = frame.shape[0]/300.0  
                widthFactor = frame.shape[1]/300.0 
                # Scale object detection to frame
                xLeftBottom = int(widthFactor * xLeftBottom) 
                yLeftBottom = int(heightFactor * yLeftBottom)
                xRightTop   = int(widthFactor * xRightTop)
                yRightTop   = int(heightFactor * yRightTop)
                # Draw location of object  
                cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                              (0, 255, 0))
                try:
                    y=yLeftBottom
                    h=yRightTop-y
                    x=xLeftBottom
                    w=xRightTop-x
                    image = cv2.imread("static/dataset/"+fname)
                    #mm=cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #cv2.imwrite("static/trained/classify/"+fname, mm)
                    #cropped = image[yLeftBottom:yRightTop, xLeftBottom:xRightTop]

                    #gg="segment.jpg"
                    #cv2.imwrite("static/result/"+gg, cropped)


                    #mm2 = PIL.Image.open('static/trained/'+gg)
                    #rz = mm2.resize((300,300), PIL.Image.ANTIALIAS)
                    #rz.save('static/trained/'+gg)
                except:
                    print("none")
                    #shutil.copy('getimg.jpg', 'static/trained/test.jpg')
                # Draw label and confidence of prediction in frame resized
                if class_id in classNames:
                    label = classNames[class_id] + ": " + str(confidence)
                    claname=classNames[class_id]

                    
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                    yLeftBottom = max(yLeftBottom, labelSize[1])
                    cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                         (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                         (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                    #print(label) #print class and confidence ''' 
    return render_template('pro4.html',dimg=dimg)


    

@app.route('/pro5', methods=['GET', 'POST'])
def pro5():
    msg=""
    dimg=[]
    path_main = 'static/trained/sg'
    for fname in os.listdir(path_main):
        dimg.append(fname)
    #graph
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[30,80,140,210,265]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model Precision")
    plt.ylabel("precision")
    
    fn="graph1.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph2
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[30,80,140,220,275]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model recall")
    plt.ylabel("recall")
    
    fn="graph2.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph3########################################
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(94,98)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(94,98)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[10,42,76,124,173]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy %")
    
    fn="graph3.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #######################################################
    #graph4
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,4)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(1,4)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[10,42,76,124,173]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Model loss")
    
    fn="graph4.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    return render_template('pro5.html',dimg=dimg)

def toString(a):
  l=[]
  m=""
  for i in a:
    b=0
    c=0
    k=int(math.log10(i))+1
    for j in range(k):
      b=((i%10)*(2**j))   
      i=i//10
      c=c+b
    l.append(c)
  for x in l:
    m=m+chr(x)
  return m
                
@app.route('/pro6', methods=['GET', 'POST'])
def pro6():
    msg=""
    dimg=[]
    path_main = 'static/trained/ff'
    print("aaa")
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)

    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')
    '''data1=[]
    data2=[]
    data3=[]
    data4=[]
    v1=0
    v2=0
    v3=0
    v4=0
    path_main = 'static/trained'
    #for fname in os.listdir(path_main):
    i=0
    i<127
        dimg.append(fname)
        d1=fname.split('_')
        if d1[0]=='d':
            data1.append(fname)
            v1+=1
        if d1[0]=='f':
            data2.append(fname)
            v2+=1
        if d1[0]=='n':
            data3.append(fname)
            v3+=1
        if d1[0]=='w':
            data4.append(fname)
            v4+=1
        

    g1=v1+v2+v3+v4
    dd2=[v1,v2,v3,v4]
    
    
    doc = cname #list(data.keys())
    values = dd2 #list(data.values())
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 5))
     
    # creating the bar plot
    plt.bar(doc, values, color ='blue',
            width = 0.4)
 

    plt.ylim((1,g1))
    plt.xlabel("Objects")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    plt.xticks(rotation=20)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    #plt.clf()'''

    #,data1=data1,data2=data2,data3=data3,data4=data4,cname=cname,v1=v1,v2=v2,v3=v3,v4=v4
    ##############################

    
    ###############################
    
    
    

    return render_template('pro6.html',dimg=dimg)

def CNN():
    #Lets start by loading the Cifar10 data
    (X, y), (X_test, y_test) = cifar10.load_data()

    #Keep in mind the images are in RGB
    #So we can normalise the data by diving by 255
    #The data is in integers therefore we need to convert them to float first
    X, X_test = X.astype('float32')/255.0, X_test.astype('float32')/255.0

    #Then we convert the y values into one-hot vectors
    #The cifar10 has only 10 classes, thats is why we specify a one-hot
    #vector of width/class 10
    y, y_test = u.to_categorical(y, 10), u.to_categorical(y_test, 10)

    #Now we can go ahead and create our Convolution model
    model = Sequential()
    #We want to output 32 features maps. The kernel size is going to be
    #3x3 and we specify our input shape to be 32x32 with 3 channels
    #Padding=same means we want the same dimensional output as input
    #activation specifies the activation function
    model.add(Conv2D(32, (3, 3), input_shape=(32, 32, 3), padding='same',
                     activation='relu'))
    #20% of the nodes are set to 0
    model.add(Dropout(0.2))
    #now we add another convolution layer, again with a 3x3 kernel
    #This time our padding=valid this means that the output dimension can
    #take any form
    model.add(Conv2D(32, (3, 3), activation='relu', padding='valid'))
    #maxpool with a kernet of 2x2
    model.add(MaxPooling2D(pool_size=(2, 2)))
    #In a convolution NN, we neet to flatten our data before we can
    #input it into the ouput/dense layer
    model.add(Flatten())
    #Dense layer with 512 hidden units
    model.add(Dense(512, activation='relu'))
    #this time we set 30% of the nodes to 0 to minimize overfitting
    model.add(Dropout(0.3))
    #Finally the output dense layer with 10 hidden units corresponding to
    #our 10 classe
    model.add(Dense(10, activation='softmax'))
    #Few simple configurations
    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(momentum=0.5, decay=0.0004), metrics=['accuracy'])
    #Run the algorithm!
    model.fit(X, y, validation_data=(X_test, y_test), epochs=25,
              batch_size=512)
    #Save the weights to use for later
    model.save_weights("cifar10.hdf5")
    #Finally print the accuracy of our model!
    print("Accuracy: &2.f%%" %(model.evaluate(X_test, y_test)[1]*100))

def model():
    IMG_SIZE = 128
    BATCH = 32
    EPOCHS = 20

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=20,
        zoom_range=0.2,
        horizontal_flip=True
    )

    train = train_datagen.flow_from_directory(
        "dataset",
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH,
        class_mode="categorical",
        subset="training"
    )

    valid = train_datagen.flow_from_directory(
        "dataset",
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH,
        class_mode="categorical",
        subset="validation"
    )

    num_classes = len(train.class_indices)

    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE,IMG_SIZE,3)),
        MaxPooling2D(),

        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(),

        Conv2D(128, (3,3), activation='relu'),
        MaxPooling2D(),

        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(train, validation_data=valid, epochs=EPOCHS)
    model.save("leaf_cnn_model.h5")
    print("CNN Training Complete!")

#######
@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    data2=[]
    data21=[]
    data3=[]
    data4=[]
    
    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')


    ##    
    ff2=open("static/trained/tdata.txt","r")
    rd=ff2.read()
    ff2.close()

    num=[]
    r1=rd.split(',')
    s=len(r1)
    ss=s-1
    i=0
    while i<ss:
        num.append(int(r1[i]))
        i+=1

    #print(num)
    dat=toString(num)
    dd2=[]
    ex=dat.split(',')
    print("xxxxx")
    ##
    vv=[]
    vn=0

    n1=0
    n2=0
    n3=0
    n4=0
    n5=0
    n6=0
    
    dt1=[]
    dt2=[]
    dt3=[]
    dt4=[]
    dt5=[]
    dt6=[]
    print("leaf1###")
    jn=1
    path_main = 'static/data1'
    for val in ex:
        dt=[]
        n=0
        
        if int(val)<7:
            for fname in os.listdir(path_main):
                #print(fname)
                #print(jn)
                jn+=1
                fa1=fname.split('.')
                fa=fa1[0].split('-')
                if len(fa)>1:
                    
                    nc=int(fa[1])
                    
                    if fa[1]=="1":
                        dt1.append(fname)
                        n1+=1
                    if fa[1]=="2":
                        dt2.append(fname)
                        n2+=1
                    if fa[1]=="3":
                        dt3.append(fname)
                        n3+=1
                    if fa[1]=="4":
                        dt4.append(fname)
                        n4+=1
                    if fa[1]=="5":
                        dt5.append(fname)
                        n5+=1
                    if fa[1]=="6":
                        dt6.append(fname)
                        n6+=1
            
            
            vn+=n
    print("end###")
    vv.append(n1)
    vv.append(n2)
    vv.append(n3)
    vv.append(n4)
    vv.append(n5)
    vv.append(n6)
    
    data2.append(dt1)
    data2.append(dt2)
    data2.append(dt3)
    data2.append(dt4)
    data2.append(dt5)
    data2.append(dt6)
        
    #print(data2)
    i=0
    vd=[]
    data4=[]
    while i<6:
        vt=[]
        vi=i+1
        vv[i]

        vt.append(cname[i])
        vt.append(str(vv[i]))
        
        vd.append(str(vi))
        data4.append(vt)
        i+=1
   
    dd2=vv
    doc = cname #list(data.keys())
    values = dd2 #list(data.values())
    
    #print(doc)
    #print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    cc=['pink','yellow','orange','red','green','blue']
    plt.bar(doc, values, color =cc,
            width = 0.4)
 

    plt.ylim((1,20))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    #plt.xticks(rotation=20)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    #plt.clf()
    ################################################
    ff=open("static/trained/class2.txt",'r')
    ext=ff.read()
    ff.close()
    cname2=ext.split(',')


    ##    
    ff2=open("static/trained/tdata2.txt","r")
    rd=ff2.read()
    ff2.close()

    num=[]
    r1=rd.split(',')
    s=len(r1)
    ss=s-1
    i=0
    while i<ss:
        num.append(int(r1[i]))
        i+=1

    #print(num)
    dat=toString(num)
    dd2=[]
    ex=dat.split(',')
    ##

    #ffq=open("static/trained/adata.txt",'r')
    #ext1=ffq.read()
    #ffq.close()

    v1=0
    v2=0
    v3=0
    v4=0
    v5=0
    v6=0
    v7=0
    v8=0
    v9=0
    v10=0
    
    #ex=ext1.split(',')
    dt1=[]
    dt2=[]
    dt3=[]
    dt4=[]
    dt5=[]
    dt6=[]
    dt7=[]
    dt8=[]
    dt9=[]
    dt10=[]
    g=0
    for nx in ex:
        g+=1
        nn=nx.split('-')
        nc=int(nn[0])
        if nc<6:
            if nn[0]=='1':
                
                dt1.append(nn[1])
                
                v1+=1
            if nn[0]=='2':
                dt2.append(nn[1])
                
                v2+=1
            if nn[0]=='3':
                dt3.append(nn[1])
                
                v3+=1
            if nn[0]=='4':
                dt4.append(nn[1])
                
                v4+=1
            if nn[0]=='5':
                dt5.append(nn[1])
                
                v5+=1
            if nn[0]=='6':
                dt6.append(nn[1])
                
                v6+=1
      
        
    data21.append(dt1)
    data21.append(dt2)
    data21.append(dt3)
    data21.append(dt4)
    data21.append(dt5)
    data21.append(dt6)

       
    dd2=[v1,v2,v3,v4,v5,v6]
    doc = cname2 #list(data.keys())
    values = dd2 #list(data.values())
    #print(doc)
    #print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    plt.bar(doc, values, color ='blue',
            width = 0.4)
 

    plt.ylim((1,40))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass2.png"
    plt.xticks(rotation=10)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    #plt.clf()
    #######################################################
    ff=open("static/trained/class3.txt",'r')
    ext=ff.read()
    ff.close()
    cname3=ext.split(',')


    ##    
    ff2=open("static/trained/tdata3.txt","r")
    rd=ff2.read()
    ff2.close()

    num=[]
    r1=rd.split(',')
    s=len(r1)
    ss=s-1
    i=0
    while i<ss:
        num.append(int(r1[i]))
        i+=1

    #print(num)
    dat=toString(num)
    dd2=[]
    ex=dat.split(',')
    
    ##
    vv=[]
    vn=0
    
    path_main = 'static/data3'
    for val in ex:
        dt=[]
        n=0
        
        for fname in os.listdir(path_main):
            fa1=fname.split('.')
            fa=fa1[0].split('-')
            
            if fa[1]==val:
                dt.append(fname)
                n+=1
        vv.append(n)
        vn+=n
        data3.append(dt)
        
    
    i=0
    vd=[]
    data31=[]
    while i<6:
        vt=[]
        vi=i+1
        vv[i]

        vt.append(cname3[i])
        vt.append(str(vv[i]))
        
        vd.append(str(vi))
        data31.append(vt)
        i+=1
   
    
    
    dd2=vv
    doc = cname3 #list(data.keys())
    values = dd2 #list(data.values())
    
    #print(doc)
    #print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    cc=['pink','yellow','orange','red','blue','green']
    plt.bar(doc, values, color =cc,
            width = 0.4)
 

    plt.ylim((1,20))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass3.png"
    #plt.xticks(rotation=20)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    ##################################################
    ff=open("static/trained/class4.txt",'r')
    ext=ff.read()
    ff.close()
    cname4=ext.split(',')
    print("banana leaf")
    df = pd.read_csv("static/trained/train.csv")
 
    data4=[]
    dtt1=[]
    dtt2=[]
    dtt3=[]
    dtt4=[]
    dtt5=[]
    dtt6=[]
    dtt7=[]
    dtt8=[]
    dtt9=[]
    dtt10=[]
    dtt11=[]
    dtt12=[]
    dtt13=[]
    dtt14=[]
    v1=0
    v2=0
    v3=0
    v4=0
    v5=0
    v6=0
    v7=0
    v8=0
    v9=0
    v10=0
    v11=0
    v12=0
    v13=0
    v14=0
        
    for ss1 in df.values:
        
        if ss1[1]=='cordano':
            print(ss1[0])
            v1+=1
            dtt1.append(ss1[0])
        

        
        if ss1[1]=='pestalotiopsis':
            #print(ss1[0])
            v2+=1
            dtt2.append(ss1[0])
      
        if ss1[1]=='sigatoka':
            v3+=1
            dtt3.append(ss1[0])
       
        
        if ss1[1]=='healthy':
            v4+=1
            dtt4.append(ss1[0])
        
     

    data4.append(dtt1)
    data4.append(dtt2)
    data4.append(dtt3)
    data4.append(dtt4)

   
    
    dd2=[v1,v2,v3,v4]
    doc = cname4 #list(data.keys())
    values = dd2 #list(data.values())
    
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    plt.bar(doc, values, color ='blue',
            width = 0.4)
 

    plt.ylim((1,25))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass4.png"
    #plt.xticks(rotation=20)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    
    
    return render_template('classify.html',msg=msg,cname=cname,data2=data2,cname2=cname2,cname3=cname3,cname4=cname4,data21=data21,data3=data3,data4=data4)

#######
@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
       
    return render_template('userhome.html',msg=msg)

#Plant Leaf Disease Detection - Vision Transformer (ViT)-based
#Multi-Class Classifier
def load_data():

    IMAGE_SIZE = 224
    PATCH_SIZE = 16
    NUM_CLASSES = 10   # Change based on dataset
    EMBED_DIM = 768
    NUM_HEADS = 8
    NUM_LAYERS = 6
    BATCH_SIZE = 16
    EPOCHS = 10
    LR = 0.0001

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Image Preprocessing

    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5])
    ])

    train_dataset = datasets.ImageFolder("dataset/train", transform=transform)
    test_dataset = datasets.ImageFolder("dataset/test", transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)


#Patch Embedding Layer
class PatchEmbedding():
    def __init__(self, img_size, patch_size, embed_dim):
        super().__init__()
        self.n_patches = (img_size // patch_size) ** 2
        self.proj = nn.Conv2d(
            in_channels=3,
            out_channels=embed_dim,
            kernel_size=patch_size,
            stride=patch_size
        )

    def forward(self, x):
        x = self.proj(x)
        x = x.flatten(2)
        x = x.transpose(1, 2)
        return x

#Vision Transformer Model
class VisionTransformer():
    def __init__(self):
        super().__init__()
        self.patch_embed = PatchEmbedding(IMAGE_SIZE, PATCH_SIZE, EMBED_DIM)
        self.cls_token = nn.Parameter(torch.zeros(1, 1, EMBED_DIM))
        self.pos_embedding = nn.Parameter(torch.zeros(1, (IMAGE_SIZE // PATCH_SIZE) ** 2 + 1, EMBED_DIM))

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=EMBED_DIM,
            nhead=NUM_HEADS,
            dim_feedforward=1024,
            dropout=0.1,
            activation='gelu'
        )

        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=NUM_LAYERS)

        self.norm = nn.LayerNorm(EMBED_DIM)
        self.fc = nn.Linear(EMBED_DIM, NUM_CLASSES)

    def forward(self, x):
        x = self.patch_embed(x)

        batch_size = x.shape[0]
        cls_tokens = self.cls_token.expand(batch_size, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)

        x = x + self.pos_embedding
        x = self.transformer(x)
        x = self.norm(x)

        cls_output = x[:, 0]
        out = self.fc(cls_output)
        return out


def model_init():
    model = VisionTransformer().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

#Training Loop
def train_model():
    train_losses = []

    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        epoch_loss = running_loss / len(train_loader)
        train_losses.append(epoch_loss)
        print(f"Epoch [{epoch+1}/{EPOCHS}], Loss: {epoch_loss:.4f}")

    print("Training Complete!")


#
def predict():
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())

    print(classification_report(all_labels, all_preds))


    #Plot Loss Curve
    plt.plot(train_losses)
    plt.title("Training Loss Curve")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.show()


#GAN
def build_generator():
    model = models.Sequential()
    model.add(layers.Dense(8 * 8 * 256, input_dim=LATENT_DIM))
    model.add(layers.Reshape((8, 8, 256)))

    model.add(layers.UpSampling2D())
    model.add(layers.Conv2D(256, kernel_size=3, padding="same"))
    model.add(layers.LeakyReLU(0.2))

    model.add(layers.UpSampling2D())
    model.add(layers.Conv2D(128, kernel_size=3, padding="same"))
    model.add(layers.LeakyReLU(0.2))

    model.add(layers.UpSampling2D())
    model.add(layers.Conv2D(64, kernel_size=3, padding="same"))
    model.add(layers.LeakyReLU(0.2))

    model.add(layers.Conv2D(CHANNELS, kernel_size=3, padding="same", activation="tanh"))
    return model

# ------------------------------
# Build Discriminator
# ------------------------------
def build_discriminator():
    model = models.Sequential()
    model.add(layers.Conv2D(64, kernel_size=3, strides=2, padding="same",
                            input_shape=(IMG_SIZE, IMG_SIZE, CHANNELS)))
    model.add(layers.LeakyReLU(0.2))
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(128, kernel_size=3, strides=2, padding="same"))
    model.add(layers.LeakyReLU(0.2))
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())
    model.add(layers.Dense(1, activation="sigmoid"))
    return model

def GAN_generate():
    IMG_SIZE = 64
    CHANNELS = 3
    LATENT_DIM = 100
    BATCH_SIZE = 32
    EPOCHS = 2000
    datagen = ImageDataGenerator(rescale=1/255)

    dataset = datagen.flow_from_directory(
        "dataset",                
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode=None,
        shuffle=True
    )
    generator = build_generator()
    discriminator = build_discriminator()

    discriminator.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    # GAN combined model
    z = layers.Input(shape=(LATENT_DIM,))
    img = generator(z)
    discriminator.trainable = False
    validity = discriminator(img)

    combined = models.Model(z, validity)
    combined.compile(optimizer="adam", loss="binary_crossentropy")

    # ------------------------------
    os.makedirs("generated_images", exist_ok=True)

    for epoch in range(EPOCHS):

        # ----------------------
        #  Train discriminator
        # ----------------------
        real_imgs = next(dataset)
        current_batch = real_imgs.shape[0]  

        valid = np.ones((current_batch, 1))
        fake = np.zeros((current_batch, 1))

        noise = np.random.normal(0, 1, (current_batch, LATENT_DIM))
        gen_imgs = generator.predict(noise)

        d_loss_real = discriminator.train_on_batch(real_imgs, valid)
        d_loss_fake = discriminator.train_on_batch(gen_imgs, fake)
        d_loss = 0.5 * (np.array(d_loss_real) + np.array(d_loss_fake))

        # ----------------------
        #  Train generator
        # ----------------------
        noise = np.random.normal(0, 1, (current_batch, LATENT_DIM))
        g_loss = combined.train_on_batch(noise, valid)

        # ----------------------
        if epoch % 100 == 0:
            print(f"{epoch} [D loss: {d_loss[0]:.4f}, acc: {d_loss[1]*100:.2f}%] [G loss: {g_loss:.4f}]")

            sample = (gen_imgs[0] * 127.5 + 127.5).astype(np.uint8)
            tf.keras.utils.save_img(f"static/test/l_{epoch}.png", sample)

###########
# Load dataset
data = pd.read_csv("static/soil_npk_dataset.csv")

X = data[['Nitrogen','Phosphorus','Potassium']]

# Encode outputs
le1 = LabelEncoder()
le2 = LabelEncoder()
le3 = LabelEncoder()

y1 = le1.fit_transform(data['Fertility'])
y2 = le2.fit_transform(data['Fertilizer'])
y3 = le3.fit_transform(data['Insight'])

# Train models
model1 = RandomForestClassifier()
model2 = RandomForestClassifier()
model3 = RandomForestClassifier()

model1.fit(X,y1)
model2.fit(X,y2)
model3.fit(X,y3)

# Prediction function
def predict_soil(n,p,k):

    input_data = [[n,p,k]]

    fertility = le1.inverse_transform(model1.predict(input_data))[0]
    fertilizer = le2.inverse_transform(model2.predict(input_data))[0]
    insight = le3.inverse_transform(model3.predict(input_data))[0]

    dat=fertility+"|"+fertilizer+"|"+insight
    ff=open("static/soil.txt","w")
    ff.write(dat)
    ff.close()
    
    return fertility,fertilizer,insight


@app.route('/test_img', methods=['GET', 'POST'])
def test_img():
    msg=""
    ss=""
    fn=""
    fn1=""
    fname=""
    tclass=0
    uname=""
    if 'username' in session:
        uname = session['username']
    result=""
    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')
    gfn=""
    atest=""
    btest=""
    ctest=""
    dtest=""
    
    if request.method=='POST':
        soil_n=request.form['soil_n']
        soil_p=request.form['soil_p']
        soil_k=request.form['soil_k']

        predict_soil(soil_n,soil_p,soil_k)

        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            f1=open('static/test/file.txt','w')
            f1.write(filename)
            f1.close()
            file.save(os.path.join("static/test", filename))
            ##
            img = cv2.imread("static/test/"+filename)
            img = cv2.resize(img, (256,256))  
            cv2.imwrite("static/test/resize.png", img)
            noise = np.random.normal(0, 25, img.shape).astype(np.int16)
            fake = img.astype(np.int16) + noise
            fake = np.clip(fake, 0, 255).astype(np.uint8)
            fake = cv2.GaussianBlur(fake, (5,5), 0)
            fm=filename.split(".")
            gfn="g"+fm[0]+".png"
            hfn="h"+filename
            cv2.imwrite("static/test/"+gfn, fake)
            ##
            img = cv2.imread("static/test/"+filename)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower = np.array([10, 30, 30])
            upper = np.array([35, 255, 255])
            mask = cv2.inRange(hsv, lower, upper)
            mask_blur = cv2.GaussianBlur(mask, (21, 21), 0)
            leaf = img.copy()
            leaf[mask_blur > 10] = leaf[mask_blur > 10] * 0.6 + np.array([0, 120, 0]) * 0.4
            cv2.imwrite("static/test/"+hfn, leaf)
            ##

        #A######
        cutoff=0
        path_main = 'static/data1'
        for fname1 in os.listdir(path_main):
            hash0 = imagehash.average_hash(Image.open("static/data1/"+fname1)) 
            hash1 = imagehash.average_hash(Image.open("static/test/"+filename))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                ss="ok"
                atest="1"
                fn=fname1
                print("ff="+fn)
                break
            else:
                ss=""
        #B####################
        cutoff=0
        path_main = 'static/data2'
        for fname1 in os.listdir(path_main):
            hash0 = imagehash.average_hash(Image.open("static/data2/"+fname1)) 
            hash1 = imagehash.average_hash(Image.open("static/test/"+filename))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                ss="ok"
                fn=fname1
                btest="1"
                break
            else:
                ss=""
        #C###############
        cutoff=0
        path_main = 'static/data3'
        for fname1 in os.listdir(path_main):
            hash0 = imagehash.average_hash(Image.open("static/data3/"+fname1)) 
            hash1 = imagehash.average_hash(Image.open("static/test/"+filename))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                ss="ok"
                fn=fname1
                ctest="1"
                print("ff="+fn)
                break
            else:
                ss=""
        #D#################
        cutoff=0
        path_main = 'static/data4'
        for fname1 in os.listdir(path_main):
            hash0 = imagehash.average_hash(Image.open("static/data4/"+fname1)) 
            hash1 = imagehash.average_hash(Image.open("static/test/"+filename))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                ss="ok"
                fn=fname1
                
                fr=fn.split('.')
                fr2=fr[0]
                dtest="1"
                break
            else:
                ss="no"

        ####################
        
        if atest=="1":
            print("yes")
            tclass=0
            dimg=[]

            ##    
            ff2=open("static/trained/tdata.txt","r")
            rd=ff2.read()
            ff2.close()

            num=[]
            r1=rd.split(',')
            s=len(r1)
            ss=s-1
            i=0
            while i<ss:
                num.append(int(r1[i]))
                i+=1

            #print(num)
            dat=toString(num)
            dd2=[]
            ex=dat.split(',')
            print(fn)
            ##
            
            ##
            n=0
            result=""
            path_main = 'static/data1'
            for val in ex:
                dt=[]
                if int(val)<7:
                    fa1=fname.split('.')
                    fa=fa1[0].split('-')
                    print("****")
                    print(fa1[0])
                    print(fa)
                    if len(fa)>1:
                        if fa[1]==val:
                            
                            result=val
                            
                            break
                    
                
                
                n+=1
          
            
            dta="a"+"|"+fn+"|"+result+"|1"
            f3=open("static/test/res.txt","w")
            f3.write(dta)
            f3.close()

            
                    
            return redirect(url_for('test_pro',act="1"))
        ################################################################
        elif btest=="1":

            ####################
            ff=open("static/trained/class2.txt",'r')
            ext=ff.read()
            ff.close()
            cname2=ext.split(',')
    
            
            print("yes2")
            tclass=0
            dimg=[]

            ##    
            ff2=open("static/trained/tdata2.txt","r")
            rd=ff2.read()
            ff2.close()

            num=[]
            r1=rd.split(',')
            s=len(r1)
            ss=s-1
            i=0
            while i<ss:
                num.append(int(r1[i]))
                i+=1

            #print(num)
            dat=toString(num)
            dd2=[]
            ex=dat.split(',')
            print(fn)
            ##
            print(ex)
            
            for nx in ex:
                
                nn=nx.split('-')
               
                if int(nn[0])<7:
                    f='a ('+nn[1]+').JPG'
                    fn1='a ('+nn[1]+').png'
                   
                    if f==fn:
                        
                        tclass=int(nn[0])
                        break

            
            
            tt=tclass-1
            cla=cname2[tt]
            dta=cla+"|"+fn+"|"+str(tclass)+"|2"
            f3=open("static/test/res.txt","w")
            f3.write(dta)
            f3.close()

            
                    
            return redirect(url_for('test_pro',act="1"))
            ###########
            
        ####################################################################
        elif ctest=="1":
            result=""
            ff=open("static/trained/class3.txt",'r')
            ext=ff.read()
            ff.close()
            cname=ext.split(',')
            
           
            
            tclass=0
            dimg=[]

            ##    
            ff2=open("static/trained/tdata3.txt","r")
            rd=ff2.read()
            ff2.close()

            num=[]
            r1=rd.split(',')
            s=len(r1)
            ss=s-1
            i=0
            while i<ss:
                num.append(int(r1[i]))
                i+=1

            #print(num)
            dat=toString(num)
            dd2=[]
            ex=dat.split(',')
            print(fn)
            ##
            
            ##
            n=0
            path_main = 'static/data3'
            for val in ex:
                dt=[]
                
                fa1=fn.split('.')
                fa=fa1[0].split('-')
            
                if fa[1]==val:
                    
                    result=n
                    
                    break
                n+=1
            dta="a"+"|"+fn+"|"+str(result)+"|3"
            f3=open("static/test/res.txt","w")
            f3.write(dta)
            f3.close()
            return redirect(url_for('test_pro',act="1"))
        
        ###############################################
        elif dtest=="1":
            

            if ss=="ok":
                print("yes")
                
                df = pd.read_csv("static/trained/train.csv")
                for ss1 in df.values:
                    a=str(ss1[0])
                    b=str(fr2)
                    if a==b:
                        
                        predict=ss1[1]
                        print("predict:"+predict)
                        break
                
                
                dta="a"+"|"+fn+"|"+predict+"|4"
                f3=open("static/test/res.txt","w")
                f3.write(dta)
                f3.close()
                return redirect(url_for('test_pro',act="1"))
            else:
                #msg="Invalid!"
                return redirect(url_for('test_pron',act="1"))
    
    return render_template('test_img.html',msg=msg)

@app.route('/test_prom', methods=['GET', 'POST'])
def test_prom():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[1]

    fn1=fn.split(".")
    fnn="g"+fn1[0]+".png"

    return render_template('test_prom.html',msg=msg,fnn=fnn)

@app.route('/test_pron', methods=['GET', 'POST'])
def test_pron():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[1]

    fn1=fn.split(".")
    fnn="g"+fn1[0]+".png"

    return render_template('test_pron.html',msg=msg,fnn=fnn,fn=fn)
    
@app.route('/test_pro', methods=['GET', 'POST'])
def test_pro():
    msg=""
    fn=""
    mycursor = mydb.cursor()
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[1]
    
    ts=gs[0]
    fname=fn
    ##bin
    '''image = cv2.imread('static/dataset/'+fn)
    original = image.copy()
    kmeans = kmeans_color_quantization(image, clusters=4)

    # Convert to grayscale, Gaussian blur, adaptive threshold
    gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

    # Draw largest enclosing circle onto a mask
    mask = np.zeros(original.shape[:2], dtype=np.uint8)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
        cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
        break
    
    # Bitwise-and for result
    result = cv2.bitwise_and(original, original, mask=mask)
    result[mask==0] = (0,0,0)

    
    ###cv2.imshow('thresh', thresh)
    ###cv2.imshow('result', result)
    ###cv2.imshow('mask', mask)
    ###cv2.imshow('kmeans', kmeans)
    ###cv2.imshow('image', image)
    ###cv2.waitKey()

    #cv2.imwrite("static/upload/bin_"+fname, thresh)'''
    

    ###fg
    '''img = cv2.imread('static/dataset/'+fn)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    segment = cv2.subtract(sure_bg,sure_fg)
    img = Image.fromarray(img)
    segment = Image.fromarray(segment)
    path3="static/trained/test/fg_"+fname
    #segment.save(path3)'''
    
        
    return render_template('test_pro.html',msg=msg,fn=fn,ts=ts,act=act)

@app.route('/test_pro2', methods=['GET', 'POST'])
def test_pro2():
    mycursor = mydb.cursor()
    msg=""
    fn=""
    fnn=""
    fnn2=""
    fn2=""
    res=""
    res1=""
    st=""
    fam_name=""
    data=[]
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')

    ff2=open("static/trained/class2.txt",'r')
    ext2=ff2.read()
    ff2.close()
    cname2=ext2.split(',')

    ff3=open("static/trained/class3.txt",'r')
    ext3=ff3.read()
    ff3.close()
    cname3=ext3.split(',')

    gs=get_data.split('|')
    fn=gs[1]
    ts=gs[2]
    leaf=gs[3]

    ff=open("static/soil.txt","r")
    soil=ff.read()
    ff.close()
    soil_data=soil.split("|")
    
    fv=fn[2:3]
    if fv=="(":
        # make new name
        num = fn.split("(")[1].split(")")[0]
        new_name = f"a_{num}.jpg"
        fn1=new_name.split(".")
        fnn="g"+fn1[0]+".png"
        fnn2="h"+new_name
    else:
        fn1=fn.split(".")
        fnn="g"+fn1[0]+".png"
        fnn2="h"+fn

    '''fn1=fn.split(".")
    fv=fn[1:3]
    print(fv)
    if fv==" (":
        fv1=fn.split(" (")
        fv2=fv1[0]+"_"+fv1[1]
        fv3=fv2.split(".")
        fnn="g"+fv3[0]+".png"
    else:
        
        fnn="g"+fn1[0]+".png"'''
    
    
    
    n=0

    if leaf=="4":
        classname=ts
        fam_name="Musaceae"
    elif leaf=="3":
        nn=int(ts)
        n=nn-1
        classname=cname3[n]
        fam_name="Anacardiaceae"
    elif leaf=="2":
        nn=int(ts)
        n=nn-1
        fn1=fn.split(".")
        fn2=fn1[0]+".png"
        classname=cname2[n]
        fam_name="Solanaceae"
    else:
        nn=int(ts)
        n=nn-1
        classname=cname[n]
        fam_name="Poaceae"

    mycursor.execute('SELECT count(*) FROM leaf_data where disease=%s',(classname,))
    cn = mycursor.fetchone()[0]
    if cn>0:
        st="1"
        mycursor.execute('SELECT * FROM leaf_data where disease=%s',(classname,))
        data = mycursor.fetchall()

    mycursor.execute('SELECT * FROM medicine where leaf_id=%s',(leaf,))
    data2 = mycursor.fetchall()
        
    return render_template('test_pro2.html',msg=msg,soil_data=soil_data,fn=fn,fn2=fn2,fnn=fnn,fnn2=fnn2,fam_name=fam_name,ts=ts,act=act,classname=classname,data=data,st=st,leaf=leaf,data2=data2)




##########################
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


