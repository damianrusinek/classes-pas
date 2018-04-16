using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace TcpServer
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
            using (var socket = new Socket(SocketType.Stream, ProtocolType.Tcp))
            {
                socket.Bind(endPoint);
                socket.Listen(10);
                Console.WriteLine($"Listening on {endPoint.Address}:{endPoint.Port} ...");
                while (true)
                {
                    using (var connection = socket.Accept())
                    {
                        Console.WriteLine("Client connected");
                        while (true)
                        {
                            var buffer = new byte[BUFFER_SIZE];
                            int length = 0;
                            try
                            {
                                length = connection.Receive(buffer);
                            }
                            catch (Exception e)
                            {
                                break;
                            }
                            if (length == 0) { break; }
                            connection.Send(buffer
                                .Take(length)
                                .ToArray());
                        }
                        Console.WriteLine("Client disconnected");
                    }
                }
            }
        }
    }
}
