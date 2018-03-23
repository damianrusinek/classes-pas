using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using static System.Text.Encoding;

namespace SocketChatClient
{
    class Program
    {
        private static readonly int BUFFER_SIZE = 1024;
        private static IPAddress _address;
        static void Main(string[] args)
        {
            if (args.Length != 2)
            {
                Console.Error.WriteLine("Usage: run program only with parameters <ip> <port>");
                Environment.Exit(1);
            }

            try
            {
                _address = IPAddress.Parse(args[0]);
            }
            catch (Exception e)
            {
                Console.Error.WriteLine("Invalid IP address");
                Environment.Exit(1);
            }
            bool portIsValid = int.TryParse(args[1], out int port);
            if (!portIsValid || port <= 0)
            {
                Console.WriteLine("Invalid port number provided");
                Environment.Exit(1);
            }
            var endPoint = new IPEndPoint(_address, port);
            using (var socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp))
            {
                try
                {
                    socket.Connect(endPoint);
                }
                catch (Exception e)
                {
                    Console.Error.WriteLine($"Couldn't connect to {endPoint.Address}:{endPoint.Port}");
                    Environment.Exit(1);
                }
                Console.WriteLine("Enter message to send, enter whitespace to exit");
                while (true)
                {
                    Console.Write("Enter your message: ");
                    var message = Console.ReadLine();
                    if (string.IsNullOrWhiteSpace(message)) { break; }
                    var data = ASCII.GetBytes(message);
                    socket.Send(data);
                    Console.WriteLine("Message Sent.");

                    var buffer = new byte[BUFFER_SIZE];
                    int dataSize = socket.Receive(buffer);
                    var responseMsg = ASCII.GetString(buffer
                        .Take(dataSize)
                        .ToArray());
                    if (string.IsNullOrWhiteSpace(responseMsg)) { break; }
                    Console.WriteLine($"Message received: {responseMsg}");
                }
            }
        }
    }
}
