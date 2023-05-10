import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
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

if __name__ == "__main__":
    state=0
    once=True
    while True:
        test=False

        if once:
            print('WELCOME TO WIZARDING CHESS')
            print('TOGETHER WE WILL LEARN HOW TO USE OUR VOICE ACTIVATED CONTROL SYSTEM')
            print('Let''s try and move the pawn from C2 to C4')
            print('If there is no action after 5 seconds, repeat your command')
            once=False

        if state==0:
            print("Say Pawn")
            curr_word="Pawn"

        if state==1:
            print("Now state the starting location (C2)")
            curr_word="C2"

        if state==2:
            print("Now state the ending location (C4)")
            curr_word="C4"
        if state==3:
            print("Great job! You are now a pro at speaking the conmands!")
            break

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

        move = "None"
        for word in choices:
            if word.lower() == curr_word.lower():
                move = word
                print(f"Great job! Recognized word: {word}")
                state+=1
                test=True
                break
                
        if move == "None":
            print("Try again")
        
        # show the user the transcription
        if test==False:
            print('\n',"The word you said was not recognized as acceptable. Here are some thinks we think you said:{}".format(guess["transcription"]))
            print("Try again: ")


    #speech_to_move()