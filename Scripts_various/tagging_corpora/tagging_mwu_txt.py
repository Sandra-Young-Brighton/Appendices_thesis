'''
Created on 5 Jul 2017

@author: sandra
'''
def import_names(name_list):
    """Loads text file and turns into a list
    """
    file = open(names_list)
    names = []
    for line in file:
        line = line.strip('\n')
        line = line.strip('\r')
        line = line.strip(' ')
        names.append(line)
    return names

def split_line(line):
    """Split a line into four parts, word, pos, lemma and tag."""
    # TODO: Speak to Diana about the spaces in the vert file - do they mean
    # anything?
    line = line.strip().split()
    if len(line) == 0:
        return line
    elif len(line) > 4:
        return line
    elif len(line) == 1:
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
    def __init__(self, f_in, f_out, n, name_list, indicators=None):
        """Populate the buffer."""
        # read the input vert file
        self.f_in = open(f_in, 'r')
        # populate the buffer (first n lines of the vert file))
        self.buffer = []
        for i in range(n):
            self.buffer.append(split_line(self.f_in.readline()))
        # read in list of names or save
        self.names = import_names(name_list)
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
            elif tagged_line[0].startswith('>'):
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
        mwutagger = MWUTagger('extended_notags.vert', 'extended_oncmy_tagged.vert', 2, 'names_oncorhynchus_mykiss.txt')
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
    mwutagger = MWUTagger('extended_notags.vert', 'extended_oncmy_tagged.vert', 2, 'names_oncorhynchus_mykiss.txt')
    name = mwutagger.names
    while True:
        try:
            mwutagger.check_for_name(name)
            mwutagger.__next__()
        except StopIteration:
            break

if __name__ == '__main__':
    main ()
