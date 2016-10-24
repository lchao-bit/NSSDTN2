#include <stdio.h>
#include <sqlite3.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>


int main(int argc, char** argv)
{
   sqlite3 *db = NULL;
   char *errMsg = 0;
   char queryname[200];
   int nrow = 0;
   int ncolumn = 0;
   int i;
   char fileid[10];
   char filename[100], errinfo[200];
   char **selectResult;
   FILE *fp;
   int opendb = sqlite3_open("/tmp/ramdisk0/namebundle.db", &db);
   if(opendb)
   {
       printf("ERROR");
       return 1;
   }
   fp = fopen("/tmp/ramdisk0/querylog.txt", "a");
   strcpy(queryname, argv[1]); 
   //certain query section
   char selectsql[100] = "SELECT ID from BundleNameID where NAME=\"";
   strcat(selectsql, queryname);
   strcat(selectsql, "\";");
   sqlite3_get_table(db, selectsql, &selectResult, &nrow, &ncolumn, &errMsg);
   if(errMsg != NULL)
   {
      fprintf(fp, "select errMsg:%s\n", errMsg);
      strcpy(errinfo, errMsg);
      if(strcmp(errinfo, "database is locked") ==0)
      {
         while(errMsg != NULL)
         {
            usleep(100000);
            fprintf(fp, "select error retry message:%s\n", errinfo);
            sqlite3_get_table(db, selectsql, &selectResult, &nrow, &ncolumn, &errMsg);
         } 
      } 
   }
   if(nrow == 0)
   {
      printf("No");
      sqlite3_free_table(selectResult);
      sqlite3_close(db);
      exit(0);
   }
   for( i=1 ; i<( nrow + 1 ) * ncolumn ; i++ )
   {
      strcpy(fileid, selectResult[i]);
      strcpy(filename, "/tmp/ramdisk0/dtn/bundles/bundle_");
      strcat(filename, fileid);
      strcat(filename, ".dat");
      if( access( filename, F_OK ) != -1 )
      {
          printf("%s", filename);
          sqlite3_free_table(selectResult);
          sqlite3_close(db);
          exit(0);
      }
      else
      {
         char deletesql[100] = "DELETE from BundleNameID where ID=";
         strcat(deletesql, fileid);
         strcat(deletesql, ";");
         sqlite3_exec(db, deletesql, 0, 0, &errMsg);
         if(errMsg != NULL)
         {
            fprintf(fp, "delete errMsg:%s\n", errMsg);
            strcpy(errinfo, errMsg);
            if(strcmp(errinfo, "database is locked") ==0)
            {
               while(errMsg != NULL)
               {
                  usleep(100000);
                  fprintf(fp, "delete error retry message:%s\n", errinfo);
                  sqlite3_exec(db, deletesql, 0, 0, &errMsg);
               } 
            } 
         }
      }
   }
   printf("No");
   sqlite3_free_table(selectResult);
   sqlite3_close(db);
   fclose(fp);
   exit(0);
}

