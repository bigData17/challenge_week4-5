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




### _____________ main _____________ ###


# Extracting targets from XML file
titles = xml2soup("split1.xml", 'title')
articles = xml2soup("split1.xml", 'text')

# Preprocessing data and storing in lists
t_list = soup2list(titles)
a_list = soup2list(articles)

# Debugging
check_length(t_list, a_list)

# Removing redirects
a_list_updated, keep_idx, _ = remove_redirects(a_list)

# Removing redirects from titles using index from articles
t_list_updated = [t_list[i] for i in keep_idx]

# Debugging
check_length(t_list_updated, a_list_updated)

# Storing data as txt files 
list2txt('wiki_astext.txt', a_list_updated)
list2txt('titles_astext.txt', t_list_updated)
