import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
from parselmouth.praat import call, run_file
import requests
import scipy
from scipy.stats import binom
import numpy as np


cred = credentials.Certificate('key.json') 
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


def myspatc(m,p):
    # sound="/api/"+m
    # print(sound)
    file_n="myspsolution.praat"
    print(file_n)
    # path="/api/"
    # print(path)
    try:
        objects= run_file(file_n, -20, 2, 0.3, "yes",m,"", 80, 400, 0.01, capture_output=True)
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
    file_n="myspsolution.praat"
    print(file_n)
    try:
        objects= run_file(file_n, -20, 2, 0.3, "yes",m,"", 80, 400, 0.01, capture_output=True)
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
    file_n="myspsolution.praat"
    print(file_n)
    try:
        objects= run_file(file_n, -20, 2, 0.3, "yes",m,"", 80, 400, 0.01, capture_output=True)
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
    file_n="myspsolution.praat"
    try:
        objects= run_file("myspsolution.praat", -20, 2, 0.3, "yes",m,"", 80, 400, 0.01, capture_output=True)
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


def main(value,user):

    

    audiofile=""
    doc_ref = db.collection('training_sessions').document(value)
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

    ar = myspatc(file_name, "") 
    clarity = analysis_ar(ar)
    sr = myspsr(file_name, "")    #speech rate
    speech_Rate = analysis_sr(sr)
    pauses = mysppaus(file_name, "")  #pauses
    pause = analysis_pauses(pauses)
    pronunciation = mysppron(file_name,"")
    print('Pronunciation Score: ', pronunciation) #pronunciation score (intonation & phenomic perfomance)

    
    doc = doc_ref.get()
    doc_ref.set({
        'clarity_score' : clarity,
        'pauses_score' :pauses,
        'pronunciation_score': pronunciation,
        'speakingrate_score' :speech_Rate , 
        'listenability_score': 7,
        'user_id' : user,
    
    }, merge = True)