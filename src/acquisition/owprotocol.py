
# OneWire part
try:
    import ow
    onewire = True
    owsensorlist = []
except:
    print "Onewire package not available"
    onewire = False  

import sys, time, os, socket
import struct, binascii, re
from datetime import datetime, timedelta

from twisted.protocols.basic import LineReceiver
from autobahn.wamp import exportRpc

from twisted.internet import reactor

from twisted.python import usage, log
from twisted.internet.serialport import SerialPort
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import listenWS
from autobahn.wamp import WampServerFactory, WampServerProtocol, exportRpc

if onewire:
    class OwProtocol():
        """
        Protocol to read one wire data from usb DS unit 
        All connected sensors are listed and data is distributed in dependency of sensor id
        Dipatch url links are defined by channel 'ow' and id+'value'
        Save path ? folders ?

        """
        def __init__(self, wsMcuFactory, outputdir):
            self.wsMcuFactory = wsMcuFactory
            #self.sensor = 'ow'
            ow.init("u")
            self.root = ow.Sensor('/').sensorList()
            self.hostname = socket.gethostname()
            self.outputdir = outputdir
            self.reconnectcount = 0

        def owConnected(self):
            global owsensorlist
            try:
                self.root = ow.Sensor('/').sensorList()

                if not (self.root == owsensorlist):
                    log.msg('Rereading sensor list')                
                    ow.init("u")
                    self.root = ow.Sensor('/').sensorList()
                    owsensorlist = self.root
                    self.connectionMade(self.root)
                self.reconnectcount = 0 
            except:
                self.reconnectcount = self.reconnectcount + 1
                log.msg('Reconnection event triggered - Number: %d' % self.reconnectcount)                
                time.sleep(2)
                if self.reconnectcount < 10:
                    self.owConnected()
                else:
                    print "owConnect: reconnection not possible"

            self.oneWireInstruments(self.root)


        def connectionMade(self,root):
            log.msg('One Wire module initialized - found the following sensors:')
            for sensor in root:
                # Use this list to initialize the sensor database including datalogger id and type
                log.msg('Type: %s, ID: %s' % (sensor.type, sensor.id))

        def oneWireInstruments(self,root):
            for sensor in root:
                if sensor.type == 'DS18B20':             
                    #sensor.useCache( False ) # Important for below 15 sec resolution (by default a 15 sec cache is used))
                    self.readTemperature(sensor)
                #if sensor.type == 'DS2406':
                #    self.readSHT(sensor)
                elif sensor.type == 'DS2438':
                    #sensor.useCache( False ) # Important for below 15 sec resolution (by default a 15 sec cache is used))
                    self.readBattery(sensor)

        def alias(self, sensorid):
            #define a alias dictionary
            sensordict = {"332988040000": "Mobil", "504C88040000": "1. Stock: Treppenhaus", 
                          "6C2988040000": "1. Stock: Flur", "FD9087040000": "Nordmauer Erdgeschoss", 
                          "090A88040000": "1. Stock: Wohnzimmer", "BB5388040000": "1. Stock: Kueche",
                          "F58788040000": "1. Stock: Schlafzimmer", "BAAE87040000": "Dach: Nico (T)",
                          "E2FE87040000": "1. Stock: Speis",
                          "BED887040000": "Dach: Flur", "2F3488040000": "1. Stock: Bad (T)", "0EB354010000": "Dach: Nico",
                          "3AD754010000": "Dach: Tina", "CBC454010000": "1. Stock: Kinderzimmer",
                          "05CE54010000": "1. Stock: Bad"}      
            try:
                return sensordict[sensorid]
            except:
                return sensorid

        def timeToArray(self, timestring):
            # Converts time string of format 2013-12-12T23:12:23.122324
            # to an array similiat to a datetime object
            try:
                splittedfull = timestring.split(' ')
                splittedday = splittedfull[0].split('-')
                splittedsec = splittedfull[1].split('.')
                splittedtime = splittedsec[0].split(':')
                datearray = splittedday + splittedtime
                datearray.append(splittedsec[1])
                datearray = map(int,datearray)
                return datearray
            except:
                log.msg('Error while extracting time array')
                return []

        def dataToFile(self, sensorid, filedate, bindata, header):
            # File Operations
            try:
                path = os.path.join(self.outputdir,self.hostname,sensorid)
                if not os.path.exists(path):
                    os.makedirs(path)
                savefile = os.path.join(path, sensorid+'_'+filedate+".bin")
                if not os.path.isfile(savefile):
                    with open(savefile, "wb") as myfile:
                        myfile.write(header + "\n")
                        myfile.write(bindata + "\n")
                else:
                    with open(savefile, "a") as myfile:
                        myfile.write(bindata + "\n")
            except:
                log.err("OW - Protocol: Error while saving file")        
            
        def readTemperature(self, sensor):

            #t = threading.Timer(1.0, self.readTemperature, [sensor])
            #t.deamon = True
            #t.start()
            dispatch_url =  "http://example.com/"+self.hostname+"/ow#"+sensor.id+"-value"
            currenttime = datetime.utcnow()
            filename = datetime.strftime(currenttime, "%Y-%m-%d")
            actualtime = datetime.strftime(currenttime, "%Y-%m-%dT%H:%M:%S.%f")
            timestamp = datetime.strftime(currenttime, "%Y-%m-%d %H:%M:%S.%f")
            outtime = datetime.strftime(currenttime, "%H:%M:%S")
            #header = "# MagPyBin, sensor_id, [parameterlist], [unit-conversion-list], packing string, length"
            packcode = '6hLL'
            header = "# MagPyBin %s %s %s %s %s %s %d" % (sensor.id, '[t1]', '[T]', '[degC]', '[1000]', packcode, struct.calcsize(packcode))

            try:
                # Extract data
                temp = float(sensor.temperature)

                # extract time data
                datearray = self.timeToArray(timestamp)
                try:
                    datearray.append(int(temp*1000))
                    #data_bin = struct.pack(packcode,datearray[0],datearray[1],datearray[2],datearray[3],datearray[4],datearray[5],datearray[6],datearray[7])
                    data_bin = struct.pack(packcode,*datearray)
                except:
                    log.msg('Error while packing binary data')
                    pass

                # File Operations
                self.dataToFile(sensor.id, filename, data_bin, header)

                # Provide data to websocket
                evt1 = {'id': 0, 'value': outtime}
                evt6 = {'id': 8, 'value': timestamp}
                evt2 = {'id': 5, 'value': temp}
                evt5 = {'id': 10, 'value': self.hostname}
                evt8 = {'id': 99, 'value': 'eol'}

                try:
                    self.wsMcuFactory.dispatch(dispatch_url, evt1)
                    self.wsMcuFactory.dispatch(dispatch_url, evt6)
                    self.wsMcuFactory.dispatch(dispatch_url, evt2)
                    self.wsMcuFactory.dispatch(dispatch_url, evt5)
                    self.wsMcuFactory.dispatch(dispatch_url, evt8)
                    pass
                except ValueError:
                    log.err('Unable to parse data at %s' % actualtime)
            except:
                log.err('Lost temperature sensor -- reconnecting')
                self.owConnected()
                

        def readBattery(self,sensor):
            dispatch_url =  "http://example.com/"+self.hostname+"/ow#"+sensor.id+"-value"
            currenttime = datetime.utcnow()
            filename = datetime.strftime(currenttime, "%Y-%m-%d")
            actualtime = datetime.strftime(currenttime, "%Y-%m-%dT%H:%M:%S.%f")
            timestamp = datetime.strftime(currenttime, "%Y-%m-%d %H:%M:%S.%f")
            outtime = datetime.strftime(currenttime, "%H:%M:%S")
            packcode = '6hLLLLLf'
            header = "# MagPyBin %s %s %s %s %s %s %d" % (sensor.id, '[t1,var1,var2,var3,var4]', '[T,rh,vdd,vad,vis]', '[deg_C,per,V,V,V]', '[1000,100,100,100,1]', packcode, struct.calcsize(packcode))

            try:
                # Extract data
                try:
                    humidity = float(ow.owfs_get('/uncached%s/HIH4000/humidity' % sensor._path))
                except:
                    humidity = float(nan)
                temp = float(sensor.temperature)
                vdd = float(sensor.VDD)
                vad = float(sensor.VAD)
                vis = float(sensor.vis)

                # Appending data to buffer which contains pcdate, pctime and sensordata
                # extract time data
                datearray = self.timeToArray(timestamp)

                try:
                    datearray.append(int(temp*1000))
                    datearray.append(int(humidity*100))
                    datearray.append(int(vdd*100))
                    datearray.append(int(vad*100))
                    datearray.append(vis)
                    #data_bin = struct.pack(packcode,datearray[0],datearray[1],datearray[2],datearray[3],datearray[4],datearray[5],datearray[6],datearray[7],datearray[8],datearray[9],datearray[10],datearray[11])
                    data_bin = struct.pack(packcode,*datearray)
                except:
                    log.msg('Error while packing binary data')
                    pass

                # File Operations
                self.dataToFile(sensor.id, filename, data_bin, header)

                evt1 = {'id': 0, 'value': outtime}
                evt9 = {'id': 8, 'value': timestamp}
                evt2 = {'id': 5, 'value': temp}
                if humidity < 100:
                    evt3 = {'id': 7, 'value': humidity}
                else:
                    evt3 = {'id': 7, 'value': 0}
                evt4 = {'id': 11, 'value': self.alias(sensor.id)}
                evt5 = {'id': 12, 'value': vdd}
                evt6 = {'id': 13, 'value': vad}
                evt7 = {'id': 14, 'value': vis}
                evt8 = {'id': 99, 'value': 'eol'}

                try:
                    self.wsMcuFactory.dispatch(dispatch_url, evt1)
                    self.wsMcuFactory.dispatch(dispatch_url, evt9)
                    self.wsMcuFactory.dispatch(dispatch_url, evt2)
                    self.wsMcuFactory.dispatch(dispatch_url, evt3)
                    self.wsMcuFactory.dispatch(dispatch_url, evt4)
                    self.wsMcuFactory.dispatch(dispatch_url, evt5)
                    self.wsMcuFactory.dispatch(dispatch_url, evt6)
                    self.wsMcuFactory.dispatch(dispatch_url, evt7)
                    self.wsMcuFactory.dispatch(dispatch_url, evt8)
                    pass
                except ValueError:
                    log.err('Unable to parse data at %s' % actualtime)
            except:
                log.err('Lost battery sensor -- reconnecting')
                self.owConnected()