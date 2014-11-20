#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "vector.h"

void vector_init(vector *v)
{
    v->capacity = VECTOR_INIT_CAPACITY;
    v->total = 0;
    v->items = malloc(sizeof(void *) * v->capacity);
}

int vector_total(vector *v)
{
    return v->total;
}

static void vector_resize(vector *v, int capacity)
{
    void **items = realloc(v->items, sizeof(void *) * capacity);
    if (items) {
        v->items = items;
        v->capacity = capacity;
    }
}

void vector_add(vector *v, void *item)
{
    if (v->capacity == v->total)
        vector_resize(v, v->capacity * 2);
    v->items[v->total++] = item;
}

void vector_set(vector *v, int index, void *item)
{
    if (index >= 0 && index < v->total)
        v->items[index] = item;
}

void *vector_get(vector *v, int index)
{
    if (index >= 0 && index < v->total)
        return v->items[index];
    return NULL;
}

void *vector_getkey(vector *v, char* key)
{
	int position = vector_find(v,key);
	if (position>=0)
		return vector_get(v, position);
	else return NULL;
}

int vector_find(vector *v, char* key)
{
	int i=0;
	for (i = 0; i < v->total; i++)
	{
	   char cur_key[50] = "";
	   strncpy (cur_key, (char*)(v->items[i]), 50);
	   if (!strcmp (cur_key, key))
		   return i;
	}
	return -1;
}

void vector_remove(vector *v, char* key)
{
	int position = vector_find(v,key);
	if (position>=0)
		vector_delete(v, position);
}

void vector_delete(vector *v, int index)
{
	int i = 0;
    if (index < 0 || index >= v->total)
        return;

    if (v->items[index]!=NULL)
    	free(v->items[index]);

    v->items[index] = NULL;

    for (i = 0; i < v->total - 1; i++) {
        v->items[i] = v->items[i + 1];
        v->items[i + 1] = NULL;
    }

    v->total--;

    if (v->total > 0 && v->total == v->capacity / 4)
        vector_resize(v, v->capacity / 2);
}

void vector_free(vector *v)
{
    free(v->items);
}
