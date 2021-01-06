"""Tags a file with _JEFF for all SCI tags
"""


def tag_diff(lines):
    """Assigns indicator tags to a list of lines
    """
    taggedlines = []
    for line in lines:
        taggedlines.append(tagline_diff(line))
    return taggedlines
        

def tagline_diff(line):
    """Assigns an indicator tag to a line
    """
    if line.startswith('<'):
        return line
    line = line.split()
    if len(line) == 4:
        if 'SCI1' or 'SCI2' or 'SCI1SCI1' or 'SCI2SCI1' in line:
            word, pos, lemma, tag = line
            lemma = lemma.split('-')[0]
            print(word + "\t" + pos + "\t" + lemma + "_JEFF-n\t" + tag + "\n")
            return word + "\t" + pos + "\t" + lemma + "_JEFF-n\t" + tag + "\n"
    else:
        return line
    return line


def read_vfile(fname):
    """Reads a vert file
    """
    with open(fname, 'r') as vfile:
        lines = vfile.readlines()
        return lines

def write_vfile(fname, taggedlines):
    """Writes a vert file
    """
    # write to file
    with open(fname, 'w') as outfile:
        outfile.writelines(taggedlines)
        
def tag_vert_diff(fname, fname_out):
    """Creates a new file with tags
    """
    # vertical file location

    # read vertical file
    lines = read_vfile(fname)
    # tag file    
    taggedlines = tag_diff(lines)
    # call write file
    write_vfile(fname_out, taggedlines)


def main(fname, fname_out):
    #call ti tagging
    tag_vert_diff(fname, fname_out)

if __name__ == "__main__":
    main('jefflrgmwutaggedALL2.vert', 'JEFF_diffall.vert')
