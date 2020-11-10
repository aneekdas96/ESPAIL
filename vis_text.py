from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from google_images_download import google_images_download
import os
import re 
import shutil

def get_chunks(text):
	tokenized_sentence = word_tokenize(text)
	pos_tagged = pos_tag(tokenized_sentence)
	chunked = ne_chunk(pos_tagged)
	nouns, verbs, adjectives, adverbs = get_diff_tags(pos_tagged)
	person, location, institution = get_named_entities(chunked)
	return nouns, verbs, adjectives, adverbs, person, location, institution

def get_diff_tags(pos_tagged):
	nouns = []
	verbs = []
	adjectives = []
	adverbs = []

	for pos_chunk in pos_tagged:
		tag = pos_chunk[1]
		word = pos_chunk[0]
		if tag == 'NN' or tag == 'NNS' or tag == 'NNP' or tag == 'NNPS':
			nouns.append(word.lower())
		elif tag == 'VB' or tag == 'VBD' or tag == 'VBG' or tag == 'VBN' or tag == 'VBP' or tag == 'VBZ':
			verbs.append(word.lower())
		elif tag == 'JJ' or tag == 'JJR' or tag == 'JJS':
			adjectives.append(word.lower())
		elif tag == 'RB' or tag == 'RBR' or tag == 'RBS':
			adverbs.append(word.lower())
	for word in nouns:
		if len(word) < 4 : 
			nouns.remove(word)
	for word in verbs:
		if len(word) < 4 : 
			verbs.remove(word)
	for word in adjectives:
		if len(word) < 4 : 
			adjectives.remove(word)
	for word in adverbs:
		if len(word) < 4 : 
			adverbs.remove(word)
	nouns = set(nouns)
	nouns.remove('male')
	adjectives = set(adjectives)
	adjectives.remove('male')

	return set(nouns), set(verbs), set(adjectives), set(adverbs) 

def get_named_entities(chunked):
	person = []
	location = []
	institution = []
	for chunk in chunked:
		if hasattr(chunk, 'label'):
			if chunk.label() == 'PERSON':
				person.append(chunk[0][0].lower())
			elif chunk.label() == 'GPE':
				location.append(chunk[0][0].lower())
			elif chunk.label() == 'FACILITY':
				institution.append(chunk[0][0].lower())

	return set(person), set(location), set(institution)
	
def get_images(query, class_dir):
	download_path = 'C:\\Users\\dcane\\OneDrive\\Desktop\\hackharv_2018\\downloads\\' + query + '\\'
	move_path = 'C:\\Users\\dcane\\OneDrive\\Desktop\\hackharv_2018\\' + str(class_dir) + '\\'
	response = google_images_download.googleimagesdownload()
	arguments = {"keywords": query ,"limit":1,"print_urls":False, 'safe_search':'On'}
	paths = response.download(arguments)[query]
	for path in paths:
		print('current path is : ', path)
		if path[-4:] == '.jpg':
			new_image_path = str(move_path + query + '.jpg')
		else:
			new_image_path = str(move_path + query + '.png')
		shutil.move(path, new_image_path)

def manager(nouns, verbs, adjectives, adverbs, person, location, institution):
	try:
		for tag in ['nouns', 'verbs', 'adjectives', 'adverbs', 'person', 'location', 'institution']:
			os.makedirs(tag)
	except Exception as e:
		pass
	try:
		for i in institution:
			get_images(i, 'institution')
	except Exception as e:
		print('could not fetch image')
	try:
		for l in location:
			get_images(l, 'location')
	except Exception as e:
		print('could not fetch image')	
	try:
		for p in person:
			get_images(p, 'person')
	except Exception as e:
		print('could not fetch image')	
	try:
		for verb in verbs:
			get_images(verb, 'verbs')
	except Exception as e:
		print('could not fetch image')
	try:	
		for adjective in adjectives:
			get_images(adjective, 'adjectives')
	except Exception as e:
		print('could not fetch image')
	try:	
		for adverb in adverbs:
			get_images(adverb, 'adverbs')
	except Exception as e:
		print('could not fetch image')
	try:
		for noun in nouns:
			get_images(noun, 'nouns')
	except Exception as e:
		print('could not fetch image')	
	

	print('Finished execution')

def meta_manager(file_name):
	store = open(file_name, 'r')
	sentence = store.read()
	nouns, verbs, adjectives, adverbs, person, location, institution = get_chunks(sentence)
	manager(nouns, verbs, adjectives, adverbs, person, location, institution)

meta_manager('after_process.txt')