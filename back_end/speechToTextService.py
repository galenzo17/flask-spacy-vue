import speech_recognition as sr
r = sr.Recognizer()
harvard = sr.AudioFile('demo2.wav')
with harvard as source:
    audio = r.record(source)

try:
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))