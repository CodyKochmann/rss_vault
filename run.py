#1/usr/bin/env python
# rss locker

filetypes_you_want = ".jpg .png .tiff .gif .jpeg .webp".split(" ")

def get_file_text(file_path):
    # returns all text from a file. 
    # Warning this may block up scripts for long files.
    with open(file_path,"r") as f:
        return(str(f.read()))

def script_path(include_name=False):
    from os import path
    full_path = path.realpath(__file__)
    if include_name:
        return(full_path)
    else:
        full_path = "/".join( full_path.split("/")[0:-1] ) + "/"
        return(full_path)

def grep(link):
    from urllib2 import urlopen
    response = urlopen(link)
    return(response.read())

def check_if_link(s,req_http=True):
    # Checks at the input is a legitimate link.
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;=%"
    if req_http and "http" not in s:
        return(False)
    if "://" in s:
        for i in s:
            if i not in allowed_chars:
                return(False)
        return(True)
    return(False)

def extract_links(url):
    # extracts all links from a URL and returns them
    def grep(link):
        from urllib2 import urlopen
        response = urlopen(link)
        return(response.read())

    def check_if_link(s,req_http=True):
        # Checks at the input is a legitimate link.
        allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;=%"
        if req_http and "http" not in s:
            return(False)
        if "://" in s:
            for i in s:
                if i not in allowed_chars:
                    return(False)
            return(True)
        return(False)
    
    collected_links = []
    link_being_built = ""
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&()*+,;=%"
    collected_html= grep(url)
    for i in collected_html:
        if i in allowed_chars:
            link_being_built+=i
        else:
            if link_being_built not in collected_links:
                if check_if_link(link_being_built):
                    collected_links.append(link_being_built)
            link_being_built=""
    return(collected_links)

def collect_links(links):
    collected_links=[]
    output = []
    for i in links:
        # gather all of the links
        for link in extract_links(i):
            collected_links.append(link)

    for i in collected_links:
        # Filter the links to just the images
        correct = False
        for t in filetypes_you_want:
            if t in i:
                correct = True
        if correct:
            output.append(i)
    return(output)

def list_dir(d):
    from os import listdir
    return(listdir(d))

def download_file(url):
    from urllib2 import urlopen
    file_n = url.split('/')[-1]
    output_path = script_path()+"pictures/"
    if file_n in list_dir(output_path):
        print(file_n+" already downloaded")
        return(False)
    print("downloading: "+file_n)
    response = urlopen(url)
    data = response.read()
    with open(output_path+file_n, "w") as f:
        f.write(data)
    print("finished: "+file_n)

def multithreaded_process(arg_list, run_process, max_threads=4):
    # runs arg_list through run_process multithreaded
    from multiprocessing import Pool
    pool = Pool(max_threads) # how much parallelism?
    pool.map(run_process, arg_list)

feeds = get_file_text(script_path()+"feed_urls.txt").split("\n")
for i in list(feeds):
    if check_if_link(i) is False:
        feeds.remove(i)

target_files = collect_links(feeds)
multithreaded_process(target_files, download_file)


