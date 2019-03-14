#include <iostream>
#include <stdexcept>
#include <string>
#include <QCoreApplication>
#include <QString>
#include <QtNetwork>

#define BUF_SIZE 1024

int main(int argc, char *argv[])
{
    if (argc != 3) {
        throw std::domain_error("Invalid number of arguments - expected ip address and port");
    }

    QCoreApplication a(argc, argv);

    QString ipAddr = argv[1];
    bool portOk = true;
    quint16 port = QString(argv[2]).toUInt(&portOk);

    if (port <= 0 || !portOk) {
        throw std::domain_error("Invalid port");
    }

    QUdpSocket socket;
    QHostAddress host;
    host.setAddress(ipAddr);

    std::string data;
    QByteArray data_srv;
    std::cout << "Leave empty line to quit" << std::endl;
    while(true) {
        std::cout << "Message to send: ";
        std::getline(std::cin, data);
        if (data == "") {
            break;
        }
        socket.writeDatagram(QString::fromStdString(data).toLatin1(), host, port);
        try {
           QNetworkDatagram datagram = socket.receiveDatagram();
           QByteArray data(datagram.data(), BUF_SIZE);
           if (data.isNull()) {
               break;
           }
           std::cout << "Answer: ";
           std::cout << data.constData() << std::endl;
        } catch (...) {
            std::cout << "Could not get any response";
        }
    }
    socket.close();
    std::cout << "Connection closed" << std::endl;


    return a.exec();
}
