#include "iec61850_server.h"
#include "static_model.h"
#include <stdlib.h>
#include <stdio.h>

/* import IEC 61850 device model created from SCL-File */
extern IedModel iedModel;

static int running = 0;
static IedServer iedServer = NULL;


static float data[2];

//Read from the data file
void readFile(){
	FILE *file;

	printf("Reading data file\n");
	
	file = fopen("dataFile.txt", "r");
	
	if(file == NULL){
		printf("Error reading from file");
		exit(1);
	}
	
	fscanf(file, "%f", &data[0]);

	fscanf(file, "%f", &data[1]);

	printf("%f, %f\n", data[0], data[1]);

	fclose(file);
}

//Writes data to file
void writeFile(){
	File *file;

	printf("Writing to data file"):
	
	file = fopen("writeDataFile.txt", "w");

	if(file == NULL){
		printf("Error occured while writing to file"):
		exit(1);
	}

	fprintf(file, "%f", data[0]);
	fprintf(file, "%f", data[1]);

	fclose(file);
}

//Handles connections from client
static void connectionHandler(IedServer self, ClientConnection connection,
                              bool connected, void *parameter) {
  if (connected)
    printf("Connection opened\n");
  else
    printf("Connection closed\n");
}

int main(int argc, char** argv) {
	int tcpPort = 102;

    	if (argc > 1) {
        	tcpPort = atoi(argv[1]);
    	}

	//Create server
	iedServer = IedServer_create(&iedModel);

	IedServer_setConnectionIndicationHandler(
      	iedServer, (IedConnectionIndicationHandler)connectionHandler, NULL);

	//Start server
	IedServer_start(iedServer, -1);

	if (!IedServer_isRunning(iedServer)) {
		printf("Starting server failed! Exit.\n");
		IedServer_destroy(iedServer);
		exit(-1);
	}
	else{
		printf("Server is starting.\n");
	}

	running = 1;
<<<<<<< HEAD

	
 
	//Main thread for server to run
	while (running) {
	    Thread_sleep(5000);
	    readFile();
	    Thread_sleep(10000);
	    writeFile();
=======
  char msg = [150];
	//Main thread for server to run
	while (running) {

      printf("Enter a message:\n");
      gets( str );
      printf("You entetered: ");
      puts( str );
	    Thread_sleep(1);
>>>>>>> 35b802070a24e92c1901c0e8f07df4cc0cf44f37
	}

	//Stops Server
	IedServer_stop(iedServer);

	IedServer_destroy(iedServer);
}
