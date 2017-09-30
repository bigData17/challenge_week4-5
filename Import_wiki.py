# import XML parsing library
import xml.etree.ElementTree as ET
import collections, re


# import the file and find the roots
tree = ET.parse('sample.xml')
root = tree.getroot()

l = []

# to go two levels deep in the roots, you will first enter <page>, then <revision> and then <text>
for x in root.findall('book'):
	for y in x.findall('hej'):
		#when we have found the text of an article, we want to remove linebreak and change everything to lower case letters.
		article = y.find('description').text
		#article = article.replace('\n', ' ').replace('\r', '')
		article = article.lower()
		article = re.sub(r'\W+', ' ', article)
		l.append(article)


l2 = [word for line in l for word in line.split()]


unique = set(l2)

Total = []									
for art in l:								
	T = art		
	T2 = re.sub(r'\W+', ' ',  T).split()	
	c = collections.Counter(T2)				
	vector = []								
	for w in unique:					
		vector.append(c.get(w,0))			
	Total.append(vector)	

				

