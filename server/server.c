#include "iec61850_server.h"
#include "static_model.h"
#include <stdlib.h>
#include <stdio.h>

/* import IEC 61850 device model created from SCL-File */
extern IedModel iedModel;

static int running = 0;
static IedServer iedServer = NULL;

/*
void sigint_handler(int signalId)

	running = 0;
}
*/

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
  char msg = [150];
	//Main thread for server to run
	while (running) {

      printf("Enter a message:\n");
      gets( str );
      printf("You entetered: ");
      puts( str );
	    Thread_sleep(1);
	}

	//Stops Server
	IedServer_stop(iedServer);

	IedServer_destroy(iedServer);
}
