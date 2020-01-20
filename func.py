class MyNews(object):
    def __init__(self,label,title,url):
        self.label = label
        self.title = title
        self.url = url

def checkIfExists(label, newsFlow):
    for item in newsFlow:
        if item.label == label:
            return True
    return False