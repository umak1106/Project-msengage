# Health++

Health++ is an app which uses opencv and other machine learning based algorithms to provide the following features .<br>
It is deployed on streamlit cloud.<br>
Link to the deployed app : https://share.streamlit.io/uk1106/repo2/main/app.py

## Installation 

git clone this repo 

OR

git clone https://github.com/Uk1106/Repo2.git <br>
Uk1106 is my 2nd github account .

```pip install -r requirements.txt```

```streamlit run app.py```


## Face Mask Detection :
Caffe model is the pre-trained deep learning model used to detect faces.<br>
For Face mask detection I have used pre-trained keras CNN model as shown in the article [here](https://pyimagesearch.com/2020/05/04/covid-19-face-mask-detector-with-opencv-keras-tensorflow-and-deep-learning/).
<br>OpencV is used to detect faces and CNN model to classify if mask  is present or not .

app5 file -> code for mask detection 

## Plant Disease Classification 
Using openCV to detect images of plant disease and usage of CNN / Conv net model for plant disease prediction .<br>
Steps for building Conv net :
Convolution Operation<br>
ReLU Layer (Rectified Linear Unit)<br>
Pooling Layer (Max Pooling)<br>
Flattening<br>
Fully Connected Layer<br>

app1 file -> code for plant disease 


## Health 
Usage of KNN , SVC , Decision tree and random forest for prediction of BP , Diabetes and heart disease . <br>
 app 3 file  -> code 
 
 ## Mental Health
 
 app 2 file -> code <br>
 Usage of KNN , SVC , Logistic Regression , Decision tree , Random forest , Naive Bayes etc for prediction of Mental health .<br>
 
 





