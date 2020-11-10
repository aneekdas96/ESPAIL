#import os

f = open("run.txt","w")
counter = 473

while True:
	counter+=1
	renanme_counter = str(counter)
	while len(renanme_counter)<4:
		renanme_counter = '0'+renanme_counter
	name = 'frame_'+renanme_counter+'.jpg'
	f.write("python transform.py -i image/content/"+name+" -s des_glaneuses -b 0.5 -o "+name[:-4]+'\n')
	if counter > 633:
		break

f.close()
