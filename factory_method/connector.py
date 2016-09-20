import abc
import urllib2
from BeautifulSoup import BeautifulStoneSoup

import port


class Connector(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, is_secure):
        self.is_secure = is_secure
        self.port = self.port_factory_method()
        self.protocol = self.protocol_factory_method()

    @abc.abstractmethod
    def parse(self):
        """Parses web content"""

    @abc.abstractmethod
    def protocol_factory_method(self):
        pass

    @abc.abstractmethod
    def port_factory_method(self):
        pass

    def read(self, host, path):
        url = self.protocol + '://' + host + ':' + str(self.port) + path
        print 'Connecting to ', url
        return urllib2.urlopen(url, timeout=2).read()


class HTTPConnector(Connector):

    def protocol_factory_method(self):
        if self.is_secure:
            return 'https'
        return 'http'

    def port_factory_method(self):
        if self.is_secure:
            return port.HTTPSecurePort()
        return port.HTTPPort()

    def parse(self, content):
        filenames = []
        soup = BeautifulStoneSoup(content)
        links = soup.table.findAll('a')
        for link in links:
            filenames.append(link['href'])
        return '\n'.join(filenames)


class FTPConnector(Connector):

    def protocol_factory_method(self):
        return 'ftp'

    def port_factory_method(self):
        return port.FTPPort()

    def parse(self, content):
        lines = content.split('\n')
        filenames = []

        for line in lines:
            split_lines = line.split(None, 8)

            if len(split_lines) == 9:
                filenames.append(split_lines[-1])

        return '\n'.join(filenames)
