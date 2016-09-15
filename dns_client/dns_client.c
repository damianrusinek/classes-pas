#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <netdb.h>
#include <arpa/inet.h>

int main(int argc, char *argv[])
{
  struct hostent *h;
  if (argc != 2) { 
    fprintf(stderr,"usage: dns_client address\n");
    exit(1);
  }

  if ((h=gethostbyname(argv[1])) == NULL) { // pobierz informacje o hoscie
    herror("gethostbyname");
    exit(1);
  }
  printf("IP Address : %s\n", inet_ntoa(*((struct in_addr *)h->h_addr)));
  return 0;
}