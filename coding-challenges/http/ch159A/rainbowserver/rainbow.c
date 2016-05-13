#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <openssl/sha.h>

const uint8_t* const CHARSET = (uint8_t*)"h9857ianeblmt0cdrs4up2vzxo1ykw3fg6qj";

#define CHAR_NUM 18
#define WORD_LEN 6
#define SUB_HASH_LEN 8
#define ITEM_LEN (SUB_HASH_LEN + WORD_LEN)
#define ITEM_COUNT 34012224    // CHAR_NUM ** WORD_LEN
#define RAINBOW_LEN (ITEM_LEN * ITEM_COUNT)

typedef struct _Item {
    uint8_t sub_hash[SUB_HASH_LEN];
    uint8_t word[WORD_LEN];
} Item;

Item RAINBOW[ITEM_COUNT];

int CreateRainbow(const char *data_file);
int RainbowLookup(uint8_t *hash_val, uint8_t *word);
void genItems(Item *items, uint8_t *word, int i, int *j);
int itemCmp(const void *item1, const void *item2);

int CreateRainbow(const char *datafile)
{
    int j = 0;
    FILE* file;
    uint8_t word[WORD_LEN];

    if ((file = fopen(datafile, "rb")) != NULL) {
        size_t readlen = fread((void*)RAINBOW, 1, RAINBOW_LEN, file);
        fclose(file);
        if (readlen == RAINBOW_LEN) {
            return 1;
        }
    }

    genItems(RAINBOW, word, 0, &j);
    qsort((void*)RAINBOW, ITEM_COUNT, ITEM_LEN, itemCmp);

    if ((file = fopen(datafile, "wb"))) {
        fwrite((void*)RAINBOW, 1, RAINBOW_LEN, file);
        fclose(file);
    }

    return 1;
}

void genItems(Item *items, uint8_t *word, int i, int *aj)
{
    if (i == WORD_LEN) {
        int j = *aj;
        uint8_t hash_val[SHA_DIGEST_LENGTH];
        SHA1(word, WORD_LEN, hash_val);
        memcpy((void*)(items[j].sub_hash), (void*)hash_val, SUB_HASH_LEN);
        memcpy((void*)(items[j].word), (void*)word, WORD_LEN);
        *aj = j + 1;
    } else {
        int k;
        for (k = 0; k < CHAR_NUM; k++) {
            word[i] = CHARSET[k];
            genItems(items, word, i+1, aj);
        }
    }
}

int itemCmp(const void *item1, const void *item2)
{
    return memcmp(item1, item2, SUB_HASH_LEN);
}

int RainbowLookup(uint8_t *hash_val, uint8_t *word)
{
    Item *items = RAINBOW;
    Item *p = (Item*)bsearch((void*)hash_val, (void*)items,
                             ITEM_COUNT, ITEM_LEN, itemCmp);
    if (p) {
        Item *end = items + ITEM_COUNT, *q = p + 1, *r = p - 1;
        while (q < end && !itemCmp(p, q)) q++ ;
        while (r > items && !itemCmp(p, r)) r-- ;
        for (p = r + 1; p < q; p++) {
            uint8_t check_hash_val[SHA_DIGEST_LENGTH];
            SHA1(p->word, WORD_LEN, check_hash_val);
            if (!memcmp(check_hash_val, hash_val, SHA_DIGEST_LENGTH)) {
                memcpy(word, p->word, WORD_LEN);
                return WORD_LEN;
            }
        }
    }

    return 0;
}
