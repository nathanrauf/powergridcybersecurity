#include "hal_thread.h"
#include "iec61850_server.h"
#include "iec61850_client.h"
#include <stdlib.h>
#include <stdio.h>
#include "static_model.h"

#define NUM_TO_CLIENT 2
#define NUM_TO_SERVER 2

extern IedModel iedModel;
static IedServer iedServer = NULL;

// Array holding the data sent to the client
static float data_to_client[NUM_TO_CLIENT];

// Array holding the data sent to the server
static float data_to_server[NUM_TO_SERVER];

/*
  readFile() reads the data from the client back-end application.
  This is typically the control center.
  Uses the global variable data_to_server.
  Returns 1 on a successful read, 0 otherwise.
 */
int readFile () {

  FILE *f = fopen("client_to_server.txt", "r");

  if (fscanf(f, "%f %f", &data_to_server[0], &data_to_server[1]) == 0) {
    printf("Error reading from the client_to_server.txt file.\n");
    return 0;
  }

  return 1;
}

/*
  writeFile() writes the data received by the server.
  This data is typically from the power grid simulator.
  Uses the global variable data_to_client.
  Returns 1 on a successful write operation. 0 otherwise.
 */
int writeFile () {

  FILE *f = fopen("server_to_client.txt", "w");

  if (fprintf(f, "%f %f", data_to_client[0], data_to_client[1]) < 0) {
    printf("Error reading from server_to_client.txt. \n");
    return 0;
  }
  
  return 1;
}


int main (int argc, char ** argv) {
	
	char * hostname;
	int tcpPort = 102;
	int running = 1;
	
	IedClientError error;
	IedConnection connection = IedConnection_create();
	
	// Get the host IP from the user
	if (argc > 1) 
		hostname = argv[1];
	else
		printf("Enter the host name and try again.");
		
	// Get port from the user
	if (argc > 2) {
		tcpPort = atoi(argv[2]);
	}
		
	IedConnection_connect(connection, &error, hostname, tcpPort);
	
	if (error == IED_ERROR_OK) {
		
		// Main loop
		while (running) {
			printf("\nClient is running!");
			Thread_sleep(1000);
		}
		
	} else 
		printf("Connection failed.");
		
	IedConnection_destroy(connection);	
}
