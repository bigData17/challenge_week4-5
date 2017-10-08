### ____________ useful functions ____________ ###


def xml2soup(xmlfile, tag):
    '''
    Description: finds tag instances in an xml file and outputs
    BeautifulSoup objects containing all instances found.
        INPUT: Xml file, tag (both as strings, ex: "split1.xml", "titles")
        OUTPUT: BeautifulSoup object with tag matches 
    '''
    from bs4 import BeautifulSoup
    #The line below works for Python 3, let me know if in Python 2 it doesn't work
    infile = open(xmlfile,"r", encoding='utf8')
    contents = infile.read()
    soup = BeautifulSoup(contents,'xml')
    return soup.find_all(tag)

    
def soup2list(object):   
    '''
    Description: creates a list from soup object, where each element in the list
    corresponds to different tag instances, and where the instances are cleaned:
    they are all converted to lowercase and linebreaks are removed.
        INPUT: BeautifulSoup object
        OUPUT: List. Each element is a different instace in the object
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
        if "#redirect" in mylist[i]:  
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
    a =  string.punctuation + string.ascii_lowercase 
    dict1 = {}; num_i = len(t_list); num_j = len(a) 
    i = 0; j = 0; not_found = []         
    while (i < num_i) & (j < num_j):
        # if 1st letter does not match 1st key, we skip to the next key     
        if t_list[i][0] != a[j]:
            not_found.append(str(a[j]))
            j= j +1            
            
        # if 1st letter matches key, we store (start, end) index in values, and
        # we skip to the next title in the list
        if t_list[i][0] == a[j]:
            start = i; end = i
            while t_list[i][0] == a[j]:
                end = end +1
                i = i +1
            dict1[str(a[j])] = (start,end-1)
            j = j +1
    return dict1 
            
            
   
### _____________ main _____________ ###


# Extracting targets from XML file
titles = xml2soup("wiki_sample", 'title')
articles = xml2soup("wiki_sample", 'text')

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
#t_list, a_list, sort_idx = sortABC(t_list, a_list)

# Creating dict with search index as tuple (Currently being debugged)
#dict1 = searchABC(t_list)

# Storing data as txt files 
list2txt('wiki_astext.txt', a_list)
list2txt('titles_astext.txt', t_list)
