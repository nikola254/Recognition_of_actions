import tensorflow as tf
import tensorflow.keras.models
import numpy as np
import cv2


path_to_model = "NN_acc_38"

model = tf.keras.models.load_model(path_to_model)

dicti = {0:"cartwheel",
1:"catch",
2:"clap",
3:"climb",
4:"dive",
5:"draw_sword",
6:"dribble",
7:"fencing",
8:"flic_flac",
9:"golf",
10:"handstand",
11:"hit",
12:"jump",
13:"pick",
14:"pour",
15:"pullup",
16:'push',
17:"pushup",
18:"shoot_ball",
19:"sit",
20:"situp",
21:"swing_baseball",
22:"sword_exercise",
23:"throw"
}


def getFrames(video_path):
    cap = cv2.VideoCapture(video_path)
    num = -1
    frames = []
    count_cadrs = 28
    while(cap.isOpened()):
        num += 1

        if num in [2, 4]:
            continue
        ret, frame = cap.read()
        if (ret == True):
            if num % 2 == 0:
                x_size = 144
                y_size = 144
                # Преобразование кадра в тензор
                frame = cv2.resize(frame, (x_size, y_size)) # Изменение размера кадра
                frame = frame / 255.0 # Нормализация пикселей
                frame = np.expand_dims(frame, axis=[0]) # Добавление измерения для тензора
                frames.append(frame)
        else:
            break
        if len(frames) == count_cadrs:
            #print('Попалось видео с недостатком кадров')
            break
    # Преобразование списка тензоров в тензор
    try:
        frames = np.concatenate(frames, axis=0)
    except ValueError:
        pass
    video_path = None
    return frames.reshape((1, 28, 144,144,3))




def predict(path_to_video):
    return dicti[np.argmax(model.predict(getFrames(path_to_video)))]

