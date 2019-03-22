#include "iec61850_server.h"
#include "static_model.h"
#include <stdlib.h>
#include <stdio.h>

/* import IEC 61850 device model created from SCL-File */
extern IedModel iedModel;

static int running = 0;

void sigint_handler(int signalId)
{
	running = 0;
}

int main(int argc, char** argv) {

	int tcpPort = 102;

    	if (argc > 1) {
        	tcpPort = atoi(argv[1]);
    	}
 
	//Create server
	IedServer iedServer = IedServer_create(&iedModel);
 
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
 
	//Main thread for server to run
	while (running) {
	    Thread_sleep(1);
	}
 	
	//Stops Server
	IedServer_stop(iedServer);
 
	IedServer_destroy(iedServer);
} 
