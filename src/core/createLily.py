#createLily.py
# Open the file

def createFile(staffu, staffl):
    fh = open('output.ly', "w")


    # Setting up the ly file
    v = "version"
    vn = '"2.18.2"'
    version = r"\{} {}".format(v, vn)
    l = "language"
    lang = '"english"'
    language = r"\{} {}".format(l, lang)

    # Writing setup into file
    fh.write(version + "\n")
    fh.write(language + "\n")

    # Setting up header block (Inputs will be specified by GUI)
    fbrac = '{'
    bbrac = '}'
    comm = '"'
    songName = '"Song Name"'
    composer = 'Username' 
    tagLine = '"Copyright: '

    title2 = r"""\header {}
        title = {}
        composer = {}{}{}
        tagline = {}{}{}
    {}""".format(fbrac, songName, 
                comm, composer, comm, 
                tagLine, composer, comm,
                bbrac)


    # Writing header into file
    fh.write(title2 + "\n")

    #Setting up 
    relative = r"\{} {}".format("relative","c'")
    #fh.write(relative + "\n")
    #Will probably implement the use of another staff (bass clef)
    staffh = "{\n\\new PianoStaff << \n"
    staffh += "  \\new Staff { \clef treble " + staffu + r'\bar "|."' + "}\n"
    staffh += "  \\new Staff { \clef bass " + staffl + r'\bar "|."' + "}\n"  #r prefix messed it up
    staffh += ">>\n}\n"

    fh.write(staffh + "\n")

    # Closing file handling
    fh.close()
