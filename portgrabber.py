import optparse
import socket
import threading

hostname = raw_input("Enter hostname or IP : ")
portnumber = raw_input("Enter port portnumber: ")
lock = threading.Semaphore(value = 1)

# print dir(Semaphore)

def parseArguments():
    """
    Parse arguments on the command line.
    """

    global hostname, portnumber

    parser = optparse.OptionParser("Usage: %prog hostname -p portnumber\n\nPort list is comma-serated portnumber");
    parser.add_option('-p', dest = "portnumber");
    (options, arguments) = parser.parse_args();

    if options.portnumber != None:
        portnumber = options.portnumber
    if len(arguments) > 0:
        hostname =arguments[0]

    return

def checkport(resolvehost, port):
    """Check if the port is open
    """

    resultString = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    try:
        s.connect((resolvehost, port))
        result = True
    except:
        result = False
    if result:
        #port is open, try to get banner
        try:
            s.send("Hellp, word!\r\n")
            resultString = s.recv(100)
            resultString = resultString.split("\n, 2")[0].strip("\r")
        except:
            pass

    s.close()

    lock.acquire();
    if result:
        print "Port %5d/tcp is open. Response: '%s'" % (port, resultString)
    else:
        print "Port %5d/tcp is closed" % (port)
    lock.release()



def main():
    parseArguments()
    try:
        resolvehost = socket.gethostbyname(hostname)
    except:
        print "Host cannot be resolved"
        exit(1)
    for port in portnumber.split(','):
        port = int(port.strip())
        thread = threading.Thread(target=checkport, args=(resolvehost, port))
        thread.start()

main()
