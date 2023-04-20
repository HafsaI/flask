import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
from parselmouth.praat import call, run_file


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


def analysis_ar(ar):
    if ar > 6:
        print("Try to speak clearly.")
    else:
        print("Clarity Score =" , round((ar/6)*10) )
    return(round((ar/6)*10))

def main(value,user):

    file_name = 'audio_file.wav'
    ar = myspatc(file_name, "") 
    clarity = analysis_ar(ar)
    doc_ref = db.collection('training_sessions').document(value)
    doc = doc_ref.get()
    doc_ref.set({
        'clarity_score' : 1,
        'pauses_score' :2,
        'pronunciation_score': 2,
        'speakingrate_score' :7 , 
        'listenability_score': 7,
        'user_id' : user,
    
    }, merge = True)