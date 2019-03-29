#include <iostream>
#include <stdexcept>
#include <string>
#include <QCoreApplication>
#include <QString>
#include <QtNetwork>

#define BUF_SIZE 1024
QUdpSocket socket;

void handleConnection()
{
    while (true) {
        if (socket.hasPendingDatagrams()) {
           QNetworkDatagram datagram = socket.receiveDatagram();
           QByteArray data(datagram.data(), BUF_SIZE);
           if (data.isNull()) {
               socket.close();
               std::cout << "No message" << std::endl;
               break;
           }
           std::cout << "Message: " << data.constData() << std::endl;
           socket.writeDatagram(datagram.makeReply(data));
        }
    }
    socket.close();
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        throw std::domain_error("Invalid number of arguments - expected port");
    }

    QCoreApplication a(argc, argv);

    bool portOk = true;
    quint16 port = QString(argv[1]).toUInt(&portOk);

    if (port <= 0 || !portOk) {
        throw std::domain_error("Invalid port");
    }

    QHostAddress ipAddr;
    ipAddr.setAddress("127.0.0.1");

    socket.bind(ipAddr, port);
    std::cout << "Listening on port " << port << " ..." << std::endl;

    QObject::connect(&socket, &QUdpSocket::readyRead, handleConnection);

    return a.exec();
}
