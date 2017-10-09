### ____________ useful functions ____________ ###


def xml2soup(xmlfile, tag1, tag2):
    '''
    Description: finds tag instances in an xml file and outputs
    BeautifulSoup objects containing all instances found.
        INPUT: Xml file, tag1 = titles, tag2 = articles/text
                (both as strings, ex: "split1.xml", "title", "text")
        OUTPUT: Two lists of BeautifulSoup objects with respective tag matches 
    '''
    from bs4 import BeautifulSoup
    #The line below works for Python 3, let me know if in Python 2 it doesn't work
    infile = open(xmlfile,"r", encoding='utf8')
    contents = infile.read()
    soup = BeautifulSoup(contents,'xml')
    list_of_titlesoups = []; list_of_articlesoups = []
    #grabbing only articles (aka entries where namespace = 0)
    for entry in soup.find_all('page'):
        if entry.ns.string == '0':
            list_of_titlesoups.append(entry.find(tag1))
            list_of_articlesoups.append(entry.find(tag2))
    return list_of_titlesoups, list_of_articlesoups #soup.find_all(tag)

    
def soup2list(object):   
    '''
    Description: creates a list from soup object, where each element in the list
    corresponds to different tag instances, and where the instances are cleaned:
    they are all converted to lowercase and linebreaks are removed.
        INPUT: List of BeautifulSoup objects
        OUPUT: List. Each element is a different instance in the object
    '''
    return [object[i].get_text().lower().replace('\n', ' ').replace('\r', '') for i in range(0, len(object))]


def remove_redirects(mylist):
    '''
    Description: removes redirect wiki entries from the list provided
        INPUT: List of tag instances
        OUPUT: Tuple of lists: (updated_list, keep_index, remove_index)
    '''    
    # Finding index of all #redirects
    rm_idx = []
    keep_idx = []
    num = len(mylist)
    for i in range(num):
        # [ ] Elaborate condition more such that it only skips true redirects and not articles
        # that may contain by chance the string #redirect
        if "#redirect" in mylist[i][0:20]:  
            rm_idx.append(i)
        else:
            keep_idx.append(i)
         
    # Removing/Skipping Redirects, and returning indexes       
    return [mylist[i] for i in keep_idx], keep_idx, rm_idx


def list2txt(filename, mylist):
    '''
    Description: creates a txt file where each line in the txt file comes from
    each element in the list provided.
        INPUT: Name of txt file desired (as string), list containing data
        OUTPUT: txt file 
    '''
    with open(filename, 'w', encoding='utf8') as f:
        for s in mylist:
            f.write("%s\n" % s)
    f.close()


def check_length(list1, list2):
    # Debugging: we should have the same number of articles and titles
    num_t = len(list1); num_a = len(list2)
    if num_t != num_a:
        print("ERROR: Length of List1 and List2 is not the same: ", num_t, ":", num_a)
    if num_t == num_a:
        print("SUCCESS: Both lists are of same length")
        
        
def sortABC(titles_list, articles_list):
    '''
    Description: sorts titles_list alphabetically, then uses that index to sort
    the articles_list.
        INPUT: Two lists of same length: titles_list and articles_list
        OUTPUT: Tuple of 3 lists: titles_list_sorted, articles_list_sorted, index_used
    '''
    a = titles_list; b = articles_list; 
    sort_idx = sorted(range(len(a)), key=lambda k: a[k])
    print("SORT_ABC: SUCCESS: Titles list has been sorted alphanumerically")
    return sorted(a), [b[i] for i in sort_idx], sort_idx

def searchABC(t_list):
    '''
    Description: takes an alphabetically sorted list of titles, and creates
    a dictionary of keys: "character to search", values: "index of where to find them"
    INPUT: Alphabetically sorted list
    OUPUT: Dictionary, for example:
            {'A' : 0:15, 'B' : 16:20, .... 'Z' : 450:500}
    '''
    import string
    a =  string.punctuation + string.digits + string.ascii_lowercase 
    dict1 = {}; num_i = len(t_list); num_j = len(a) 
    i = 0; j = 0; not_found = []; special_characters = []     
    while (i < num_i) and (j < num_j):
        # if 1st letter does not match 1st key, we skip to the next key     
        if t_list[i][0] != a[j]:
            not_found.append(str(a[j]))
            j= j +1  ; #print("First if block: i=", i, "j=", j)          
            
        # if 1st letter matches key, we store (start, end) index in values, and
        # we skip to the next title in the list
        if t_list[i][0] == a[j]:
            start = i; end = i
            while (t_list[i][0] == a[j]) and (i <= num_i-1):
                #print("Second if block (inside while) : i=", i, "j=", j, "end= ", end)
                if i == (num_i -1):
                    print("SEARCH_ABC: 1Finished iterating over titles list")
                    break;
                end = end +1
                i = i +1; 

            dict1[str(a[j])] = (start,end-1)
            j = j +1; #print("Second if block (outside while): i=", i, "j=", j)
            
        if i == (num_i -1):
            print("SEARCH_ABC: 2Finished iterating over titles list")
            break;
        # if there are titles that start with a letter/character that is not found in a list     
        if (i == num_i) and (j < num_j):
            print("SEARCH_ABC: ERROR: Character ", str(a[j]), "is not found in string list privided:\n\t", str(a))
            print("Third if block: i=", i, "j=", j)
            
        if (i <= num_i) and (j == num_j):
            for k in range(i, num_i):
                special_characters.append(t_list[k][0])
                #print("Fourth if block: i=", i, "j=", j)
            print("SEARCH_ABC: The following characters were not binned in dictionary: \n\t", special_characters)
            print("SEARCH_ABC: 3Finished iterating over titles list")
            
    print("SEARCH_ABC: Last check: i=", i, "num_i= ", num_i, "j=", j, "num_j=", num_j)
    return dict1, not_found, special_characters
            

def list2bagofwords(a_list):
    '''
    INPUT: list of all articles in entire wiki xml file
    OUTPUT: List where each element is a bag of words (a set) for each article 
    '''
    import collections, re
    bagsofwords = [ collections.Counter(re.findall(r'\w+', txt)) for txt in a_list]
    temp = [bagsofwords[i].keys() for i in range(len(bagsofwords))]
    return [set(temp[i]) for i in range(len(bagsofwords))]

def wiki2bagofwords(wiki_string):
    '''
    INPUT: One string that captures the entire wiki file
    OUTPUT: a set of words (bag of words) of that entire wiki file
    '''
    import collections, re
    return {collections.Counter(re.findall(r'\w+', wiki_string))}

    
def which_lines(list_keywords, list_baos): #still debugging
    '''
    INPUT: list of keywords in pattern, entire wiki bag of words, list where each 
        element is an article's bag of words  
    OUTPUT: a list contatining the index of lines in the .txt file that contain
        the pattern keywords
    '''
    index = []
    for i in range(len(list_baos)):
        if list_keywords[0] in list_baos[i] and list_keywords[1] in list_baos[i] and list_keywords[2] in list_baos[i]:
            index.append(i)
    if not index:
        print("WHICH_LINES: The keywords provided were not found in any of the lines in", list_baos)
    else:
        print("WHICH_LINES: The keywords provided were found in ", len(index), "lines: \n\tLines:", index)
    return index


def smart_search(lines_index, a_list):
    '''
    INPUT: lines_index list (output from which_lines), and processed articles_list
    OUPUT: subset of a_list containing only articles which contain the keywords in pattern to search
    '''
    return [a_list[i] for i in lines_index]


def extract_patterns(smart_list, list_of_patterns): #text_file
    '''
    Description: This matches (and returns) the entire pattern provided (non-recursively)
    found in the string provided
    INPUT: string, a list whose elements are the patterns to search for in string
    OUPUT: a list of unique matches found
    TO DO:
        [x] Make it accept a list of strings
        [] Make it returns matches within matches, [x]and return only unique matches
        [] Change the list_of_patterns to match exactly as in the gdoc "str1" "[1,5]" "str2"
    '''
    #regex library
    import re
    
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
    match_list = []
    for i in range(0, len(smart_list)):
       current_match = re.findall(regex, smart_list[i], flags=re.I)
       if current_match:
           match_list.append(set(current_match))
           
    if not match_list:
        print("EXTRACT_PATTERNS: The pattern provided is not found in list of articles provided")
    return match_list
    


### _____________ main _____________ ###


############ PREPROCESSING DATA #########################

# Extracting targets from XML file
titles, articles = xml2soup("wiki_sample", 'title', 'text')

# Preprocessing data and storing in lists
t_list = soup2list(titles)
a_list = soup2list(articles)

# Debugging
check_length(t_list, a_list)

# Removing redirects
a_list, keep_idx, _ = remove_redirects(a_list)

# Removing redirects from titles using index from articles
t_list = [t_list[i] for i in keep_idx]

# Debugging
check_length(t_list, a_list)

# Reogranizing entries alphabetically
t_list, a_list, sort_idx = sortABC(t_list, a_list)

# Creating dict with search index as tuple (Currently being debugged)
# not_found is a list of characters which were not found in the 1st letter
# of the title for all titles found in the xml file provided
dict1, not_found, special_characters = searchABC(t_list)

# Creating a BAO (bag of words) for each article
list_of_baos = list2bagofwords(a_list)



############   QUERY TIME   #############################

# Enter the keywords you would like to search on wiki below:
keywords = ["the", "going", "on"]

# Define the pattern to search here
list_of_patterns = ["the", 1, 25, "going", 1, 10, "on"]

# Finding the index of lines (which articles) that contain those words
lines_index = which_lines(keywords, list_of_baos)

# Creating a reduced list of only articles that contain the pattern keywords
smart_articles_list = smart_search(lines_index, a_list)
'''
Optimization Note: The above can be optimized using cython. Instead of creating a subset of
the original file, we can simply create an array of pointers that point
to those lines, hence more memory efficient and faster. '''


# Storing data as txt files 
#list2txt('wiki_astext.txt', smart_articles_list)
#list2txt('titles_astext.txt', t_list)
'''
Optimization Note: The above could be optimized if we completely skipt it. That is,
instead of converting to txt file, we could simply feed the regex functions a list of 
strings to iterate over. Also, I'm not sure if converting to t_list to txt is necessary'''


# Extracting matches
patterns = extract_patterns(smart_articles_list, list_of_patterns)
print(patterns)




