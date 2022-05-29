# TOMB RUNNER

Play Tomb runner game using face movements .

Usage opencv harcassade classifier and kcf for face detection and movement recognition and pyatogui for simulating actions .

Reason for not deploying :
Opencv tries to open the camera on whatever device the app is running on. 
Code in current state makes use of webcam if available on server side not client side.
So when app is run locally on a laptop Video Streaming through webcam is possible. But if it's deployed to a cloud, the 
app is stored in a data center somewhere which obviously doesn't have web camera connected to it and hence it doesn't work.


Installation :

pip install -r requirements.txt

run app.py
