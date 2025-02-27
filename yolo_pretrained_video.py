# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 23:56:29 2022

@author: lenovo
"""

import cv2
import numpy as np

cap = cv2.VideoCapture("videos/people.mp4")
#print(img)

while True:
    ret, frame = cap.read()
    
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    frame_blob = cv2.dnn.blobFromImage(frame, 1/255, (416,416), swapRB=True, crop = False)

    labels = ["person","bicycle","car","motorcycle","airplane","bus","train","truck","boat",
                    "trafficlight","firehydrant","stopsign","parkingmeter","bench","bird","cat",
                    "dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack",
                    "umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sportsball",
                    "kite","baseballbat","baseballglove","skateboard","surfboard","tennisracket",
                    "bottle","wineglass","cup","fork","knife","spoon","bowl","banana","apple",
                    "sandwich","orange","broccoli","carrot","hotdog","pizza","donut","cake","chair",
                    "sofa","pottedplant","bed","diningtable","toilet","tvmonitor","laptop","mouse",
                    "remote","keyboard","cellphone","microwave","oven","toaster","sink","refrigerator",
                    "book","clock","vase","scissors","teddybear","hairdrier","toothbrush"]


    colors = ["0, 255, 255", "0,0,255", "255,0,0", "255,255,0", "0,255,0"]
    colors = [np.array(color.split(",")).astype("int") for color in colors]
    colors = np.array(colors)
    colors = np.tile(colors,(18,1))


    model=cv2.dnn.readNetFromDarknet("pretrained_model/yolov3.cfg", "pretrained_model/yolov3.weights")
    layers = model.getLayerNames()
    output_layer=[layers[layer-1] for layer in model.getUnconnectedOutLayers()]
    
    model.setInput(frame_blob)
    
    detection_layers = model.forward(output_layer)

    ########## NON-MAXIMUM SUPRESSION - OPERATION 1 ##########
    
    ids_list = []
    boxes_list = []
    confidences_list = []
    
    
    
    
    
    
    
    
    ########## END OF OPERATION 1 ##########

    
    for detection_layer in detection_layers:
        for object_detection in detection_layer:
            
            scores = object_detection[5:]
            predicted_id = np.argmax(scores)
            confidence = scores[predicted_id]
            
            if confidence > 0.20:
                label = labels[predicted_id]
                bounding_box = object_detection[0:4] * np.array([frame_width,frame_height,frame_width,frame_height])
                (box_center_x,box_center_y,box_width,box_height) = bounding_box.astype("int")
                
                start_x = int(box_center_x - (box_width/2))
                start_y = int(box_center_y - (box_height/2))
                
                ######### NON-MAXIMUM SUPRESSION - OPERATION 2 ##########
                # For döngüsünde tespit edilen her şey boş listelerin içine yollandı.
                ids_list.append(predicted_id)
                confidences_list.append(float(confidence))
                boxes_list.append([start_x,start_y,int(box_width),int(box_height)])

         
            ########## END OF OPERATION 2 ##########
            
######### NON-MAXIMUM SUPRESSION - OPERATION 3 ##########
            
    max_ids = cv2.dnn.NMSBoxes(boxes_list,confidences_list,0.5,0.4) #max güvenilirliğe sahip boxları max_ids içine sakladık.
    
    #tek tek tüm id'lere erismek icin for döngüsü kullandık
    for max_id in max_ids:
        max_class_id = max_id
        box = boxes_list[max_class_id]
        
        start_x = box[0]
        start_y = box[1]
        box_width = box[2]
        box_height = box[3]
        
        predicted_id = ids_list[max_class_id]
        label = labels[predicted_id]
        confidence = confidences_list[max_class_id]
        
        
             
    ########## END OF OPERATION 3 ##########
    
    
        end_x = start_x + box_width
        end_y = start_y + box_height
                
        box_color = colors[predicted_id]
        box_color = [int(each) for each in box_color]
                
                
        label = "{}: {:.2f}%".format(label, confidence*100)
        print("predicted object {}".format(label))
                
        cv2.rectangle(frame,(start_x,start_y),(end_x,end_y),box_color,1)
        cv2.putText(frame,label,(start_x,start_y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,box_color,1)
                
    
    cv2.imshow("Detection Window", frame)
    
    if cv2.waitKey(100) & 0xFF == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        