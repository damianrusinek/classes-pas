using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using static System.Text.Encoding;

namespace SocketChatServer
{
    class Program
    {
        private static readonly int BUFFER_SIZE = 1024;
        static void Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.Error.WriteLine("Usage: run program only with parameter (port)");
                Environment.Exit(1);
            }

            bool portIsValid = int.TryParse(args[0], out int port);
            if (!portIsValid || port <= 0)
            {
                Console.Error.WriteLine("Invalid port number provided");
                Environment.Exit(1);
            }
            var endPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), port);
            using (var socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp))
            {
                socket.Bind(endPoint);
                socket.Listen(5);
                while (true)
                {
                    Console.WriteLine($"Listening on {endPoint.Address}:{endPoint.Port} ...");
                    using (var connection = socket.Accept())
                    {
                        Console.WriteLine("someone connected");
                        Console.WriteLine("receive and send message, empty line closes connection");
                        while (true)
                        {
                            var buffer = new byte[BUFFER_SIZE];
                            int dataSize = connection.Receive(buffer);
                            var message = ASCII.GetString(buffer
                                .Take(dataSize)
                                .ToArray());
                            if (string.IsNullOrWhiteSpace(message)) { break; }
                            Console.WriteLine($"Message:{message}");

                            Console.Write("Type in your response:");
                            var responseMsg = Console.ReadLine();
                            if (string.IsNullOrWhiteSpace(responseMsg)) { break; }
                            var response = ASCII.GetBytes(responseMsg);
                            connection.Send(response);
                        }
                    }
                }
            }
        }
    }
}
