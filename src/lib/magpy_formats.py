'''
Path:			magpy.lib.magpy_formats
Part of package:	stream (read/write)
Type:			Input tester, call to read library

PURPOSE:
	Tests which format a file has using the read library.

CONTAINS:
        isFormat:	(Func) Runs through datatypes in library to find fitting type.
	readFormat:	(Func) When format is found, reads data file into DataStream.
	writeFormat:	(Func) Writes DataStream object to given format.

DEPENDENCIES:
	magpy.lib...
		.format_gsm19
		.format_didd
		.format_gdas
		.format_lemi
		.format_pos1
		.format_env05
		.format_cr800
		.format_iaga02
		.format_wdc
		.format_magpy
		.format_noaa
		.format_latex
		.format_wik
		.format_wic
		.format_sfs
		.format_bdv
		.format_dtu
		.format_gfz
		.format_imf

CALLED BY:
	magpy.stream.read()
	magpy.stream.write()
'''

from stream import *

# IMPORT INSTRUMENT SPECIFIC DATA FORMATS:
from lib.format_gsm19 import *
from lib.format_didd import *
from lib.format_gdas import *
from lib.format_lemi import *
from lib.format_pos1 import *
from lib.format_env05 import *
from lib.format_cr800 import *

# IMPORT GENERAL PURPOSE FORMATS:
from lib.format_iaga02 import *
from lib.format_wdc import *
from lib.format_magpy import *
from lib.format_noaa import *
from lib.format_latex import *

# IMPORT OBSERVATORY/GROUP SPECIFIC FORMATS:
from lib.format_wik import *
from lib.format_wic import *
from lib.format_sfs import *
from lib.format_bdv import *
from lib.format_dtu import *
from lib.format_gfz import *

from lib.format_imf import *
try:
    from lib.format_autodif_fread import *
except:
    logging.warning("magpy-formats: Format package autodif-F not available")


def isFormat(filename, format_type):
    if (format_type == "IAGA"):
        if (isIAGA(filename)):
            return True
    elif (format_type == "WDC"):
        if (isWDC(filename)):
            return True
    elif (format_type == "DIDD"):
        if (isDIDD(filename)):
            return True
    elif (format_type == "OPT"):
        if (isOPT(filename)):
            return True
    elif (format_type == "PMAG1"): # Data from the ELSEC820 System 
        if (isPMAG1(filename)):
            return True
    elif (format_type == "PMAG2"): # Data from the ELSEC820 System via Cobenzl RCS
        if (isPMAG2(filename)):
            return True
    elif (format_type == "GDASA1"): # Data from the Conrad Observatory GDAS System
        if (isGDASA1(filename)):
            return True
    elif (format_type == "GDASB1"): # Data from the Conrad Observatory GDAS System
        if (isGDASB1(filename)):
            return True
    elif (format_type == "DTU1"): # ASCII Data from the DTU's FGE systems
        if (isDTU1(filename)):
            return True
    elif (format_type == "PYSTR"):
        if (isPYSTR(filename)):
            return True
    elif (format_type == "PYCDF"):
        if (isPYCDF(filename)):
            return True
    elif (format_type == "PYBIN"):
        if (isPYBIN(filename)):
            return True
    elif (format_type == "RMRCS"): # Data from the Conrad Observatory RCS System
        if (isRMRCS(filename)):
            return True
    elif (format_type == "METEO"): # Conrad Observatory RCS System - METEO files
        if (isMETEO(filename)):
            return True
    elif (format_type == "GRAVSG"): # Data from the Conrad Observatory SG gravity system
        if (isGRAVSG(filename)):
            return True
    elif (format_type == "IWT"): # Data from the Conrad Observatory tiltmeter system
        if (isIWT(filename)):
            return True
    elif (format_type == "LIPPGRAV"): # Data from the Lippmann tiltmeter system
        if (isLIPPGRAV(filename)):
            return True
    elif (format_type == "CR800"): # Data from the CR800 datalogger
        if (isCR800(filename)):
            return True
    elif (format_type == "RADON"): # Data from the CR800 datalogger
        if (isRADON(filename)):
            return True
    elif (format_type == "USBLOG"): # Data from the USB temperature logger
        if (isUSBLOG(filename)):
            return True
    elif (format_type == "CS"):
        if (isCS(filename)):
            return True
    elif (format_type == "GSM19"): # Data from the GEM GSM 19 Overhauzer sensor
        if (isGSM19(filename)):
            return True
    elif (format_type == "LEMIHF"): # High frequency Lemi data (10 Hz)
        if (isLEMIHF(filename)):
            return True
    elif (format_type == "LEMIBIN"): # Binary Lemi data (10 Hz)
        if (isLEMIBIN(filename)):
            return True
    elif (format_type == "LEMIBIN1"): # Binary Lemi data (10 Hz)
        if (isLEMIBIN1(filename)):
            return True
    elif (format_type == "POS1"): # Binary POS1 data (0.2 Hz)
        if (isPOS1(filename)):
            return True
    elif (format_type == "POS1TXT"): # Text POS1 data (0.2 Hz)
        if (isPOS1TXT(filename)):
            return True
    elif (format_type == "IMF"): # Intermagnet v1.22,v1.23 data (60 sec)
        try:
            if (isIMF(filename)):
                return True
        except:
            pass
    elif (format_type == "BLV"): # Intermagnet IBFV2.00
        try:
            if (isBLV(filename)):
                return True
        except:
            pass
    elif (format_type == "AUTODIF_FREAD"): # Text AUTODIF F for baseline (0.2 Hz, from POS1)
        try:
            if (isAUTODIF_FREAD(filename)):
                return True
        except:
            pass
    elif (format_type == "ENV05"): # Binary Environmental data (1 Hz)
        if (isENV05(filename)):
            return True
    elif (format_type == "SFDMI"): # San Fernando DMI(FGE) format
        if (isSFDMI(filename)):
            return True
    elif (format_type == "SFGSM"): # San Fernando GSM format
        if (isSFGSM(filename)):
            return True
    elif (format_type == "BDV1"): # Budkov format
        if (isBDV1(filename)):
            return True
    elif (format_type == "GFZKP"): # GFZ Kp
        if (isGFZKP(filename)):
            return True
    elif (format_type == "NOAAACE"): # NOAA Satellite date
        if (isNOAAACE(filename)):
            return True
    else:
        return False


def readFormat(filename, format_type, headonly=False, **kwargs):
    empty = DataStream()
    if (format_type == "IAGA"):
        return readIAGA(filename, headonly, **kwargs)
    elif (format_type == "WDC"):
        return readWDC(filename, headonly, **kwargs)
    elif (format_type == "IMF"):
        return readIMF(filename, headonly, **kwargs)
    elif (format_type == "BLV"): # Intermagnet IBFV2.00
        return readBLV(filename, headonly, **kwargs)
    elif (format_type == "DIDD"):
        return readDIDD(filename, headonly, **kwargs)
    elif (format_type == "GDASA1"):
        return readGDASA1(filename, headonly, **kwargs)
    elif (format_type == "GDASB1"):
        return readGDASB1(filename, headonly, **kwargs)
    elif (format_type == "RMRCS"):
        return readRMRCS(filename, headonly, **kwargs)
    elif (format_type == "METEO"):
        return readMETEO(filename, headonly, **kwargs)
    elif (format_type == "PYSTR"):
        return readPYSTR(filename, headonly, **kwargs)
    elif (format_type == "PYCDF"):
        return readPYCDF(filename, headonly, **kwargs)
    elif (format_type == "PYBIN"):
        return readPYBIN(filename, headonly, **kwargs)
    elif (format_type == "GSM19"):
        return readGSM19(filename, headonly, **kwargs)
    elif (format_type == "LEMIHF"):
        return readLEMIHF(filename, headonly, **kwargs)
    elif (format_type == "LEMIBIN"):
        return readLEMIBIN(filename, headonly, **kwargs)
    elif (format_type == "LEMIBIN1"):
        return readLEMIBIN1(filename, headonly, **kwargs)
    elif (format_type == "POS1"):
        return readPOS1(filename, headonly, **kwargs)
    elif (format_type == "POS1TXT"):
        return readPOS1TXT(filename, headonly, **kwargs)
    elif (format_type == "AUTODIF_FREAD"):
        return readAUTODIF_FREAD(filename, headonly, **kwargs)
    elif (format_type == "ENV05"):
        return readENV05(filename, headonly, **kwargs)
    elif (format_type == "USBLOG"):
        return readUSBLOG(filename, headonly, **kwargs)
    elif (format_type == "GRAVSG"):
        return readGRAVSG(filename, headonly, **kwargs)
    elif (format_type == "IWT"):
        return readIWT(filename, headonly, **kwargs)
    elif (format_type == "LIPPGRAV"):
        return readLIPPGRAV(filename, headonly, **kwargs)
    elif (format_type == "CR800"):
        return readCR800(filename, headonly, **kwargs)
    elif (format_type == "RADON"):
        return readRADON(filename, headonly, **kwargs)
    elif (format_type == "CS"):
        return readCS(filename, headonly, **kwargs)
    # Observatory specific
    elif (format_type == "OPT"):
        return readOPT(filename, headonly, **kwargs)
    elif (format_type == "PMAG1"):
        return readPMAG1(filename, headonly, **kwargs)
    elif (format_type == "PMAG2"):
        return readPMAG2(filename, headonly, **kwargs)
    elif (format_type == "DTU1"):
        return readDTU1(filename, headonly, **kwargs)
    elif (format_type == "SFDMI"):
        return readSFDMI(filename, headonly, **kwargs)
    elif (format_type == "SFGSM"):
        return readSFGSM(filename, headonly, **kwargs)
    elif (format_type == "BDV1"):
        return readBDV1(filename, headonly, **kwargs)
    elif (format_type == "GFZKP"):
        return readGFZKP(filename, headonly, **kwargs)
    elif (format_type == "NOAAACE"):
        return readNOAAACE(filename, headonly, **kwargs)
    else:
        return DataStream(empty,empty.header)


def writeFormat(datastream, filename, format_type, **kwargs):
    """
    calls the format specific write functions
    if the selceted dir is not existing, it is created
    """
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(os.path.normpath(directory))
    if (format_type == "IAGA"):
        return writeIAGA(datastream, filename, **kwargs)
    elif (format_type == "WDC"):
        return writeWDC(datastream, filename, **kwargs)
    elif (format_type == "IMF"):
        return writeIMF(datastream, filename, **kwargs)
    elif (format_type == "BLV"):
        return writeBLV(datastream, filename, **kwargs)
    elif (format_type == "DIDD"):
        return writeDIDD(datastream, filename, **kwargs)
    elif (format_type == "PMAG1"):
        return writePMAG1(datastream, filename, **kwargs)
    elif (format_type == "PMAG2"):
        return writePMAG2(datastream, filename, **kwargs)
    elif (format_type == "DTU1"):
        return writeDTU1(datastream, filename, **kwargs)
    elif (format_type == "GDASA1"):
        return writeGDASA1(datastream, filename, **kwargs)
    elif (format_type == "RMRCS"):
        return writeRMRCS(datastream, filename, **kwargs)
    elif (format_type == "PYSTR"):
        return writePYSTR(datastream, filename, **kwargs)
    elif (format_type == "PYASCII"):
        return writePYASCII(datastream, filename, **kwargs)
    elif (format_type == "PYCDF"):
        return writePYCDF(datastream, filename, **kwargs)
    elif (format_type == "AUTODIF_FREAD"):
        return writeAUTODIF_FREAD(datastream, filename, **kwargs)
    elif (format_type == "USBLOG"):
        return writeUSBLOG(datastream, filename, **kwargs)
    elif (format_type == "CR800"):
        return writeCR800(datastream, filename, **kwargs)
    elif (format_type == "LATEX"):
        return writeLATEX(datastream, filename, **kwargs)
    else:
        logging.warning("magpy-formats: Writing not succesful - format not recognized")



