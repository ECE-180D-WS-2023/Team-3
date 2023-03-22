#taken from: https://realpython.com/python-speech-recognition/#putting-it-all-together-a-guess-the-word-game

import speech_recognition as sr #djf


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, None , 3) # duration to listen 

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, show_all=True)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    while True:
        test=False

        # create recognizer and mic instances
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        print("Say something:\n")
        #time.sleep(1)

        while True:
            print('Speak!')
            guess = recognize_speech_from_mic(recognizer, microphone)
            
            while(not guess["transcription"]):
                guess = recognize_speech_from_mic(recognizer, microphone)

           # if guess["success"]
            choices=[]
            length=len(guess["transcription"]["alternative"])
           
            for i in range(0,length):
                choice=(guess["transcription"]["alternative"][i])
                choices.append(choice['transcript'])

            locations = []

            # iterate over all columns and rows
            for col in range(1, 9):
                for row in range(1, 9):
                    # create a string representation of the location
                    loc = f"{chr(col + 96).upper()}{row}"
                    # add the location to the list
                    locations.append(loc)
               
            acceptable_words = ["pawn", "bishop", "rook", "knight","queen","king","Pawn", "Bishop", "Rook", "Knight","Queen","King"]
            acceptable_words+=locations
            #print(acceptable_words)
            
            for word in choices:
                if word in acceptable_words:
                    print(f"Recognized word: {word}")
                    test=True
                    break
            
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")
                

        # if there was an error, stop 
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))

        # show the user the transcription
        if test==False:
            print('\n',"You said: {}".format(guess["transcription"]))
