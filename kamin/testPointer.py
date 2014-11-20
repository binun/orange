import pickle

class B(object):
    def __init__(self):
        print 'Perhaps __init__ must not happen twice?'
        print
        self.val = 100

    def __str__(self):
        """What a looks like if your print it"""
        return 'B:'+str(self.val)

    def __getstate__(self):
        return self.val

    def __setstate__(self,val):
        self.val = val

b = B()
b_pickled = pickle.dumps(b)
b.val = 200
b2 = pickle.loads(b_pickled)
print 'the original b'
print b
print # newline
print 'b2 - b clone of b before we changed the value'
print b2

print b_pickled
