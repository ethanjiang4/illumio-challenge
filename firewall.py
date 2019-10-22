class Intervals:
    # A data structure that holds a list of [portRange, ipRange]
    # or a dict of [port, ip/ipRange]
    def __init__(self):
        self.intervals = []
        self.singles = {}

    def ipLTOrEq(self, ip1, ip2):
        # Return if ip1 <= ip2
        if ip1 == ip2:
            return True
        ip1List = [int(x) for x in ip1.split('.')]
        ip2List = [int(x) for x in ip2.split('.')]
        for i in range(len(ip1List)):
            if ip1List[i] > ip2List[i]:
                return False
            elif ip1List[i] < ip2List[i]:
                return True
        return True
    
    def insert(self, portRange, ipRange):
        portRange = [int(port) for port in portRange]
        # If single port, add it to singles
        if len(portRange) == 1:
            self.singles[portRange[0]] = ipRange
        else:
            # Else add the interval to intervals
            if len(ipRange) == 1:
                ipRange.append(ipRange[0])
            newInterval = [portRange, ipRange]
            self.intervals.append(newInterval)
    
    def search(self, port, ip):
        # Check singles
        if port in self.singles:
            if len(self.singles[port]) == 1 and self.singles[port][0] == ip:
                return True
            elif self.ipLTOrEq(self.singles[port][0], ip) and self.ipLTOrEq(ip, self.singles[port][1]):
                return True
        # Iterate through and search intervals
        # Note item[0] is the portRange and item[1] is the ipRange
        for item in self.intervals:
            if item[0][0] <= port <= item[0][1]:
                if self.ipLTOrEq(item[1][0], ip) and self.ipLTOrEq(ip, item[1][1]):
                    return True
        return False

class Firewall:
    def __init__(self, path):
        self.path = path
        # Dict of tuples representing the 4 possible combos of direction / protocol
        self.directionsProtocols = {}
        self.data = open(path, mode='r')
        for line in self.data:
            # Remove '/n', remove quotation marks, split by comma for .csv
            line = line.rstrip()
            line = line[1:len(line)-1]
            line = line.split(',')
            primaryInfo = (line[0], line[1]) # Direction and protocol
            if not primaryInfo in self.directionsProtocols:
                # Add to dict
                self.directionsProtocols[primaryInfo] = Intervals()
            
            # Generate port and ip ranges and add them to the structures
            port = line[2].split('-')
            portRange = [int(x) for x in port]
            ipRange = line[3].split('-')
            self.directionsProtocols[primaryInfo].insert(portRange, ipRange)

    def accept_packet(self, dir, proto, port, ip):
        primaryInfo = (dir, proto)
        if primaryInfo in self.directionsProtocols:
            # Run search on the ranges
            search = self.directionsProtocols[primaryInfo].search(port, ip)
            return search
        else:
            return False

# TESTING
# fw = Firewall('data.csv')
# Test ports and port ranges
# print(fw.accept_packet('outbound', 'tcp', 9999, '192.168.10.11')) #False
# print(fw.accept_packet('outbound', 'tcp', 2, '0.0.0.1')) #False
# print(fw.accept_packet('inbound', 'tcp', 65535, '0.0.0.0')) #False
# print(fw.accept_packet('outbound', 'tcp', 12345, '192.168.10.11')) #True
# print(fw.accept_packet('inbound', 'udp', 53, '192.168.1.1')) #True
# print(fw.accept_packet('outbound', 'tcp', 1, '0.0.0.1')) #True
# Test ips and ip ranges
# print(fw.accept_packet('inbound', 'udp', 1, '255.255.255.255')) #False
# print(fw.accept_packet('inbound', 'udp', 53, '192.168.1.0')) #False
# print(fw.accept_packet('inbound', 'tcp', 65535, '0.0.1.0')) #False
# print(fw.accept_packet('outbound', 'udp', 12345, '255.255.255.255')) #True
# print(fw.accept_packet('inbound', 'udp', 53, '192.168.2.0')) #True
# print(fw.accept_packet('outbound', 'udp', 1999, '52.12.48.92')) #True
