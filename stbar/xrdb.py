from subprocess import Popen, PIPE
import re

def get_xrdb_colors():	
	'''
	Generates a dictionary of all colors in Xresources
	'''
	xrdb = Popen(('xrdb', '-query'), stdout=PIPE)
	xrdb_clean = xrdb.communicate()[0].decode().replace('\t', '')
	return dict(re.findall(r'\*.(color\d):(#\w+)', xrdb_clean))

def hex_to_rgb(hex_string):
	hex_string = re.sub('#', '', hex_string)

	if len(hex_string) == 3:
		hex_string = ''.join([c*2 for c in hex_string])
	if len(hex_string) != 6:
		raise ValueError('Invalid hex string')
	return ','.join((str(int(hex_string[i:i+2], 16)) for i in range(0,6,2)))

def parse_colors(input, xrdb=get_xrdb_colors()):
	'''
	Replaces all matches of {xrdb:color#} in a string
	with the hex code for that color
	'''

	pattern = r'(rgb-)?xrdb-(color\d+)(-#\w+)?'

	for result in re.findall(pattern, input):
		try:
			repl = xrdb[result[1]] if result[1] in xrdb else result[2][1::]
			if len(result[0]) > 0: #RGB
				input = re.sub(pattern, hex_to_rgb(repl), input, 1)
			else: # HEX
				input = re.sub(pattern, repl, input, 1)
		except IndexError:
			raise ValueError('invalid xrdb value and no backup was set')

	return input

if __name__ == '__main__':
	xrdb = get_xrdb_colors()

	print(parse_colors('xrdb-color7', xrdb))
	print(parse_colors('rgb-xrdb-color7', xrdb))

	try: #should throw an error (it doesn't right now, it just returns blank because of backup string being '')
		print(parse_colors('xrdb-color20'))
	except Exception as e:
		print(e)

	print(parse_colors('asdf'))
	print(parse_colors('asdf: xrdb-color2'))
	print(parse_colors('asdf: xrdb-color20-#ffffff'))