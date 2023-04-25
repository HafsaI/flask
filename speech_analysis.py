import firebase_admin
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
from parselmouth.praat import call, run_file
import requests
import scipy
from scipy.stats import binom
import numpy as np
import os
# import whisper
from scipy.stats import norm
# from textstat import textstat

cred = credentials.Certificate('key.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()


def clarityscore(m):
    file_n = "./myspsolution.praat"
    audio_file = "./" + m
    try:
        objects = run_file(file_n, -20, 2, 0.3, "yes", audio_file,
                           "./", 80, 400, 0.01, capture_output=True)
        print('objects', objects)
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = int(z2[3])  # will be the integer number 10
        z4 = float(z2[3])  # will be the floating point number 8.3
        return(z3)

    except:
        return(0)


def speech_ratescore(m):
    file_n = "./myspsolution.praat"
    audio_file = "./" + m
    try:
        objects = run_file(file_n, -20, 2, 0.3, "yes", audio_file,
                           "./", 80, 400, 0.01, capture_output=True)
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = int(z2[2])  # will be the integer number 10
        z4 = float(z2[3])  # will be the floating point number 8.3
        return(z3)
    except:
        return(0)


def no_of_pauses(m):
    file_n = "./myspsolution.praat"
    audio_file = "./" + m
    try:
        objects = run_file(file_n, -20, 2, 0.3, "yes", audio_file,
                           "./", 80, 400, 0.01, capture_output=True)
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = int(z2[1])  # will be the integer number 10
        z4 = float(z2[3])  # will be the floating point number 8.3
        return(z3)
    except:
        return(0)


def pronunciation(m):
    file_n = "./myspsolution.praat"
    audio_file = "./" + m
    try:
        objects = run_file(file_n, -20, 2, 0.3, "yes", audio_file,
                           "./", 80, 400, 0.01, capture_output=True)
        # This will print the info from the textgrid object, and objects[1] is a parselmouth.Data object with a TextGrid inside
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = int(z2[13])  # will be the integer number 10
        z4 = float(z2[14])  # will be the floating point number 8.3
        db = binom.rvs(n=10, p=z4, size=10000)
        a = np.array(db)
        b = np.mean(a)*100/10
        return(round(b, 1))
    except:
        return(0)


def calibrate_clarity(new_score):
    if new_score == 0:
        clarity_comment = "Speak Clearly!"
    else:
        mean_good = 5
        sd_good = 0.67

        mean_avg = 5
        sd_avg = 0.32

        mean_bad = 5
        sd_bad = 0.97

        z_good = (new_score - mean_good) / sd_good
        z_avg = (new_score - mean_avg) / sd_avg
        z_bad = (new_score - mean_bad) / sd_bad

        # Calculate the probability using the cumulative distribution function (cdf) of the normal distribution
        # The cdf gives the probability that a random variable is less than or equal to a certain value (in this case, the z-score)
        prob_good = norm.cdf(z_good)
        prob_avg = norm.cdf(z_avg)
        prob_bad = norm.cdf(z_bad)

        if new_score == 6:
            clarity_comment = "Above Average!"
        else:
            max_clarity = max(prob_avg, prob_bad, prob_good)
            if max_clarity == prob_avg:
                clarity_comment = "Average!"
            elif max_clarity == prob_good:
                clarity_comment = "Above Average!"
            elif max_clarity == prob_bad:
                clarity_comment = "Below Average!"
    return(clarity_comment)


def calibrate_speechrate(new_score):
    if new_score == 0:
        clarity_comment = "Speak Clearly!"
    else:
        mean_good = 4
        sd_good = 0.52

        mean_avg = 5
        sd_avg = 0.53

        mean_bad = 4
        sd_bad = 0.97
        z_good = (new_score - mean_good) / sd_good
        z_avg = (new_score - mean_avg) / sd_avg
        z_bad = (new_score - mean_bad) / sd_bad

        # Calculate the probability using the cumulative distribution function (cdf) of the normal distribution
        # The cdf gives the probability that a random variable is less than or equal to a certain value (in this case, the z-score)
        prob_good = norm.cdf(z_good)
        prob_avg = norm.cdf(z_avg)
        prob_bad = norm.cdf(z_bad)

        max_clarity = max(prob_avg, prob_bad, prob_good)
        if max_clarity == prob_avg:
            clarity_comment = "Average!"
        elif max_clarity == prob_good:
            clarity_comment = "Above Average!"
        else:
            clarity_comment = "Below Average!"
    return(clarity_comment)


def listenability(audio_filename):
    model = whisper.load_model("small.en")
    result = model.transcribe(audio_filename, language="en", fp16=False)
    text = result["text"]
    flesch_reading_ease = textstat.flesch_reading_ease(text)
    return(round(flesch_reading_ease, 1))


# for vr speech
def main(sess_id):
    audiofile = ""
    doc_ref = db.collection('training_sessions').document(sess_id)
    # cwd = os.getcwd()
    # path = cwd
    # print("path", path)
    doc = doc_ref.get()
    dictt = doc.to_dict()
    if ('session' in dictt):
        if (dictt['session'] == False):
            if ('audio_recording' in dictt):
                audiofile = dictt['audio_recording']
    response = requests.get(audiofile)
    file_name = 'audio_file.wav'
    with open(file_name, 'wb') as f:
        f.write(response.content)

    # Clarity score
    clarity_score = clarityscore(file_name)
    clarity_comments = calibrate_clarity(clarity_score)
    print("Clarity score is: ", clarity_score)
    print("Comments: " + clarity_comments)

    # Speech rate score
    speechrate_score = speech_ratescore(file_name)
    speech_Rate_comments = calibrate_speechrate(speechrate_score)
    print("Speech rate score is: ", speechrate_score)
    print("Comments: " + speech_Rate_comments)

    # No of Pauses
    pauses = no_of_pauses(file_name)
    print("num of pauses: ", pauses)

    # Pronounciation score
    pronunciation_score = pronunciation(file_name)
    print("Pronounciation score is: ", pronunciation_score)

    # Listenability score
    # listenability_score = listenability(file_name)
    # print("Listenability score is: ", listenability_score)

    doc = doc_ref.get()
    doc_ref.set({
        'clarity_score': clarity_score,
        'clarity_comment': clarity_comments,
        'pauses_score': pauses,
        'pronunciation_score': pronunciation_score,
        'speakingrate_score': speechrate_score,
        'speakingrate_comment': speech_Rate_comments,
        # 'listenability_score': listenability_score,

    }, merge=True)

# for individual speech


def individual_analysis(file_name):
    clarity_score = clarityscore(file_name)
    clarity_comments = calibrate_clarity(clarity_score)
    print("Clarity score is: ", clarity_score)
    print("Comments: " + clarity_comments)

    # Speech rate score
    speechrate_score = speech_ratescore(file_name)
    speech_Rate_comments = calibrate_speechrate(speechrate_score)
    print("Speech rate score is: ", speechrate_score)
    print("Comments: " + speech_Rate_comments)

    # No of Pauses
    pauses = no_of_pauses(file_name)
    print("num of pauses: ", pauses)

    # Pronounciation score
    pronunciation_score = pronunciation(file_name)
    print("Pronounciation score is: ", pronunciation_score)
    data = {'clarity_score': clarity_score, 'clarity_comments': clarity_comments, 'speechrate_score': speechrate_score,
            'speechrate_comments': speech_Rate_comments, 'pauses_score': pauses, 'pronunciation_score': pronunciation_score}

    return data
