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
  int sockfd, connectedfd;
  struct sockaddr_in listen_addr;
  struct sockaddr_in client_addr;
  int sin_size, recv_size;
  char buffer[BUF_SIZE+1];

  sin_size = sizeof(struct sockaddr_in);
  if (argc != 2) { 
    fprintf(stderr,"usage: tcp_server port\n");
    exit(1);
  }
  port = atoi(argv[1]);
  if (port <= 0) {
    fprintf(stderr,"error: invalid port\n");
    exit(1);
  }
  if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
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
  if (listen(sockfd, 5) == -1) {
    perror("listen");
    exit(1);
  }
  while(1) { 
    if ((connectedfd = accept(sockfd, (struct sockaddr *)&client_addr, &sin_size)) == -1) {
      perror("accept");
      continue;
    }
    printf("%s connected now.\n", inet_ntoa(client_addr.sin_addr));
    while(1) {
      if ((recv_size = recv(connectedfd, buffer, BUF_SIZE, 0)) == 0) {
        close(connectedfd);
        if (errno != 0) {
          perror("recv");
        }
        break;
      }
      buffer[recv_size] = '\0';
      if (send(connectedfd, buffer, recv_size, 0) == -1) {
        perror("send");
        close(connectedfd);
        break;
      }
    }
  }
}