import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
from parselmouth.praat import call, run_file
import requests
import scipy
from scipy.stats import binom
import numpy as np
import syllables
import os
# import whisper

cred = credentials.Certificate('key.json') 
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


def myspatc(m,p):
    # sound= p + "/"+m
    # print(sound)
    file_n= "./myspsolution.praat"   
    audio_file = "./" + m
    try:
        objects= run_file(file_n, -20, 2, 0.3, "yes",audio_file,"./", 80, 400, 0.01, capture_output=True)
        print("objects", objects)
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        z3=int(z2[3]) # will be the integer number 10
        z4=float(z2[3]) # will be the floating point number 8.3
        return(z3)

    except:
        z3=0
        print ("Try again the sound of the audio was not clear")
    return z3

def myspsr(m,p):
    # sound=p+"/"+m+".wav"
    file_n= "./myspsolution.praat"   
    audio_file = "./" + m
    try:
        objects= run_file(file_n, -20, 2, 0.3, "yes",audio_file,"./", 80, 400, 0.01, capture_output=True)
        # print (objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        z3=int(z2[2]) # will be the integer number 10
        z4=float(z2[3]) # will be the floating point number 8.3
        # print ("rate_of_speech=",z3,"# syllables/sec original duration")
        return(z3)
    except:
        z3=0
        print ("Try again the sound of the audio was not clear")
    return z3
def mysppaus(m,p):
    # sound=p+"/"+m+".wav"
    # sound=p+"/"+m
    # sourcerun=p+"/myspsolution.praat"
    # path=p+"/"
    # file_n="myspsolution.praat"
    file_n= "./myspsolution.praat"   
    audio_file = "./" + m
    try:
        objects= run_file(file_n, -20, 2, 0.3, "yes",audio_file,"./", 80, 400, 0.01, capture_output=True)
        # print (objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        z3=int(z2[1]) # will be the integer number 10
        z4=float(z2[3]) # will be the floating point number 8.3
        # print ("number_of_pauses=",z3)
        return(z3)
    except:
        z3=0
        print ("Try again the sound of the audio was not clear")
    return z3; 

def mysppron(m,p):
    file_n= "./myspsolution.praat"   
    audio_file = "./" + m
    try:
        objects= run_file(file_n, -20, 2, 0.3, "yes",audio_file,"./", 80, 400, 0.01, capture_output=True)
        # print (objects[0]) # This will print the info from the sound object, and objects[0] is a parselmouth.Sound object
        z1=str( objects[1]) # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z2=z1.strip().split()
        z3=int(z2[13]) # will be the integer number 10
        z4=float(z2[14]) # will be the floating point number 8.3
        db= binom.rvs(n=10,p=z4,size=10000)
        a=np.array(db)
        b=np.mean(a)*10/10
        #print ("Pronunciation Score= :%.2f" % (b))
        
    except:
        print ("Try again the sound of the audio was not clear")
        b = 0
    return (round(b, 2))


def analysis_ar(ar):
    if ar > 6:
        print("Try to speak clearly.")
    else:
        print("Clarity Score =" , round((ar/6)*10) )
    return(round((ar/6)*10))

def analysis_sr(sr): # 3 - 6
    # 
    # if sr>6:
    #     print("Speaking too fast.")
    # elif sr<3:
    #     print("Speaking too slow")
    # else:
    #     print("Speech rate is good.")
    # 
    if sr > 5:
        print("Please try to speak a bit slowly.")
    print("Speech rate Score = ", round((sr/5)*10))
    return(round((sr/5)*10))
def analysis_pauses(pauses): # 21.92 pauses per minute   or 21.92 in 60 seconds
    print("Pauses:" , pauses)
    return(pauses)

def readabiity_ease(filename):
    print('newfileame', filename)
    # filename = '/Users/laibairfan/flask/' + filename
    model = whisper.load_model("small.en")
    result = model.transcribe(filename, language = "en", fp16 = False)
    passage = result["text"]    
    # passage = "Mike and Morris lived in the same village. While Morris owned the largest jewellery shop in the village, Mike was a poor farmer. Both had large families with many sons, daughters-in-law and grandchildren. One fine day, Mike, tired of not being able to feed his family, decided to leave the village and move to the city where he was certain to earn enough to feed everyone. There are usually five steps which are a part of the scientific method. The steps can occur in any order, but the first step is usually observation. An observation is the use of one or more of the five senses, which include seeing, hearing, feeling, smelling, and tasting. The five senses are used to learn about or identify an event or object the scientist wants to study."
    # passage = "All living things need food and energy to survive. The food-making and energy process for plants to survive is called photosynthesis. Plants make food and produce oxygen through photosynthesis. The process is complex but with the sun, water, nutrients from the soil, oxygen, and chlorophyll, a plant makes its own food in order to survive."

    sentences = passage.split('.')

    total_sentences = 0
    total_words = 0
    total_syllables = 0
    for i in sentences:
        sentences[total_sentences] = sentences[total_sentences].split()
        total_sentences = total_sentences + 1
    for sentence in sentences:
        for word in sentence:
            if word != "" :  
                total_words = total_words + 1
    
    for sentence in sentences:
        for word in sentence:
            if word != "" :
                total_syllables = total_syllables + syllables.estimate(word)
    re = 206.835 - 1.015*(total_words/total_sentences) - 84.6*(total_syllables/total_words)
    print("working")
    return(re)
def check_grade(score):
    if 90 < score <= 100:
        print("Grade = 5th grade.")
        print("Very easy to listen to.")
    elif 80 < score <= 90:
        print("Grade = 6th grade.")
        print("Easy to listen to.")
    elif 70 < score <= 80:
        print("Grade = 7th grade.")
        print("Fairly easy to listen.")
    elif 50 < score <= 70:
        print("Grade = 8th and 9th grade.")
        print("Plain English.")
    elif 50 < score <= 55:
        print("Grade = 10th to 12th grade.")
        print("Fairly difficult to listen to.")
    elif 30 < score <= 50:
        print("Grade = College")
        print("Difficult to listen to.")
    elif 10 < score <= 30:
        print("Grade = College Graduate")
        print("Very difficult to listen.")
    elif 0 < score <= 10:
        print("Grade = Professional.")
        print("Extremely difficult to listen.")
    elif score <= 0:
        print("Very Confusing.")
    print("Listenability score:", round(score, 2))
    return(round(score, 2))


def main(value,user):
    audiofile=""
    doc_ref = db.collection('training_sessions').document(value)
    cwd = os.getcwd()
    path = cwd
    print("path", path)
    doc = doc_ref.get()
    dictt = doc.to_dict()
    if ('session' in dictt):
        if (dictt['session'] == False):
            if ('audio_recording' in dictt):
                audiofile =  dictt['audio_recording']
    response = requests.get(audiofile)
    file_name = 'audio_file.wav'
    with open(file_name, 'wb') as f:
        f.write(response.content)

    ar = myspatc(file_name, path) 
    clarity = analysis_ar(ar)
    sr = myspsr(file_name, "")    #speech rate
    speech_Rate = analysis_sr(sr)
    pauses = mysppaus(file_name, "")  #pauses
    pause = analysis_pauses(pauses)
    pronunciation = mysppron(file_name,"")
    print('Pronunciation Score: ', pronunciation)
    # re = readabiity_ease(file_name)
    # print('read', re)
    # listenability = round(check_grade(re)/10, 2)
    # print('listenability', listenability)

    
    doc = doc_ref.get()
    doc_ref.set({
        'clarity_score' : clarity,
        'pauses_score' :pauses,
        'pronunciation_score': pronunciation,
        'speakingrate_score' :speech_Rate , 
        # 'listenability_score': listenability,
        'user_id' : user,
    
    }, merge = True)

    