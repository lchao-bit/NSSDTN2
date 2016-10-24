#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
int main(int argc, char** argv)
{
	int waiting = 1;
        int round = 0;
	char query[200], info[200], dtnquery[200], queryres[1280], queryline[128], tmpfilepath[200];
        dtnquery[0]='\0';
        strcpy(dtnquery, "/home/root/DTN2/apps/dtnquery/dtnquery -m send -s dtn://dtn1.dtn -d dtn://dtn2.dtn -q ");
        strcat(dtnquery, argv[1]);
        strcat(dtnquery, " 2>&1");
        FILE *fp, *wl;
        strcpy(tmpfilepath, "/tmp/ramdisk0/querytmplog/");
        strcat(tmpfilepath, argv[1]);
        wl = fopen(tmpfilepath, "a");
        fp = popen(dtnquery, "r");
        queryres[0] = '\0';
        while(fgets(queryline, sizeof(queryline), fp) != NULL)
        {
           strcat(queryres, queryline);
        }
        pclose(fp);
        fprintf(wl, "%s\n", queryres);
        printf("%s\n", queryres);
        if(strstr(queryres, "error") != NULL)
        {
           int retryquery = 1;
           while(retryquery)
           {
              fp = popen(dtnquery, "r");
              queryres[0] = '\0';
              while(fgets(queryline, sizeof(queryline), fp) != NULL)
              {
                 strcat(queryres, queryline);
              }
              fprintf(wl, "%s\n", queryres);
              if(strstr(queryres, "error") == NULL)
              {
                 retryquery = 0;
              }
              pclose(fp);
           }
        }
        fclose(wl); 
        for(round = 0; round <120; round++)
        {
           query[0]='\0';
           strcpy(query, "/tmp/ramdisk0/accesscache ");
           strcat(query, argv[1]);
           FILE* ac = popen(query, "r");
           char buf[128];
           while (fgets(buf, 128, ac) != NULL)
           {
              printf("OUTPUT: %s\n", buf);
           }
           pclose(ac);
           if (strcmp(buf, "No") !=0 && strcmp(buf, "ERROR") != 0) 
           {
               return 0;
           }
           else
           {
              sleep(1);
              info[0]='\0';
              strcpy(info, "waiting for ");
              strcat(info, argv[1]);
              printf("%s\n", info);
           }
        }
	return 0;
}

