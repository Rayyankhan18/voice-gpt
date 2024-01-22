import openai
import pyttsx3
import speech_recognition as sr


openai.api_key = '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'

engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except Exception as e:
            print(f'skipping unknown error: {e}')
            return None

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=4000,
        temperature=0.5,
    )
    return response['choices'][0]['message']['content']


def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:

        print("Say 'jarvis' to start recording your question...  ")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "jarvis":


                    filename = "input.wav"
                    print("Say Your Question....")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())


                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")


                        speak_text(response)
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Speech Recognition request failed: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

print("hello world")
