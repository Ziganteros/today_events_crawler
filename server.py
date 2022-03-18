from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from spider import crawler, today_date


class Server(Protocol):
    def connectionMade(self):
        print("New Connection")
        self.transport.write(f"Nel giorno {today_date().replace('_',' ')} sono avvenuti i seguenti fatti: \n\n".encode('utf-8'))
        eventi = crawler()
        self.transport.write(f"{eventi}".encode('utf-8'))
    
    def dataReceived(self, data):
        self.transport.write(data)


class ServerFactory(ServFactory):
    def buildProtocol(self, addr):
        return Server()

if __name__== '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 2000)
    endpoint.listen(ServerFactory())
    reactor.run()


# print('ok, provo a stampare la server response')
# try:
    # print('ecco la server response:')
    # print(server_response)
# except:
    # print('non riesco a vedere la server response')
