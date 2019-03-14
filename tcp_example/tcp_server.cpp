#include <iostream>
#include <stdexcept>
#include <string>
#include <QCoreApplication>
#include <QString>
#include <QtNetwork>

#define BUF_SIZE 1024
QTcpServer server;

void handleConnection()
{
    QTcpSocket* socket = server.nextPendingConnection();

    if (!socket) {
        return;
    }

    std::cout << "Client connected " << socket->peerAddress().toString().toStdString() << std::endl;

    while (true) {
        socket->waitForReadyRead(-1);
        QByteArray data = socket->read(BUF_SIZE);
        if (data.isNull()) {
            socket->close();
            std::cout << "No message" << std::endl;
            break;
        }

        std::cout << "Message: " << data.constData() << std::endl;
        socket->write(data);
    }
    socket->close();
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

    server.setMaxPendingConnections(5);

    QHostAddress ipAddr;
    ipAddr.setAddress("127.0.0.1");

    std::cout << "Listening on port " << port << " ..." << std::endl;

    if(!server.listen(ipAddr, port)) {
        throw std::domain_error("Listening error");
    }

    QObject::connect(&server, &QTcpServer::newConnection, handleConnection);


    return a.exec();
}
