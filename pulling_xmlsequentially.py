from lxml import etree


infile = 'split1.xml'
context = etree.iterparse(infile, events=('end',), tag=('title', 'ns', 'id', 'text'))

titles = open('titles.txt', 'w')
namespaces = open('namespaces.txt', 'w')
articles = open('articles.txt', 'w')
ids = open('ids.txt', 'w');              i = 0;
for event, elem in context:
    print("Event number: ", i); i = i +1;
    #Adding page number
    #if i%7 == 0:
    #    out.write('%d\n' % int(i/7) )
        
    #Adding title
    if elem.tag == 'title':
        if not elem.text.encode('utf-8'):
            titles.write('ERROR: No Title Content Found\n' )
        if elem.text.encode('utf-8'):
            titles.write('%s\n' % elem.text.encode('utf-8'))
            print(str(elem.text.encode('utf-8')))

    #Adding namespace
    if elem.tag == 'ns':
        if not elem.text.encode('utf-8'):
            namespaces.write('ERROR: No Namespace Content Found\n' )
        if elem.text.encode('utf-8'):
            namespaces.write('%s\n' % elem.text.encode('utf-8'))
    
    #Adding ID
    if elem.tag == 'id':
        if not elem.text.encode('utf-8'):
            ids.write('ERROR: No ID Content Found\n' )
        if elem.text.encode('utf-8'):
            ids.write('%s\n' % elem.text.encode('utf-8'))
            
    #Adding title
    if elem.tag == 'text':
        if not elem.text.encode('utf-8'):
            articles.write('ERROR: No Text Content Found\n' )
        if elem.text.encode('utf-8'):
            articles.write('%s\n' % elem.text.encode('utf-8'))
     
    # Making it memory efficient to avoid clogging RAM    
    #deleting descendants
    elem.clear()
    #deleting now-empty references from the root node to tag <title>, etc 
    while elem.getprevious() is not None:
        del elem.getparent()[0]
del context
titles.close()
namespaces.close()
articles.close()
ids.close()

