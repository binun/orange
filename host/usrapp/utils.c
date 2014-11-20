/**
 * section: Scheduling
 * synopsis: Suspend a domain and then resume its execution
 * purpose: Demonstrate the basic use of the library to suspend and
 *          resume a domain. If no id is given on the command line
 *          this script will suspend and resume the first domain found
 *          which is not Domain 0.
 * usage: suspend [id]
 * test: suspend
 * author: Daniel Veillard
 * copy: see Copyright for the status of this software.
 */
#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <memory.h>

int runShell(char *cmd, char *result, int limitResult)
{
	FILE *fp;
	char *redirected = NULL;

	redirected = (char*)malloc(strlen(cmd) + 50);
	memset(redirected,0,strlen(cmd) + 49);

	sprintf(redirected, "%s > tmpStorage.txt", cmd);
	system(redirected);
	fp = fopen("tmpStorage.txt", "r");
	if (fp == NULL)
	{
		printf("The temporary storage cannot be opened\n");
	}
	else
	{
	   while (fgets(result, limitResult, fp) != NULL)
	       printf("%s", result);

	   fclose(fp);
	   system ("rm -f tmpStorage.txt");
	}

	free(redirected);

	return 0;
}
