'''
Python CLI tool used to obsufscate batch scripts.
Inspired by John Hammond's video on the subject. 
'''

import random
import string

import argparse as ap

# chars is a dict where each char is a key and it's obsfuscated name is the value
chars = {}

# makeName() generates variable names for each letter.
def makeName(maxLen=15):

	if maxLen <= 5:
		maxLen = 5

	while True:
		name = ''.join([ random.choice(string.ascii_letters) for _ in range(random.randint(5, 15))])
		if name in chars.values():
			continue
		return name

# This takes clear and writes to an output file, which can be passed in as the parameter file.
def makeFile(file='test.txt', clear=''):

	# these keys are needed for the setup of the file. 
	# since the obsfusaction doesn't include special chars or whitespace,
	# We need to add them to the chars dict here.
	chars['set'] = makeName()
	chars[' '] = makeName()
	chars['='] = makeName()

	# this creates the char dict.
	for char in string.printable[:-38]:
		chars[char] = f'{makeName()}'

	# File is opened with the w+ mode, so the file will be created
	with open(file, 'w+') as f:

		f.write('@echo OFF\n')

		# these create variables for each of the special cases on lines 34-36
		f.write(f'set {chars["set"]}=set\n')
		f.write(f'%{chars["set"]}% {chars[" "]}= \n')
		f.write(f'%{chars["set"]}%%{chars[" "]}%{chars["="]}==\n')

		# these variables are just for ease of use. setSpace repersents "set " and equalSign is  "="
		setSpace = f'%{chars["set"]}%%{chars[" "]}%'
		equalSign = f'%{chars["="]}%'

		# defines a variable for each char in chars
		for char in chars:
			f.write(f'{setSpace}{chars[char]}{equalSign}{char}\n')

		f.write('@echo ON\n')

		# wrties the payload to the file
		for char in clear:
			if char in chars.keys():
				f.write(f'%{chars[char]}%')
			else:
				f.write(char)

def main():

	parser = ap.ArgumentParser()
	parser.add_argument('inputFile', type=str, help='Name of input (clear) file.' )
	parser.add_argument('outputFile', type=str, help='Name of output (Obs) file.' )

	args = parser.parse_args()

	try:
		with open(args.inputFile, 'r') as f:
			clear = ''.join([ x for x in f.readlines() ])
	except FileNotFoundError:
		print(f'File {args.inputFile} does not exist.')
		return 0

	makeFile(file=args.outputFile, clear=clear)

if __name__ == '__main__':
	main()