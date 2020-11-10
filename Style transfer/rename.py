import os
for i in os.listdir(os.getcwd()):
	print (i[:6])
	if i[:6]=='frame_':
		renames = i
		while len(renames[6:])!=4:
			renames = renames[:6]+'0'+renames[6:]
			print (renames[6:])
			break

		print (renames)
		os.rename(i,renames)
		break
		
