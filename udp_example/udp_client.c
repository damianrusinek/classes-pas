#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char * argv[]) {
  int BUF_SIZE = 1024;
  char * ip_addr;
  int port;
  int sockfd;
  struct sockaddr_in server_addr;
  int recv_size, read_size, sent_size;
  char buffer[BUF_SIZE+1];

  if (argc != 3) { 
    fprintf(stderr,"usage: udp_client ip port\n");
    exit(1);
  }
  ip_addr = argv[1];
  port = atoi(argv[2]);
  if (port <= 0) {
    fprintf(stderr,"error: invalid port\n");
    exit(1);
  }
  if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
    perror("socket");
    exit(1);
  }

  server_addr.sin_family = AF_INET;
  server_addr.sin_port = htons(port);
  inet_aton(ip_addr, &server_addr.sin_addr);

  while(1) { 
    printf("Data to send (Ctrl+D quits): ");
    if (fgets(buffer, BUF_SIZE, stdin) == NULL) {
      close(sockfd);
      perror("fgets");  
      exit(1);
    }
    read_size = strlen(buffer);

    if ((sent_size = sendto(sockfd, buffer, read_size, 0, (struct sockaddr *)&server_addr, sizeof(struct sockaddr))) == -1) {
      close(sockfd);
      perror("sendto");
      exit(1);
    }

    if ((recv_size = recvfrom(sockfd, buffer, BUF_SIZE, 0, NULL, NULL)) == 0) {
      close(sockfd);
      if (errno != 0) {
        perror("recv");
        exit(1);
      }
      break;
    }

    buffer[recv_size] = '\0';
    printf("Answer: %s", buffer);
  }
}