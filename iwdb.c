#include <sqlite3.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int main(int argc, char *argv[])
{
   sqlite3 *db = NULL;
   char bdid[20];
   char name[100];
   char errinfo[255];
   char insertsql[100];
   char deletesql[100];
   char dblog[200] = "/tmp/ramdisk0/dblog.txt";
   FILE *fp;
   bdid[0] = '\0';
   name[0] = '\0';
   sprintf(bdid, "%s", argv[1]);
   sprintf(name, "%s", argv[2]);
   fp = fopen(dblog, "a");
   char* errMsg = 0;
   int opendb = sqlite3_open("/tmp/ramdisk0/namebundle.db", &db);
   if(opendb)
   {
       sqlite3_close(db);
       return;
   }

   char deletecomminit[50] = "DELETE from \"BundleNameID\" where ID=";
   deletesql[0]='\0';
   strcpy(deletesql, deletecomminit);
   strcat(deletesql, bdid);
   strcat(deletesql, ";");
   fprintf(fp, "deletesql string:%s\n", deletesql);
   sqlite3_exec(db, deletesql, 0, 0, &errMsg);
   if(errMsg != NULL)
   {
      strcpy(errinfo, errMsg);
      fprintf(fp, "delete error message:%s\n", errMsg);
      fprintf(fp, "errinfo string:%s\n", errinfo);
      if(strcmp(errinfo, "database is locked") == 0)
      {
         while(errMsg != NULL)
         {
            usleep(100000);
            fprintf(fp, "delete error retry message:%s\n", errMsg);
            sqlite3_exec(db, deletesql, 0, 0, &errMsg);
         }
      }
   }


   char insertcomminit[50] = "INSERT INTO \"BundleNameID\" VALUES(";
   insertsql[0] = '\0';
   strcat(insertsql, insertcomminit);
   strcat(insertsql, bdid);
   strcat(insertsql, ", '");
   strcat(insertsql, name);
   char insertcommend[10] = "');";
   strcat(insertsql, insertcommend);
   fprintf(fp, "insertsql string:%s\n", insertsql);
   sqlite3_exec(db, insertsql, 0, 0, &errMsg);
   if(errMsg != NULL)
   {
      strcpy(errinfo, errMsg);
      fprintf(fp, "insert error message:%s\n", errMsg);
      fprintf(fp, "errinfo string:%s\n", errinfo);
      if(strcmp(errinfo, "database is locked") == 0)
      {
         while(errMsg != NULL)
         {
            usleep(100000);
            fprintf(fp, "insert error retry message:%s\n", errMsg);
            sqlite3_exec(db, insertsql, 0, 0, &errMsg);
         }
      }
    }
    fclose(fp);
}
