#ifndef DEFS_H
#define DEFS_H

typedef struct tagVMStruct
{
	char name[50];
	char ip[20];
	int pid;
	short suspended;
} VMStruct;

#endif
