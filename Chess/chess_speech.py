import speech_recognition as sr


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
        audio = recognizer.listen(source, None, 3)

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


def speech_to_move():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    guess = recognize_speech_from_mic(recognizer, microphone)

    while(not guess["transcription"]):
        guess = recognize_speech_from_mic(recognizer, microphone)


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
        
    acceptable_words = ["QUIT","ENGINE"]
    acceptable_words+=locations
    #print(acceptable_words)

    move = "None"
    for word in choices:
        word = word.upper()
        if word in acceptable_words:
            move = word
            break
            
    if move == "None":
        print("Try again")
        return speech_to_move()

    return move.lower()

def testing():
    while True:
        speech_to_move()


if __name__ == '__main__':
    testing()


