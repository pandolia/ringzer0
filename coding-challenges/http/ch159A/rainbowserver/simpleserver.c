#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

#define MAXPENDING 5        /* Max connection requests */

void Die(char *message) { perror(message); exit(1); }

typedef void (*Handler)(int sock);

void ServeForeverAt(const char* addr, unsigned short port, Handler handle)
{
    int serversock, clientsock;
    struct sockaddr_in echoserver, echoclient;

    /* Create the TCP socket */
    if ((serversock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {
        Die("Failed to create socket");
    }

    /* Construct the server sockaddr_in structure */
    memset(&echoserver, 0, sizeof(echoserver));     /* Clear the structure */
    echoserver.sin_family = AF_INET;                /* Internet/IP */
    echoserver.sin_addr.s_addr = inet_addr(addr);   /* Incoming addr */
    echoserver.sin_port = htons(port);              /* Server port */

    /* Bind the server socket */
    if (bind(serversock,
             (struct sockaddr *) &echoserver,
             sizeof(echoserver)) < 0) {
        Die("Failed to bind the server socket");
    }

    /* Listen on the server socket */
    if (listen(serversock, MAXPENDING) < 0) {
        Die("Failed to listen on server socket");
    }

    fprintf(stdout, "Server is running...\n");

    /* Run until cancelled */
    while (1) {
        unsigned int clientlen = sizeof(echoclient);
        /* Waiting for client connection */
        if ((clientsock = accept(serversock,
                                 (struct sockaddr *) &echoclient,
                                 &clientlen)) < 0) {
            Die("Failed to accept client connection");
        }
        fprintf(stdout, "Client connected: %s\n",
                inet_ntoa(echoclient.sin_addr));
        handle(clientsock);
    }
}

/*
int sendall(int sock, char *buf, size_t length)
{
    int bytes;
    while (length > 0 && (bytes = send(sock, buf, length, 0)) > 0) {
        buf += bytes;
        length -= bytes;
    }
    return length == 0;
}

int recvall(int sock, char *buf, size_t length)
{
    int bytes;
    while (length > 0 && (bytes = recv(sock, buf, length, 0)) > 0) {
        buf += bytes;
        length -= bytes;
    }
    return length == 0;
}
*/
