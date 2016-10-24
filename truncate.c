#include <stdio.h>
#include <sqlite3.h>

int main(int argc, char** argv)
{
   sqlite3 *db = NULL;
   char *errMsg = 0;
   char queryname[200];
   int nrow = 0;
   int ncolumn = 0;
   int i;
   char **selectResult;
   int opendb = sqlite3_open("/tmp/ramdisk0/namebundle.db", &db);
   if(opendb)
   {
    printf("Cannot open database: %s\n", sqlite3_errmsg(db));
    return 1;  
   }
   
   char deletesql[100] = "DELETE from \"BundleNameID\"";
   sqlite3_exec(db, deletesql, 0, 0, &errMsg);


   sqlite3_close(db);
   return 0;
}
