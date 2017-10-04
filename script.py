# CHALLENGE 1 


###             LIBRARIES              ###

import re


###           USEFUL FUNCTIONS        ###


# This function converts a list of words into a single string
def list_to_string(list_of_words):
    return " ".join(list_of_words)
    
# This function matches (and returns) the entire pattern (non-recursively)
# found in the string
def extract_patterns1(text_file, list_of_patterns):

    #extracting strings, mins and maxs from list    
    a = list_of_patterns[0::3] #list of strings
    b = list_of_patterns[1::3] #list of mins
    c = list_of_patterns[2::3] #list of maxs
    num_strings = len(a)
    num_mins = len(b)
    
    #for debugging
    if (num_strings) != (num_mins +1):
        print("Error: Lists are not of same size....")
    
    #initializing regex
    regex = "(" 
    
    #extending regex
    for i in range(num_mins):
        string1 = a[i]
        min1 = b[i]
        max1 = c[i]
        regex = regex + string1 + ".{" + str(min1) + ',' + str(max1) + '}'   
        
    #closing regex with last string
    regex = regex + a[num_strings-1] + ")"
        
    #extract pattern 
    match = re.findall(regex, text_file, flags=re.I)
    if not match:
        print("The pattern provided is not found in\t", text_file)
    return match

# This function extracts recursively
def extract_patterns2(text_file, list_of_patterns):
  
    #extracting strings, mins and maxs from list    
    a = list_of_patterns[0::3] #list of strings
    b = list_of_patterns[1::3] #list of mins
    c = list_of_patterns[2::3] #list of maxs
    num_strings = len(a)
    num_mins = len(b)
    
    #for debugging
    if (num_strings) != (num_mins +1):
        print("Error: Lists are not of same size....")
    
    #initializing regex
    regex = "(" 
    
    #extending regex and searching one pattern at a time (recursively)
    for i in range(num_mins):
        string1 = a[i]
        min1 = b[i]
        max1 = c[i]
        regex = regex + string1 + ".{" + str(min1) + ',' + str(max1) + '}' + '.)'
        match = re.findall(regex, text_file, flags=re.I)
        #if the 1st pattern is not there, we exit
        if not match:
            print("The ", str(i),"st pattern provided is not found in\t", text_file)
            break
        #if the 1st pattern exists, we add the second pattern to regex
        if match:
            num_chars = len(regex)
            regex = regex[0:(num_chars-2)]
        #if it makes it to the end, we add closing string
        if (i+1) == num_mins:
            print("Adding last string to pattern")
            regex = regex + a[num_strings-1] + ")"
            match = re.findall(regex, text_file, flags=re.I)
            if not match:
                print("The global pattern provided is not found in\t", text_file)
                global_match = [""]
                break
            if match:
                global_match = match
    return global_match

        



###         SOLVING CHALLENGE          ###

# Putting wikipedia article into a string
article_text = list_to_string(l2)

# Define the pattern to search here
list_of_patterns = ["duncan", 1, 25, "refer", 1, 10, "henry"]

# Extracting pattern
pattern0 = extract_patterns1(l3, list_of_patterns)
pattern1 = extract_patterns2(l3, list_of_patterns)






