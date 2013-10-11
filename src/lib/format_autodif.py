"""
MagPy
Auxiliary input filter - Env05 data
Written by Roman Leonhardt June 2012
- contains test and read function, toDo: write function
"""

from stream import *

def isAUTODIF(filename):
    """
    Checks whether a file is text POS-1 file format.
    """
    try:
        line = open(filename, 'r').readline()
    except:
        return False
    try:
        temp = line.split()
        if len(temp[0]) == 8 and len(temp[1]) == 5 and len(temp[2]) == 2:
            logging.debug("lib - format_autodif: Found Autodif Text file %s" % filename)
            return True
        else:
            return False
    except:
        return False


def readAUTODIF(filename, headonly=False, **kwargs):
    '''
    Reading AUTODIF format data.
    Looks like:
    48486304 00126 80 01.01.13 00:00:00,00
    48486309 00036 80 01.01.13 00:00:05,00
    48486314 00027 80 01.01.13 00:00:10,00
    '''

    # Reading AUTODIF text format data.
    starttime = kwargs.get('starttime')
    endtime = kwargs.get('endtime')
    getfile = True

    fh = open(filename, 'rb')
    # read file and split text into channels
    stream = DataStream()
    # Check whether header infromation is already present
    if stream.header is None:
        headers = {}
    else:
        headers = stream.header
    data = []
    key = None

    theday = extractDateFromString(filename)
    try:
        day = datetime.strftime(theday,"%Y-%m-%d")
        # Select only files within eventually defined time range
        if starttime:
            if not datetime.strptime(day,'%Y-%m-%d') >= datetime.strptime(datetime.strftime(stream._testtime(starttime),'%Y-%m-%d'),'%Y-%m-%d'):
                getfile = False
        if endtime:
            if not datetime.strptime(day,'%Y-%m-%d') <= datetime.strptime(datetime.strftime(stream._testtime(endtime),'%Y-%m-%d'),'%Y-%m-%d'):
                getfile = False
    except:
        logging.warning("Could not identify date in %s. Reading all ..." % daystring)
        getfile = True

    if getfile:

	line = fh.readline()

	while line != "":
            data = line.split()
            row = LineStruct()

            timestring = data[3] + ' ' + data[4]
            time = datetime.strptime(timestring, "%d.%m.%y %H:%M:%S,%f")

            row.time = date2num(time)
            row.f = float(data[0])/1000.
            row.df = float(data[1])/1000.
            row.var1 = float(data[2])

            stream.add(row)    

    	    line = fh.readline()

        #print "Finished file reading of %s" % filename

    fh.close()


    return DataStream(stream, headers)

def writeAUTODIF(datastream, filename, **kwargs):
    """
    Function to write AUTODIF-format data 
    """

    headdict = datastream.header

    myFile= open( filename, 'wb' )

    try:
        for elem in datastream:
            time = datetime.strftime(num2date(elem.time).replace(tzinfo=None), "%d.%m.%y %H:%M:%S,%f")

            if elem.var1 > 9 and elem.var1 < 90:
                line = '%08d %05d %02d %s\n' % (elem.f*1000., elem.df*1000., elem.var1, time[:20])
            else:
                line = '%08d %05d %02d %s\n' % (elem.f*1000., elem.df*1000., '80', time[:20])
            myFile.write(line)
    except:
        logging.warning('lib - format_autodif write: Data missing/wrong data format.')

    myFile.close()

