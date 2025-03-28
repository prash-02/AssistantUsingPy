import speech_recognition as sr
import time

def list_microphones():
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone {index}: {name}")

def test_microphone(device_index=5):  # Default to Intel Smart Sound Technology mic
    r = sr.Recognizer()
    try:
        print(f"\nTesting microphone with index {device_index}")
        mic = sr.Microphone(device_index=device_index)
        
        with mic as source:
            print("Initializing...")
            time.sleep(1)  # Give the microphone a moment to initialize
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Ready! Say something...")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                print("Processing audio...")
                try:
                    text = r.recognize_google(audio)
                    print("You said: " + text)
                    return True
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
            except Exception as e:
                print(f"Error during recording: {str(e)}")
    except Exception as e:
        print(f"Error initializing microphone: {str(e)}")
    return False

if __name__ == "__main__":
    list_microphones()
    # Try specific microphone
    success = test_microphone(5)  # Try Intel Smart Sound Technology mic
    if not success:
        print("\nTrying alternative microphone...")
        test_microphone(17)  # Try Realtek HD Audio Mic input as fallback
