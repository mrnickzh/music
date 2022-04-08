from urllib.request import urlopen
import pyaudio, keyboard, os

print("\nNickZh's music stream player\n")

def play(id):
    pyaud = pyaudio.PyAudio()

    stream = pyaud.open(format=pyaud.get_format_from_width(2),
                        channels=2,
                        rate=44100,
                        output=True)

    url = f"http://localhost:8000/play${id}"  # "http://45.8.229.36:8000/test"
    u = urlopen(url)

    data = u.read(1024)

    name = urlopen(f"http://localhost:8000/id2name${id}")
    name = name.read(1024).decode("utf-8")

    print(f'Now playing - "{name.split(".wav")[0]}"\nTo stop press P on keyboard')

    while data:
        stream.write(data)
        data = u.read(1024)
        if keyboard.is_pressed('p'):
            print("Stopped")
            return

def search(name):
    u = urlopen(f"http://localhost:8000/search${name}")
    data = u.read(1024).decode("utf-8").replace("|", "\n")
    print(data)

while True:
    id = str(input("Enter song id to play or name to search: "))
    if id.isnumeric() == True:
        try:
            play(id)
        except:
            print("Error, check the song id")
    else:
        search(id)
