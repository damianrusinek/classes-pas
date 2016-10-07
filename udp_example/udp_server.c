#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char * argv[]) {
  int BUF_SIZE = 1024;
  int port;
  int sockfd;
  struct sockaddr_in listen_addr;
  struct sockaddr_in client_addr;
  int sin_size, recv_size;
  char buffer[BUF_SIZE+1];

  if (argc != 2) { 
    fprintf(stderr,"usage: udp_server port\n");
    exit(1);
  }
  port = atoi(argv[1]);
  if (port <= 0) {
    fprintf(stderr,"error: invalid port\n");
    exit(1);
  }
  if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
    perror("socket");
    exit(1);
  }

  listen_addr.sin_family = AF_INET;
  listen_addr.sin_port = htons(port);
  listen_addr.sin_addr.s_addr = INADDR_ANY;

  if (bind(sockfd, (struct sockaddr *)&listen_addr, sizeof(struct sockaddr)) == -1) {
    perror("bind");
    exit(1);
  }

  while(1) { 
    sin_size = sizeof(struct sockaddr);
    if ((recv_size = recvfrom(sockfd, buffer, BUF_SIZE, 0, (struct sockaddr *)&client_addr, &sin_size)) == 0) {
      close(sockfd);
      if (errno != 0) {
        perror("recvfrom");
      }
      break;
    }
    buffer[recv_size] = '\0';
    printf("Received message. Size: %d, message: %s", recv_size, buffer);
    if (sendto(sockfd, buffer, recv_size, 0, (struct sockaddr *)&client_addr, sizeof(struct sockaddr)) == -1) {
      perror("sendto");
      close(sockfd);
      break;
    }
  }
}