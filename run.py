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
    return urlopen(link).read()

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
    # extracts all links from a URL and returns them as a list
    # by: Cody Kochmann
    def grep(link):
        try:
            from urllib2 import urlopen
            response = urlopen(link)
            return(response.read())
        except:
            pass
    def check_if_link(s,req_http=True):
        # Checks at the input is a legitimate link.
        allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'*+,;=%"
        if req_http and "http" not in s:
            return(False)
        if "://" in s:
            for i in s:
                if i not in allowed_chars:
                    return(False)
            return(True)
        return(False)
    
    c_links = []
    link_being_built = ""
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&*+,;=%"
    collected_html=grep(url)
    if collected_html is not None:
        for i in collected_html:
            if i in allowed_chars:
                link_being_built+=i
            else:
                if link_being_built not in c_links:
                    if check_if_link(link_being_built):
                        if ".html" not in link_being_built:
                            c_links.append(link_being_built)
                link_being_built=""
    return(c_links)

def collect_links(links):
    collected_links=[]
    output = []
    for i in links:
        for link in list(extract_links(i)):
            correct = False
            for t in filetypes_you_want:
                if t in link:
                    correct = True
            if correct:
                output.append(link)
                print(link)
    return(output)

def list_dir(d):
    from os import listdir
    return(listdir(d))

def random_string():
    import random
    import string
    return "".join([random.SystemRandom().choice(string.digits + string.letters) for i in range(16)])

def download_file(url):
        from urllib2 import urlopen
        file_n = url.split('/')[-1]
        output_path = script_path()+"pictures/"
        if "?" in file_n or len(file_n) > 30:
            for i in filetypes_you_want:
                if i in file_n:
                    file_n=random_string()+i
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


