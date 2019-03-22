#include "hal_thread.h"
#include "iec61850_client.h"
#include <stdlib.h>
#include <stdio.h>

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
			Thread_sleep(1);
		}
		
	} else 
		printf("Connection failed.");
		
	IedConnection_destroy(connection);	
}
