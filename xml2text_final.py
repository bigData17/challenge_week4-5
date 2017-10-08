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
                end = end +1
                i = i +1; 
                if i == (num_i -1):
                    print("Finished iterating over titles list")
                    break;
            dict1[str(a[j])] = (start,end-1)
            j = j +1; #print("Second if block (outside while): i=", i, "j=", j)
            
        if i == (num_i -1):
            break;
        # if there are titles that start with a letter/character that is not found in a list     
        if (i == num_i) and (j < num_j):
            print("ERROR: Character ", str(a[j]), "is not found in string list privided:\n\t", str(a))
            print("Third if block: i=", i, "j=", j)
            
        if (i <= num_i) and (j == num_j):
            for k in range(i, num_i):
                special_characters.append(t_list[k][0])
                #print("Fourth if block: i=", i, "j=", j)
            print("The following characters were not binned in dictionary: \n\t", special_characters)
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
        if list_keywords[0] in list_baos and list_keywords[1] in list_baos and list_keywords[3] in list_baos:
            index.append(i)
    return index


def smart_search(lines_index, a_list):
    '''
    INPUT: lines_index list (output from which_lines), and processed articles_list
    OUPUT: subset of a_list containing only articles which contain the keywords in pattern to search
    '''
    return [a_list[i] for i in lines_index]
    


### _____________ main _____________ ###


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

# Creating a BAO (bag of words) for each article
list_of_baos = list2bagofwords(a_list)

# Finding the index of lines to search in
lines_index = which_lines(["the", "going", "for"], list_of_baos)

# Creating a reduced list of only articles that contain the pattern keywords
smart_articles_list = smart_search(lines_index, a_list)

# Creating dict with search index as tuple (Currently being debugged)
# not_found is a list of characters which were not found in the 1st letter
# of the title for all titles found in the xml file provided
dict1, not_found, special_characters = searchABC(t_list)

# Storing data as txt files 
list2txt('wiki_astext.txt', a_list)
list2txt('titles_astext.txt', t_list)

