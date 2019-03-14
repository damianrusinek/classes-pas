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

    QTcpSocket socket;
    socket.connectToHost(ipAddr, port);
    if(socket.waitForConnected() ) {
        std::cout << "Connected to " << ipAddr.toStdString() << " port " << port << std::endl;
    }

    std::string data;
    QByteArray data_srv;
    std::cout << "Leave empty line to quit" << std::endl;
    while(true) {
        if(socket.isWritable()) {
            std::cout << "Message to send: ";
            std::getline(std::cin, data);
            if (data == "") {
                break;
            }
            socket.write(QString::fromStdString(data).toLatin1());
        }

        socket.waitForReadyRead(-1);
        data_srv = socket.read(BUF_SIZE);
        if (data_srv == "") {
            break;
        }
        std::cout << "Answer: ";
        std::cout << data_srv.constData() << std::endl;
    }
    socket.close();
    std::cout << "Connection closed" << std::endl;


    return a.exec();
}
