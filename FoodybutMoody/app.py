import random, os, io, base64
from flask import Flask, render_template, request, jsonify
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


KEY = "bb71dc93bc25491fb91041cf74f9f4d4"
ENDPOINT = "https://ok-try-2.cognitiveservices.azure.com/"
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


emotions = ['anger','neutral','disgust','fear','happiness','sadness','surprise']

#emotions is a dictionary that stores the percentages for 8 of these emotions and 
# best_emotions() returns the name of the emotion with the highest percentage.
def best_emotion(emotion):
    emotions = {}
    emotions['anger'] = emotion.anger
    emotions['disgust'] = emotion.disgust
    emotions['fear'] = emotion.fear
    emotions['happiness'] = emotion.happiness
    emotions['neutral'] = emotion.neutral
    emotions['sadness'] = emotion.sadness
    emotions['surprise'] = emotion.surprise
    return max(zip(emotions.values(), emotions.keys()))[1]

#moody dictionary suggests foods for the correct mood
moody={'sadness':{'Omega-3':['Salmon','Sardines','Oyesters','Walnut seeds','Mackerel'], \
        'Probiotics':['Yogurt', 'Kefir', 'Buttermilk', 'Natto', 'CHEESE'], \
        'Vitamin B':['Avocado', 'Egg', 'Spinach', 'CHICKEN', 'Tuna'], \
        'Vitamin D':['Cheese', 'Egg Yolks', 'Milk', 'Soy Milk', 'Orange Juice']},\
    'disgust':{'Detoxifying Food':['Artichokes','Broccoli','Sprouts','Blueberries','Apple','Ginger'], \
        'Detoxifying Drinks':['Pomegranate juice', 'Coconut Water', 'Honey Lemon Ginger Tea', 'Lemonade', 'Cucumber Mint Drink'], \
        'Low-calorie':['Greek yogurt', 'Watermelon', 'Chia seeds', 'Eggs', 'Berries']}, \
    'neutral':{'Fruits and Vegetables':['Dark-green Veggies', 'Sweet potatoes', 'Broccoli', 'Orange', 'Tomatoes'], \
        'Whole grains':['Barley', 'Oatmeal', 'Brown rice', 'Whole-wheat pasta', 'Whole-wheat crackers'], \
        'Dairy':['Low-fat milk', 'Low-fat yogurt', 'Soymilk', 'Cheese', 'Tofu'], \
        'Lean protein':['Nuts', 'Lean pork', 'Lean chicken', 'Lean turkey', 'Eggs']}, \
    'happiness':{'Protein':['Peanut butter', 'Eggs', 'Beans', 'Tofu', 'White meat'], \
        'Calcium':['Plain yogurt', 'Cereal from low-fat milk', 'Cheese', 'Kale', 'Cabbage'], \
            
        'Whole grains':['Brown rice', 'Popcorn', 'Wholegrain toast', 'Wholegrain biscuit', 'Barley pudding'], \
        'Vitamins & Minerals': ['Strawberries', 'Apples', 'Bananas', 'Raspberries', 'Mango']}, \
    'anger':{'Confections':['Dark chocolate', 'Maple-flavored gummies', 'Candy-infused trail mixes', 'Snack bars', 'Avocado chocolate bars'], \
        'Carbohydrates':['Apple', 'Banana', 'Sweet potato', 'Grapefruit', 'Pasta'], \

        'Protein':['Peanut butter', 'Protein bars', 'Greek yogurt', 'Chicken breast', 'Almonds'],
        'Modest amount of caffeine':['Green tea', 'Black tea', 'Chai tea', 'Chicory tea', 'Lemon tea']}, \
    'surprise':{'Antioxidants':['Dark chocolate', 'Leaf vegetable', 'Tomato', 'Berries', 'Onion' ], \
        'Zinc':['Oysters', 'Cashews', 'Beef', 'Eggs', 'Poultry (chickens, turkeys, ducks, geese)'], \
        'Vitamin C':['Oranges', 'Cabbage', 'Kiwi', 'Red/green/yellow pepper', 'Broccoli'], \

        'Omega-3':['Salmon','Sardines','Anchovies','Walnut seeds','Chia seeds']}}


emotion_messages={'anger':'Anger increases stress and carbohydrates and protein provide fuel for your body to aid in concentration.', \
    'neutral':'Health is wealth!Do not skip a healthy meal',\
    'disgust':'Detoxifying foods cleanse your body naturally and keep your immune systems healthy. These natural ingredients help alleviate your disgust.',\
    'happiness':'Protein, calcium, whole grains, and especially vitamins help to increase your serotonin levels and keep your emotions leveled.',\
    'sadness':'Omega-3, probiotics, vitamin B, and vitamin D elevate positive mood  and help achieve mental well being.',\
    'surprise':'Antioxidants lower your blood pressure, zinc helps you deal with stress, vitamin C calms you down, berries , dark choclate,coffee are all mood boosters'}


app = Flask(__name__)

#routing for the home page
@app.route('/')
def home():
    page_data = {
        'emotion' : random.choice(emotions)
    }
    return render_template('home.html', page_data = page_data)

#routing for result page
@app.route('/result', methods=['POST'])
def check_results():
    body = request.get_json()
    desired_emotion = body['emotion']

    image_bytes = base64.b64decode(body['image_base64'].split(',')[1])
    image = io.BytesIO(image_bytes)

    #this converts the binary image data into a stream
    faces = face_client.face.detect_with_stream(image,
                                                return_face_attributes=['emotion'])

    if len(faces) == 1:
        #returns info in JSON format given that there's no error
        detected_emotion = best_emotion(faces[0].face_attributes.emotion)

        display_message=f'You showed {detected_emotion}.'+'<br /> We recommend the following foods to boost your mood! <br />'
        
        num_count=1
        for i in moody[detected_emotion]:

            display_message+=f'{num_count}. {random.choice(moody[detected_emotion][i])} ({i}) <br />'
            num_count+=1

        display_message+=emotion_messages[detected_emotion]

        return jsonify({
            'message': display_message
        })

    else:
        return jsonify({
            'message': '☠️ ERROR: No faces detected'
        })

if __name__ == '__main__':
    app.run(debug=True)