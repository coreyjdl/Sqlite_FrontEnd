
# A minimal SQLite shell for experiments

import sys
import sqlite3

def roll_array( array ):
	result = [ list() for _ in array[0] ]
	for row in array:
		for idx, element in enumerate(row):
			result[idx].append(element)
	return result

def get_column_widths(data):
	rolled_array = roll_array(data)
	result = list()
	for column in rolled_array:
		width = len( str( max( map(str, column), key =len )))
		result.append(width)
	return result
	
def display(headers, results):
	
	# left most borders
	HEAVY_DOWN_RIGHT = "\N{BOX DRAWINGS HEAVY DOWN AND RIGHT}"
	HEAVY_UP_RIGHT = "\N{BOX DRAWINGS HEAVY UP AND RIGHT}"
	HEAVY_VERTICAL_LIGHT_RIGHT = "\N{BOX DRAWINGS VERTICAL HEAVY AND RIGHT LIGHT}"
	
	# right most borders
	HEAVY_UP_LEFT = "\N{BOX DRAWINGS HEAVY UP AND LEFT}"
	HEAVY_DOWN_LEFT = "\N{BOX DRAWINGS HEAVY DOWN AND LEFT}"
	HEAVY_VERTICAL_LIGHT_LEFT = "\N{BOX DRAWINGS VERTICAL HEAVY AND LEFT LIGHT}"
	
	# horizontal lines
	LIGHT_HORIZONTAL = "\N{BOX DRAWINGS LIGHT HORIZONTAL}"
	HEAVY_HORIZONTAL = "\N{BOX DRAWINGS HEAVY HORIZONTAL}"
	
	# intermediate vertical lines
	HEAVY_VERTICAL = "\N{BOX DRAWINGS HEAVY VERTICAL}"
	HEAVY_DOWN_HORIZONTAL = "\N{BOX DRAWINGS HEAVY DOWN AND HORIZONTAL}"
	HEAVY_UP_HORIZONTAL = "\N{BOX DRAWINGS HEAVY UP AND HORIZONTAL}"
	HEAVY_VERTICAL_LIGHT_HORIZONTAL = "\N{BOX DRAWINGS VERTICAL HEAVY AND HORIZONTAL LIGHT}"

	
	table = [[header[0] for header in headers], *results]
	widths = get_column_widths(table)
	
	# strings to start each template.
	top_border_template = HEAVY_DOWN_RIGHT
	bottom_border_template = HEAVY_UP_RIGHT
	header_bottom_template = HEAVY_VERTICAL_LIGHT_RIGHT
	text_template = HEAVY_VERTICAL
	
	
	for width in widths:
		width += 2
		top_border_template += "{}{}".format( HEAVY_HORIZONTAL * width, HEAVY_DOWN_HORIZONTAL)	
		bottom_border_template += "{}{}".format(HEAVY_HORIZONTAL * width, HEAVY_UP_HORIZONTAL)	
		header_bottom_template += "{}{}".format(LIGHT_HORIZONTAL * width, HEAVY_VERTICAL_LIGHT_HORIZONTAL)	
		text_template += "{{:>{}}}{}".format(width, HEAVY_VERTICAL)
		
	top_border_template = top_border_template[:-1] + HEAVY_DOWN_LEFT
	bottom_border_template = bottom_border_template[:-1] + HEAVY_UP_LEFT
	header_bottom_template = header_bottom_template[:-1] + HEAVY_VERTICAL_LIGHT_LEFT

	first = True
	print(top_border_template)
	for line in table:
		print(text_template.format(*map(str, line)))
		if first:
			print(header_bottom_template)
			first = False
	print(bottom_border_template)
		
def main():

	first_line = True
	exit = False
	
	args = sys.argv
	db = args[1] if len(args) > 1 else None		
	con = sqlite3.connect(db) if db else sqlite3.connect(":memory:")
	
	con.isolation_level = None
	cur = con.cursor()
	
	buffer = ""
	
	print("Enter your SQL commands to execute in sqlite3.")
	print("Enter a blank line to exit.")
	
	while True:
		line = input('>> ' if first_line else ' ' * 3)
		first_line = False
		
		if not line and exit:
			break
		elif not line:
			exit = True
		elif line:
			exit = False
			
		buffer += ' ' + line
			
		if sqlite3.complete_statement(buffer):
			try:
				buffer = buffer.strip()
				cur.execute(buffer)			
				results = cur.fetchall()
								
				if results:
					display(cur.description, results)
				elif cur.rowcount :
					print( f"{cur.rowcount} row{'s' if cur.rowcount != 1 else ''} affected.")
					
			except sqlite3.Error as e:
				print("An error occurred:", e.args[0])
				
			buffer = ""
			first_line = True

	con.close()
	
if __name__ == "__main__":
	main()
