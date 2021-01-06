'''
Created on 5 Jul 2017

@author: sandra
'''
import json
#from tagging import import_names
import pandas as pd

def import_names(vto_file):
    #import vto_file
    df_vto = pd.read_csv(vto_file)
    names = df_vto['name'].tolist()
    #print(names)
    return names

def split_line(line):
    """Split a line into four parts, word, pos, lemma and tag."""
    # TODO: Speak to Diana about the spaces in the vert file - do they mean
    # anything?
    line = line.strip().split()
    if len(line) == 1:
        word = line[0]
        pos, lemma, tag = None, None, None
    elif len(line) == 3:
        word, pos, lemma = line
        tag = ''
    elif len(line) == 4:
        word, pos, lemma, tag = line
    return [word, pos, lemma, tag]


class MWUTagger(object):
    """Contains a buffer of lines split into word, pos, lemma, tag items."""
    def __init__(self, f_in, f_out, n, vto_file, indicators=None):
        """Populate the buffer."""
        # read the input vert file
        self.f_in = open(f_in, 'r')
        # populate the buffer (first n lines of the vert file)
        self.buffer = []
        for i in range(n):
            self.buffer.append(split_line(self.f_in.readline()))
        # read in list of names or save
        self.names = import_names(vto_file)
        # create the output vert file
        self.f_out = f_out

    def __iter__(self):
        return self
    
    def write_line(self):
        """Write out the oldest line in the buffer, and add a new line to the buffer."""
        # write the oldest line from the buffer
        tagged_line = self.buffer.pop(0)
        tagged_line = [i for i in tagged_line if i]
        with open(self.f_out, 'a') as f:
            if tagged_line[0].startswith('<') and tagged_line[-1].endswith('>'):
                f.write(' '.join(tagged_line) + '\n')
                return  ' '.join(tagged_line) + '\n'
            else:
                f.write('\t'.join(tagged_line) + '\n')
                #print('\t'.join(tagged_line) + '\n')
                return  '\t'.join(tagged_line) + '\n'

    def __next__(self):
        """write out the oldest line in the buffer and add a new line to the buffer"""
        #write the oldest line from the buffer
        self.write_line()
        # add a new line to the buffer (found an example here https://bufferoverflow.com/a/14797993/1706564)
        line = self.f_in.readline()
        if line:
            self.buffer.append(split_line(line))
        else:
            self.f_in.close()
            self.flush()
            raise StopIteration
    
    def flush(self):
        """Write all remaining lines from buffer file to the output file"""
        while self.buffer:
            self.write_line()

    def check_for_name(self, name):
        """Depending on length of name, check if the first n items in the buffer
        match name."""
        mwutagger = MWUTagger('jefflrgmwutaggedALL2.vert', 'jefflrgmwutagged_div.vert', 2, 'VTO_salmonidae_190619.csv')
        # check if tagged
        #if self.buffer[0][-1] == 'SCI1':
        #    return
        for name in mwutagger.names:
            name = name.strip().split()
            name = [n + '-n' for n in name]
            n = len(name)

            # check if they match
            candidate = [line[2] for line in self.buffer[:n]]
            if name == candidate:
                print('1:' + str(n))
                # edit the tags in the first n items in the buffer if they do
                for i in range(n):
                    if '_JEFF-n' in self.buffer[i][-2]:
                        continue
                    else:
                        self.buffer[i][-2] = self.buffer[i][-2].replace('-n', '_JEFF-n') 
                    i += 1 
                print('2:' + str(self.buffer))
                    
def main():
    mwutagger = MWUTagger('jefflrgmwutaggedALL2.vert', 'jefflrgmwutagged_div.vert', 2, 'VTO_salmonidae_190619.csv')
    name = mwutagger.names
    while True:
        try:
            mwutagger.check_for_name(name)
            mwutagger.__next__()
        except StopIteration:
            break

if __name__ == '__main__':
    main ()
