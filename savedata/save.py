import json
from collections import defaultdict
class Save:
    def __init__(self,filename):
        self.filename = filename
        self.data = None
        self.lsts = defaultdict(list)
        self.load()

    def load(self):
        with open(self.filename,'r') as f:
            self.data = json.loads(f.read())
        self.load_lst()

    def load_lst(self):
        for lvl,dat in self.data.items():
            if dat['completed']:
                self.lsts['completed'].append(lvl)
            else:
                self.lsts['incompleted'].append(lvl)

    def getcompleted(self):
        return self.lsts.get('completed',[])
    
    def getincompleted(self):
        return self.lsts.get('incompleted',[])
    
    def change_stat(self,lvl,stat = True):
        self.data[lvl]['completed'] = stat

        with open(self.filename,'w') as f:
            f.write(json.dumps(self.data))
        self.load_lst()

    def is_complete(self,lvl):
        self.change_stat(lvl)
        
        

    
        


