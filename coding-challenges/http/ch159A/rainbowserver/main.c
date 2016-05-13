#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <sys/socket.h>
#include <unistd.h>
#include <openssl/sha.h>

#define WORD_LEN 32

typedef void (*Handler)(int sock);

int CreateRainbow(const char *data_file);
int RainbowLookup(uint8_t *hash_val, uint8_t *word);
void handleClient(int sock);
void ServeForeverAt(const char* addr, unsigned short port, Handler handle);

int main(int argc, char *argv[])
{
    if (argc != 4) {
        fprintf(stderr, "USAGE: %s <datafile> <address> <port>\n", argv[0]);
        return 1;
    }

    fprintf(stdout, "Creating the rainbow...\n");
    if (!CreateRainbow(argv[1])) {
        fprintf(stderr, "Failed to create the rainbow\n");
        return 1;
    }
    fprintf(stdout, "Create the rainbow complete\nStart the rainbow server\n");
    ServeForeverAt(argv[2], atoi(argv[3]), handleClient);

    return 0;
}

void handleClient(int sock)
{
    uint8_t hashval[SHA_DIGEST_LENGTH], word[WORD_LEN+1];
    if (recv(sock, (char*)hashval, sizeof(hashval), 0) == sizeof(hashval)) {
        word[0] = RainbowLookup(hashval, word+1);
        send(sock, (char*)word, word[0]+1, 0);
    }
    close(sock);
}
