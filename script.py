# CHALLENGE 1 


###             LIBRARIES              ###

import re
import untangle


###           USEFUL FUNCTIONS        ###

def visible(element):
    '''
    Visible returns boolean True if text is not under the html/xml tags below.
    The input is website text (including xml code), and when used with python's
    filter function, it outputs the visible text in a website '''
    
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif  re.match('.*<!--.*-->.*', str(element), re.DOTALL):
        return False
    return True


def xml_to_text(xml_file):
    text = list(filter(visible, xml_file))
    if text:
        # removing newlines and concatenating all text
        website_text = ' '.join([x for x in website_text if x != '\n'])
        #website_text = soup.get_text()  #just text, no html or javascript code (hopefully)    
        # removing further emptyspaces
        website_text = website_text.replace(" '\n' ", "")
        website_text = website_text.replace("\n", "")
        website_text = website_text.replace("    ", "")
        
    if not text:
        print("\t", xml_file, 'IS EMPTY')
        text = ""
    return text

def extract_patterns(text_file, string1, min, max, string2):
    '''
    Function Description:
    S1 [a1, b1] S2 [a2,b2] S3 … [an-1,bn-1] Sn where Sk is a 
    specific string (for example “dog”) and [ak,bk] matches 
    any string with at least ak characters and at most bk 
    characters.

    For example:
        “cat” [2,4] “hat” will match any string that starts 
        with “cat”, then has between 2 and 4 characters and 
        then has “hat”.
        
        INPUT:  .txt, string, min num of characters after 
                string, max num of characters after last 
                letter in string1, the string the pattern 
                should end with
        
        OUTPUT: A list of strings where each element in the
                list is a match 
        '''
    #extract pattern 
    regex = "(" + string1 + ".{" + str(min) + ',' + str(min) + '}' + string2 + ")"
    match = re.findall(regex, text_file, flags=re.I)
    if not match:
        print("The pattern provided is not found in\t", text_file)
    return match




###         SOLVING CHALLENGE          ###

# Uploading xml file 
xml_file = untangle.parse('wiki_example.xml')

# Extracting text
text = xml_to_text(xml_file)

# Extracting pattern
result = extract_patterns(text, "cat", 2, 4, "hat")
print(result[0])

