from flask import Flask
from flask import Response
import pyaudio, os
import wave

app = Flask(__name__)

def genHeader(sampleRate, bitsPerSample, channels, samples):
    datasize = 10240000 # Some veeery big number here instead of: #samples * channels * bitsPerSample // 8
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

@app.route('/id2name$<string:sid>')
def id2name(sid):
    dirs=os.listdir("music")
    for odr in dirs:
        dr = odr.split("!")
        id = dr[0]
        dr = dr[1]
        if sid==id:
            return odr.split('!')[1]

@app.route('/play$<string:id>')
def play(id):
    name=""
    dirs = os.listdir("music")
    for odr in dirs:
        dr = odr.split("!")
        if dr[0]==id:
            name=odr

    wf = wave.open(f"music/{name}", 'rb')

    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
        p.get_device_info_by_index(i)

    wav_header = genHeader(wf.getframerate(), 16, wf.getnchannels(), 1024)
    def sound(name):
        wf = wave.open(f"music/{name}", 'rb')
        data = wav_header
        data += wf.readframes(1024)
        yield (data)
        while True:
            data = wf.readframes(1024)
            if data != b'':
                yield (data)
            else:
                wf = wave.open(f"music/{name}", 'rb')

    return Response(sound(name), mimetype="audio/x-wav")

@app.route('/search$<string:strg>')
def search(strg):
    strg2=""
    dirs=os.listdir("music")
    for odr in dirs:
        dr = odr.split("!")
        id = dr[0]
        dr = dr[1]
        dr = dr.split(strg)
        if len(dr)>1:
            strg2+=f"ID: {id} NAME: {odr.split('!')[1]}|"
    if strg2=="":
        return "Nothing found"
    else:
        return strg2


app.run(host="localhost", port=8000)