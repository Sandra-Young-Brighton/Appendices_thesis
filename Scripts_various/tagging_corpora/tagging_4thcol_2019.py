"""Tags a file with verb TI. Reads and writes vert files.
"""
import json
#from pip._vendor.pyparsing import line

VFILE = 'jeff_notags_extended2903.vert'

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
    word, pos, lemma = line.split()
    for i in indicators:
        if i == lemma.split('-')[0]:
            print(line.strip() + "\tTI\n")
            return line.strip() + "\tTI\n"
    return line

def tag_sci(lines, indicators):
    """Assigns scientific name tags to a list of lines
    """
    taggedlines = []
    for line in lines:
        taggedlines.append(tagline_sci(line, indicators))
    return taggedlines

def tagline_sci(line, names):
    """Assigns a scientific name tag to a line
    """
    if line.startswith('<'):
        return line
    try:
        word, pos, lemma = line.split()
    except ValueError:
        return line
    
    for n in names:
        if n == lemma.split('-')[0]:
            print(line.strip() + "\tSCI\n")
            return line.strip() + "\tSCI\n"
    return line

def tagline_sci_insensitive(line, names):
    """Assigns an indicator tag to a line
    """
    if line.startswith('<'):
        return line
    word, pos, lemma = line.split()
    for n in names:
        if n.lower() == lemma.split('-')[0].lower():
            print(line.strip() + "\t\tSCI\n")
            return line.strip() + "\t\tSCI\n"
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
            print(line.strip() + "\tCOM\n")
            return line.strip() + "\tCOM\n"
    return line

def tag_gen(lines, indicators):
    """Assigns general name tags to a list of lines
    """
    taggedlines = []
    for line in lines:
        taggedlines.append(tagline_gen(line, indicators))
    return taggedlines

def tagline_gen(line, names):
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
            print(line.strip() + "\tGEN\n")
            return line.strip() + "\tGEN\n"
    return line

# def import_names(fname):
#     """Loads json file and turns into a list
#     """
#     with open(fname, 'r') as gnrd_file:
#         gnrd_names = json.load(gnrd_file)
#     sci = []
#     for name in gnrd_names['names']:
#         sci.append(name['scientificName'])
#     return sci

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

def tag_vert_sci(fname, fname_out, names):
    """Creates a new file with tags
    """
    # vertical file location
    # make list of species names
    # read vertical file
    lines = read_vfile(fname)
    # tag file    
    taggedlines = tag_sci(lines, names)
    # call write file
    write_vfile(fname_out, taggedlines)

def tag_vert_com(fname, fname_out, names=None):
    """Creates a new file with tags
    """
    # vertical file location
    # make list of species names
    if not names:
        names = ['waterstrider', 'strider', 'roach', 'perch', 'trout', 'salmon', 'alga', 'bluegill', 'bullhead',
                 'chironomid', 'eel', 'mayfly', 'minnow', 'zooplankton']
    # read vertical file
    lines = read_vfile(fname)
    # tag file    
    taggedlines = tag_com(lines, names)
    # call write file
    write_vfile(fname_out, taggedlines)

def tag_vert_gen(fname, fname_out, names=None):
    """Creates a new file with tags
    """
    # vertical file location
    # make list of species names
    if not names:
        names = ['bacterium', 'consumer', 'fish', 'invertebrate', 'male', 'species', 'specie', 
                 'nymph', 'parr', 'predator', 'prey', 'resource', 'shoal', 'insect', 'organism', 'food', 'larva', 'egg']
    # read vertical file
    lines = read_vfile(fname)
    # tag file    
    taggedlines = tag_gen(lines, names)
    # call write file
    write_vfile(fname_out, taggedlines)
    

def main(fname, fname_out, gnrd_names):
    #call ti tagging
    tag_vert_ti(fname, 'tmpTI.vert')
    # import name file
    sci = []
    lines = open(gnrd_names).readlines()
    for line in lines:
        line = line.strip()
        sci.append(line)
    #call sci_name tagging
    tag_vert_sci('tmpTI.vert', 'tmpSCI.vert', sci)
    #call com_name tagging
    tag_vert_com('tmpSCI.vert', 'tmpCOM.vert')
    #call gen_name tagging
    tag_vert_gen('tmpCOM.vert', fname_out)

if __name__ == "__main__":
    main('jeff_large_nospaces_2.vert', 'jeff_large_4thcol.vert', 'names_list_nospace.txt')
