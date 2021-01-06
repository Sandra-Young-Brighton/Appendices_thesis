"""Tags a file with one word GEN, COM, TI names, with extra breakdown. Reads and writes vert files.
"""


VFILE = 'jefflrgmwutagged.vert'

def tag_ti(lines, indicators):
    """Assigns indicator tags to a list of lines
    """
    taggedlines = []
    for line in lines:
        taggedlines.append(tagline_ti(line, indicators))
    return taggedlines
        

def tagline_ti(line, indicators):
    """Assigns an indicator tag to a line
    """
    if line.startswith('<'):
        return line
    try: 
        word, pos, lemma = line.split()
    except ValueError:
        return line
    
    for i in indicators:
        if i == lemma.split('-')[0]:
            print(line.strip() + "\tTI\n")
            return line.strip() + "\tTI\n"
    return line

def tag_com(lines, indicators):
    """Assigns common name tags to a list of lines
    """
    taggedlines = []
    for line in lines:
        taggedlines.append(tagline_com(line, indicators))
    return taggedlines

def tagline_com(line, names):
    """Assigns a common name tag to a line
    """
    if line.startswith('<'):
        return line
    try:
        word, pos, lemma = line.split()
    except ValueError:
        return line
    
    for n in names:
        if n == lemma.split('-')[0]:
            print(line.strip() + "\tNCOM\n")
            return line.strip() + "\tNCOM\n"
    return line

def tag_gencoll(lines, indicators):
    """Assigns general name tags to a list of lines
    """
    taggedlines = []
    for line in lines:
        taggedlines.append(tagline_gencoll(line, indicators))
    return taggedlines

def tagline_gencoll(line, names):
    """Assigns a general name tag to a line
    """
    if line.startswith('<'):
        return line
    try:
        word, pos, lemma = line.split()
    except ValueError:
        return line
    
    for n in names:
        if n == lemma.split('-')[0]:
            print(line.strip() + "\tNGENCOLL\n")
            return line.strip() + "\tNGENCOLL\n"
    return line

def tag_genprt(lines, indicators):
    """Assigns general name tags to a list of lines
    """
    taggedlines = []
    for line in lines:
        taggedlines.append(tagline_genprt(line, indicators))
    return taggedlines

def tagline_genprt(line, names):
    """Assigns a general name tag to a line
    """
    if line.startswith('<'):
        return line
    try:
        word, pos, lemma = line.split()
    except ValueError:
        return line
    
    for n in names:
        if n == lemma.split('-')[0]:
            print(line.strip() + "\tNGENPRT\n")
            return line.strip() + "\tNGENPRT\n"
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

def tag_vert_ti(fname, fname_out, indicators=None):
    """Creates a new file with tags
    """
    # vertical file location
    # make list of trophic indicators
    if not indicators:
        indicators = ['eat', 'consume', 'feed']
    # read vertical file
    lines = read_vfile(fname)
    # tag file    
    taggedlines = tag_ti(lines, indicators)
    # call write file
    write_vfile(fname_out, taggedlines)
        
def tag_vert_com(fname, fname_out, names=None):
    """Creates a new file with tags
    """
    # vertical file location
    # make list of species names
    if not names:
        names = ['perch', 'trout', 'salmon', 'eel', 'chub', 'stickleback', 'goby', 'whitefish']
    # read vertical file
    lines = read_vfile(fname)
    # tag file    
    taggedlines = tag_com(lines, names)
    # call write file
    write_vfile(fname_out, taggedlines)

def tag_vert_gencoll(fname, fname_out, names=None):
    """Creates a new file with tags
    """
    # vertical file location
    # make list of species names
    if not names:
        names = ['species', 'specie', 'insect', 'animal', 'fish', 'plant']
    # read vertical file
    lines = read_vfile(fname)
    # tag file    
    taggedlines = tag_gencoll(lines, names)
    # call write file
    write_vfile(fname_out, taggedlines)

def tag_vert_genprt(fname, fname_out, names=None):
    """Creates a new file with tags
    """
    # vertical file location
    # make list of species names
    if not names:
        names = ['nymph', 'parr', 'larvae', 'larva', 'egg']
    # read vertical file
    lines = read_vfile(fname)
    # tag file    
    taggedlines = tag_genprt(lines, names)
    # call write file
    write_vfile(fname_out, taggedlines)
    
def main(fname, fname_out):
    #call ti tagging
    tag_vert_ti(fname, 'tmpTI.vert')
    # import name file
    #call com_name tagging
    tag_vert_com('tmpTI.vert', 'tmpCOM4.vert')
	#call gencoll_name tagging
    tag_vert_gencoll('tmpCOM4.vert', 'tmpGENCOLL4.vert')
    #call gen_name tagging
    tag_vert_genprt('tmpGENCOLL4.vert', fname_out)

if __name__ == "__main__":
    main('jefflrgmwutagged.vert', 'jefflrgmwutaggedALL_TI.vert')
