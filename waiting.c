#include <stdio.h>
#include <unistd.h>
int main(int argc, char** argv)
{
	int waiting = 1;
	char deliverfile[200], removecomm[200], query[200];
        while(waiting)
        {
		strcpy(query, argv[1]);
		usleep(100000);
                deliverfile[0]='\0';
                strcat(deliverfile, "/home/dtn2/delivered/");
                strcat(deliverfile, query);
                if(0 == access(deliverfile, F_OK))
                {
			waiting = 0;
                        removecomm[0] = '\0';
                        strcat(removecomm, "rm ");
                        strcat(removecomm, deliverfile);
                        system(removecomm);
                }
                printf("Now waiting for deliver signal\n");
                
        }       
	return 0;
}

