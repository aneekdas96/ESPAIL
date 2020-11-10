import subprocess 
import re
import speech_recognition as sr
from os import path
import requests
import json
import time
import pandas as pd

API_KEY = "Bearer 01dzB5uPPHurzlH0XSAKAZKZBKzBygteZyXkzFhfhwrmDvRvD3nkL806QPxC5ucHC5ltCJCvlVckPzRd7Qtv10nrbck-Q"
HEADERS = {'Authorization': API_KEY}

path_to_vid = './lion.mp4'

def submit_job_file(file):
    url = "https://api.rev.ai/revspeech/v1beta/jobs"
    files = { 'media': (file, open(file, 'rb'), 'audio/mp3') }
    request = requests.post(url, headers=HEADERS, files=files)
    print(request.status_code)
    if request.status_code != 200:
        
        raise Exception

    response_body = request.json()
    return response_body['id']

def view_job(id=59594172):
    url = f'https://api.rev.ai/revspeech/v1beta/jobs/{id}'
    request = requests.get(url, headers=HEADERS)

    if request.status_code != 200:
        raise Exception

    response_body = request.json()
    return response_body

def get_transcript(id='59594172'):
    url = f'https://api.rev.ai/revspeech/v1beta/jobs/{id}/transcript'
    headers = HEADERS.copy()
    headers['Accept'] = 'application/vnd.rev.transcript.v1.0+json'
    request = requests.get(url, headers=headers)

    if request.status_code != 200:
        raise

    response_body = request.json()
    return response_body

def test_workflow_with_url(url):
    print ("Submitting job with URL")
    id = submit_job_url(url)
    print ("Job created")
    view_job(id)

    while True:
        job = view_job(id)
        status = job["status"]
        print (f'Checking job transcription status: { status }')
        if status == "transcribed":
            break
        if status == "failed":
            raise

        print ("Trying in another 30 seconds")
        time.sleep(30)

    return get_transcript(id)

def test_workflow_with_file(file):
    print ("Submitting job with file")
    id = submit_job_file(file)
    print ("Job created")
    view_job(id)

    while True:
        job = view_job(id)
        status = job["status"]
        print (f'Checking job transcription status: { status }')
        if status == "transcribed":
            break
        if status == "failed":
            raise

        print ("Trying in another 30 seconds")
        time.sleep(30)

    return get_transcript(id)

def get_audio_from_vid(path_to_vid):
	if path_to_vid[-4:] == '.mp4':
		m = re.search('/.*mp4', path_to_vid)
		vid_file = m.group()[1:-4]
		command = "ffmpeg -i " + str(path_to_vid) + " -ab 160k -ac 2 -ar 44100 -vn " + vid_file + '.wav'
		subprocess.call(command, shell=True)
		audio_file = vid_file + '.wav'
		return audio_file

# def get_text_from_audio(audio_file):
	# r = sr.Recognizer()
	# with sr.AudioFile(audio_file) as source:
	#     audio = r.record(source)  
	# try:
	# 	text_in_wav_file = r.recognize_sphinx(audio)
	# 	
	# 	print("Audio file reads as : " + text_in_wav_file)
	# except sr.UnknownValueError:
	# 	print("Audio could not be understood")
	# except sr.RequestError as e:
	# 	print("Error while reading audio file {0}".format(e))
	# return text_in_wav_file


# store = get_text_from_audio('lion.wav')
def get_text_from_audio():
	store = 'lion.wav'
	out_dict = test_workflow_with_file(store)
	mono = out_dict['monologues']
	stuff_1 = mono[0]
	stuff_2 = stuff_1['elements']
	stuff_3 = stuff_2[0]
	l = []
	for i in stuff_2:
	    l.append(i['value'])
	new_l = "".join(l)
	print('the converted text looks like : ', new_l)
	store_transcript = open('trans.txt', 'w')
	store_transcript.write(new_l)
	store_transcript.close()

	return new_l

def post_processing_text():
	doc_in_chunks = []
	window_size = 0
	store = open('trans.txt', 'r')
	text_in_store = store.read()
	text_in_store = text_in_store.split('.')
	text_in_store = text_in_store[:-1]
	# word_counter = len(text_in_store)
	# word_chunk = []
	# for i in range(word_counter):
	# 	if window_size < 10:
	# 		word_chunk.append(text_in_store[i])
	# 		window_size += 1
	# 	else:
	# 		doc_in_chunks.append(word_chunk)
	# 		window_size = 0
	# 		word_chunk = []
	# return doc_in_chunks
	return text_in_store

def recombine_chunks_to_file(text_in_store):
	if text_in_store == None:
		return False
	else:
		with open('after_process.txt', 'w') as new_text_file:
			for sentence in text_in_store:
				new_text_file.write(sentence)
				new_text_file.write('\n')
		new_text_file.close()
		return True

def manager_func(file_name):
	text_in_store = get_text_from_audio()
	text_in_store = post_processing_text()	
	bool_val = recombine_chunks_to_file(text_in_store)

manager_func('lion.mp4')
