import os

from zope.interface import Interface, implements

from twisted.application import service
from twisted.internet import reactor
from twisted.internet import endpoints

from anion import messaging
from anion import entity

import osx_driver

class ISay(Interface):

    def say(phrase):
        """
        """


class IVolume(Interface):

    def get_volume():
        """
        """

    def set_volume(value):
        """
        """


class Demo(service.Service):

    implements(ISay, IVolume)

    def __init__(self):
        self._volume = osx_driver.Volume()

    def say(self, phrase):
        osx_driver.say(phrase)

    def get_volume(self):
        return self._volume.get_volume()

    def set_volume(self, value):
        self._volume.set_volume(value)

def clientFactory(name):
    node = messaging.Node()
    client = entity.RPCClientEntityFromInterface(name, ISay)
    node.addEntity('foo', client, messaging.NChannel)
    local_endpoint = endpoints.TCP4ClientEndpoint(reactor, 'localhost', 'amqp')
    local_endpoint.connect(node)
    return client

def make_name():
    login = os.getlogin()
    nodename = os.uname()[1]
    return 'osx' + login

def main():
    """
    make the name of the say server a startup parameter
    """
    node = messaging.Node()

    demo = Demo()

    e = entity.RPCEntityFromService(demo)
    node.addEntity(make_name(), e, messaging.RPCChannel)
    #node.addServer((exchange, key), entity, ChannelType)

    localendpoint = endpoints.TCP4ClientEndpoint(reactor, 'localhost', 'amqp')
    localendpoint.connect(node)


if __name__ == '__main__':
    main()
    reactor.run()


