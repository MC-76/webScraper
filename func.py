class MyNews(object):
    def __init__(self,label,title,url):
        self.label = label
        self.title = title
        self.url = url

def checkIfExists(title, newsFlow):
    for item in newsFlow:
        if item.title in title:
            return True
    return False