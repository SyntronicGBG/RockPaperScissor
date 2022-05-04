import os
import sys 

import numpy as np
import matplotlib.pyplot as plt
import cv2
import pickle
import mediapipe as mp
from tqdm import tqdm

from tensorflow import keras
from sklearn.model_selection import StratifiedKFold, KFold

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def save_mediapipe_data():
    path = 'data/kaggle_dataset/'

    X = []
    Y = []
    T = []
    hand_signs = ['rock','paper','scissors']
    one_hot_encoding = {'rock':[1,0,0], 'paper':[0,1,0],'scissors':[0,0,1]}
    labels = {'rock':1, 'paper':2,'scissors':3}


    for hand_sign in (hand_signs):
        images = os.listdir(path+hand_sign)
        for image in tqdm(images):
            img = cv2.imread(path+hand_sign+'/'+image,1)
            
            
            imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imageRGB)
            landmarks = results.multi_hand_landmarks
            coordinates = np.zeros(shape=(21,2))
            if landmarks:
                for i, landmark in enumerate(landmarks[0].landmark):
                    coordinates[i,0] = landmark.x
                    coordinates[i,1] = landmark.y
                
                X.append(coordinates)
                T.append(labels[hand_sign]) 
                Y.append(one_hot_encoding[hand_sign])

    X = np.array(X)
    T = np.array(T)
    Y = np.array(Y)

    skf = StratifiedKFold(n_splits=5)
    for train, test in skf.split(X,T):
        break

    pickle.dump([X[train], Y[train]], open('mediapipe_train_local.pckl','wb'))
    pickle.dump([X[test], Y[test]], open('mediapipe_test_local.pckl','wb'))

class DataGenerator(keras.utils.Sequence):
    def __init__(self, data, labels, scaling=0.5):
        self.batch_size=32
        self.data = data
        self.labels = labels
        self.scaling = scaling
        self.shuffle = True
        self.on_epoch_end()
        
    def on_epoch_end(self):
        self.indexes = np.arange(len(self.labels))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __len__(self):
        return int(np.floor(len(self.data)/self.batch_size))
    
    def __getitem__(self,index):
        batch_index = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        data_batch = self.data[batch_index]*(1 + np.random.uniform(-self.scaling,self.scaling, size=self.batch_size)[:, None])
        
        label_batch = self.labels[batch_index]

        return data_batch,label_batch
    
def transform_to_invariant_coordinates(coordinates):
    if len(coordinates.shape) == 3:
        new_coordinates = []
        for coord in coordinates:
            new_coordinates.append(np.abs(coord[1:,:]-coord[0,:]))
        return np.sqrt(np.sum(np.array(new_coordinates)**2,axis=-1))
    else:
        return np.sqrt(np.sum(np.abs(coordinates[1:,:]-coordinates[0,:])**2, axis=-1))
    
def train_image_data_model():
    [images, targets]=pickle.load(open('train.pckl','rb'))

    skf = StratifiedKFold(n_splits=5)

    integer_targets = np.argmax(targets,axis=1)
    for train, test in skf.split(images,integer_targets):
        break

    X_train = images[train]
    X_val = images[test]
    y_train = targets[train]
    y_val = targets[test]
    
    inputs = keras.Input(shape=(200,300,3))
    x=keras.layers.Conv2D(32,(20,20))(inputs)
    x=keras.layers.MaxPooling2D((8,8))(x)
    x=keras.layers.Flatten()(x)

    outputs=keras.layers.Dense(3, activation='softmax')(x)
    model = keras.Model(inputs=inputs, outputs=outputs, name="test_model")

    print(model.summary())

    model.compile(loss=keras.losses.categorical_crossentropy,metrics=['accuracy'])
    history = model.fit(X_train,y_train,epochs=10,validation_data=(X_val,y_val),batch_size=10)
    return model, history

def train_mediapipe_data_model():
    [images, targets]=pickle.load(open('mediapipe_train_local.pckl','rb'))
    skf = StratifiedKFold(n_splits=5)
    integer_targets = np.argmax(targets,axis=1)
    for train, test in skf.split(images,integer_targets):
        break

    X_train = images[train]
    X_val = images[test]
    y_train = targets[train]
    y_val = targets[test]

    X_train = transform_to_invariant_coordinates(X_train)
    X_val = transform_to_invariant_coordinates(X_val)
 

    train_generator = DataGenerator(X_train, y_train, scaling=0)
    val_generator = DataGenerator(X_val, y_val, scaling=0)
    
    inputs = keras.Input(shape=(20))
    x=keras.layers.Flatten()(inputs)

    outputs=keras.layers.Dense(3, activation='softmax')(x)
    model = keras.Model(inputs=inputs, outputs=outputs, name="test_model")

    model.summary()
    model.compile(loss=keras.losses.categorical_crossentropy,metrics=['accuracy'])
    #history = model.fit(X_train,y_train,epochs=50,validation_data=(X_val,y_val),batch_size=10)
    history = model.fit_generator(generator = train_generator,validation_data=val_generator, epochs=50)

    
    return model, history

def display_hand_on_webcam():
    
    model = keras.models.load_model('test_model_local')
    model.summary()
    vid = cv2.VideoCapture(0)
    while True:
        ret, frame = vid.read()
        
        imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imageRGB)
        if results.multi_hand_landmarks:
            
            coordinates = np.zeros(shape=(1,21,2))
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                for i, landmark in enumerate(hand_landmarks.landmark):
                    coordinates[0,i,0] = landmark.x
                    coordinates[0,i,1] = landmark.y
                    
            inv_coord = transform_to_invariant_coordinates(coordinates)
            sign = ['rock','paper','scissors']
            predict = model.predict(inv_coord)
            print(predict, sign[np.argmax(predict)])
        cv2.imshow('MediaPipe Hands', cv2.flip(frame, 1))
        if cv2.waitKey(1) == ord('q'):
            break  
    vid.release()
    cv2.destroyAllWindows()
    
    
#save_mediapipe_data()
#model, history = train_mediapipe_data_model()
#model.save('test_model_local')

#display_hand_on_webcam()