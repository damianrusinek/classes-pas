using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;

namespace UdpServer
{
    class Program
    {
        private static readonly int BUFFER_SIZE = 1024;
        static void Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.Error.WriteLine("Usage: run program only with parameter <port>");
                Environment.Exit(1);
            }
            bool portIsValid = int.TryParse(args[0], out int port);
            if (!portIsValid || port <= 0)
            {
                Console.WriteLine("Invalid port number provided");
                Environment.Exit(1);
            }
            var endPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), port);
            using (var socket = new Socket(SocketType.Dgram, ProtocolType.IP))
            {
                socket.Bind(endPoint);
                while (true)
                {
                    var buffer = new byte[BUFFER_SIZE];
                    var ep = new IPEndPoint(IPAddress.Any, 0) as EndPoint;
                    int length = socket.ReceiveFrom(buffer, ref ep);
                    Console.WriteLine($"Received message from {ep}");
                    socket.SendTo(buffer, length, SocketFlags.None, ep);
                }
            }
        }
    }
}


