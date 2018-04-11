using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using static System.Text.Encoding;

namespace UdpClient
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
            var endPoint = new IPEndPoint(_address, port) as EndPoint;
            using (var socket = new Socket(SocketType.Dgram, ProtocolType.IP))
            {
                Console.WriteLine("Example udp client. Empty line exits");
                socket.Blocking = false;
                while (true)
                {
                    Console.Write("Enter your message:");
                    var message = Console.ReadLine();
                    if (string.IsNullOrWhiteSpace(message)) { break; }
                    var data = ASCII.GetBytes(message);
                    socket.SendTo(data, endPoint);
                    var buffer = new byte[BUFFER_SIZE];
                    int dataSize = 0;
                    try
                    {
                        dataSize = socket.ReceiveFrom(buffer, ref endPoint);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("Couldn't get response from server");
                        continue;
                    }
                    var responseMsg = ASCII.GetString(buffer, 0, dataSize);
                    if (string.IsNullOrWhiteSpace(responseMsg)) { break; }
                    Console.WriteLine($"Response: {responseMsg}");
                }
            }
        }
    }
}