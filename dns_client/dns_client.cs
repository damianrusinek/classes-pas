using System;
using System.Linq;
using System.Net;
using static System.Net.Dns;

namespace DnsClient
{
    class Program
    {
        static void Main(string[] args)
        {
            // c# 7.0 tinkering, use this version of input error handling if you want
            if (args.Length != 1)
            {
                Console.Error.WriteLine("Usage: run with parameter <host-name>");
                Environment.Exit(1);
            }
            var hostname = args[0];
            try
            {
                IPHostEntry entry = GetHostEntry(hostname); //GetHostByName method is obsolete
                var ip = entry.AddressList.FirstOrDefault();
                Console.WriteLine($"Resolved IP address: {ip}");
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }
    }
}
