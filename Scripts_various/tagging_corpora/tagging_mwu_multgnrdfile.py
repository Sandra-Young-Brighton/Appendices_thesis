'''
Created on 5 Jul 2017

@author: sandra
'''
import json
import os


def split_line(line):
    """Split a line into four parts, word, pos, lemma and tag."""
    # TODO: Speak to Diana about the spaces in the vert file - do they mean
    # anything?
    line = line.strip().split()
    if len(line) == 1:
        word = line[0]
        pos, lemma, trophic, sci = None, None, None, None
    elif len(line) == 3:
        word, pos, lemma = line
        trophic = ''
        sci = ''
    elif len(line) == 4:
        word, pos, lemma, trophic = line
    elif len(line) == 5:
        word, pos, lemma, trophic, sci = line
    return [word, pos, lemma, trophic, sci]

def import_names():
    """Loads json file and turns into a list
    """
#     path = './output/'
#     filelist = os.listdir(path)
#     
#     sci = []
#     for file in filelist:
#         with open(path+file, 'r') as gnrd_file:
#             gnrd_names = json.load(gnrd_file)
#         
#             for name in gnrd_names['names']:
#                 sci.append(name['scientificName'])
#     list_nodup = list(set(sci))
#     return list_nodup

    gnrd_file = open('names_lists.txt', 'r')
    lines = gnrd_file.readlines()
    sci = []
    for line in lines:
        sci.append(line.strip())
    #print(sci)
    return sci        


class MWUTagger(object):
    """Contains a buffer of lines split into word, pos, lemma, tag items."""
    def __init__(self, f_in, f_out, n, indicators=None):
        """Populate the buffer."""
        # read the input vert file
        self.f_in = open(f_in, 'r')
        # populate the buffer (first n lines of the vert file)
        self.buffer = []
        for i in range(n):
            self.buffer.append(split_line(self.f_in.readline()))
        # read in list of names or save
        self.names = import_names()
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
                print('\t'.join(tagged_line) + '\n')
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
        mwutagger = MWUTagger('JEFF_extendedonly.vert', 'JEFF_extendedMWUtag.vert', 2)
        # check if tagged
        if self.buffer[0][-1] == 'SCI1':
            return
        for name in mwutagger.names:
            name = name.strip().split()
            name = [n + '-n' for n in name]
            n = len(name)
            # check if they match
            candidate = [line[2] for line in self.buffer[:n]]
            if name == candidate:
                # edit the tags in the first n items in the buffer if they do
                for i in range(n):
                    self.buffer[i][-1] += "SCI%i" % (i + 1)

         
    def check_for_ti(self, ti):
        """Depending on length of TI, check if the first n items in the buffer
        match name."""
        # check if they match
        if self.buffer[0][-1] == 'TI':
            return
        ti = ti.strip().split()
        n = len(ti)
        # check if they match
        if ti == [line[2] for line in self.buffer[:n]]:
            # edit the tags in the first n items in the buffer if they do
            for i in range(n):
                self.buffer[i][-1] + "TI%i" % (i + 1)


def main():
    mwutagger = MWUTagger('JEFF_extendedonly.vert', 'JEFF_extendedMWUtag.vert', 2)
    name = mwutagger.names
    while True:
        try:
            mwutagger.check_for_name(name)
            mwutagger.__next__()
        except StopIteration:
            break

if __name__ == '__main__':
    main ()
