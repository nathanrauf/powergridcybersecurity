#include "hal_thread.h"
#include "iec61850_client.h"
#include "iec61850_server.h"
#include "static_model.h"
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include "iso_connection_parameters.h"
#include "mms_client_connection.h"

#define NUM_TO_CLIENT 2
#define NUM_TO_SERVER 2

extern IedModel iedModel;
static IedServer iedServer = NULL;
static int running = 1;

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
int readFile() {
  // Create file descriptor for the data buffer
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
int writeFile() {
  // File descriptor for the data buffer
  FILE *f = fopen("server_to_client.txt", "w");

  if (fprintf(f, "%f %f", data_to_client[0], data_to_client[1]) < 0) {
    printf("Error reading from server_to_client.txt. \n");
    return 0;
  }

  return 1;
}

static void connectionHandler(IedServer self, ClientConnection connection,
                              bool connected, void *parameter) {
  if (connected)
    printf("Connection opened\n");
  else
    printf("Connection closed\n");
}

void sigint_handler(int signalId) { running = 0; }

int main(int argc, char **argv) {
  printf("1");
  char *hostname;
  int tcpPort = 102;

  printf("1");
  iedServer = IedServer_create(&iedModel);

  /* Set the base path for the MMS file services */
  printf("1");
  MmsServer mmsServer = IedServer_getMmsServer(iedServer);
  MmsServer_setFilestoreBasepath(mmsServer, "./vmd-filestore/");
  IedServer_setConnectionIndicationHandler(
      iedServer, (IedConnectionIndicationHandler)connectionHandler, NULL);

  /* MMS server will be instructed to start listening to client connections. */
  printf("1");
  IedServer_start(iedServer, 103);
  if (!IedServer_isRunning(iedServer)) {
    printf("Starting server failed! Exit.\n");
    IedServer_destroy(iedServer);
    exit(-1);
  }

  running = 1;

  // signal(SIGINT, sigint_handler);

  printf("1");
  IedServer_setWriteAccessPolicy(iedServer, IEC61850_FC_DC,
                                 ACCESS_POLICY_ALLOW);
  IedServer_setWriteAccessPolicy(iedServer, IEC61850_FC_CF,
                                 ACCESS_POLICY_ALLOW);
  IedServer_setWriteAccessPolicy(iedServer, IEC61850_FC_SP,
                                 ACCESS_POLICY_ALLOW);
  IedServer_setWriteAccessPolicy(iedServer, IEC61850_FC_SV,
                                 ACCESS_POLICY_ALLOW);
  IedServer_setWriteAccessPolicy(iedServer, IEC61850_FC_SE,
                                 ACCESS_POLICY_ALLOW);
  
  // Get the host IP from the user
  if (argc > 1) {
    hostname = argv[1];

  } else {
    printf("Enter the host name and try again.");
    exit(1);
  }
  // Get port from the user
  if (argc > 2) {
    tcpPort = atoi(argv[2]);
  }

  // Establish connection with the server
  IedClientError error;
  
  IedConnection connection = IedConnection_create();
  
  MmsConnection mmsCon = IedConnection_getMmsConnection(connection);
  IsoConnectionParameters parameters = MmsConnection_getIsoConnectionParameters(mmsCon);

  char* password = "InfoSec";  
  AcseAuthenticationParameter auth = (AcseAuthenticationParameter)calloc(1, sizeof(struct sAcseAuthenticationParameter));
  auth->mechanism = ACSE_AUTH_PASSWORD;
  auth->value.password.octetString = (uint8_t*) password;
  auth->value.password.passwordLength = strlen(password);
  
  IsoConnectionParameters_setAcseAuthenticationParameter(parameters, auth);
  
  IedConnection_connect(connection, &error, hostname, tcpPort);

  // Successful connection to the server
  if (error == IED_ERROR_OK) {
    // Main loop
    while (running) {
      IedServer_lockDataModel(iedServer);
      printf("\n Data from client: %f %f", data_to_server[0],
             data_to_server[1]);
      printf("\n Data to client:   %f %f", data_to_client[0],
             data_to_client[1]);

      // Begin data reception
      if (error == IED_ERROR_OK) {
        IedConnection_getServerDirectory(connection, &error, false);

        // Get the first value from the server application.
        data_to_client[0] = IedConnection_readFloatValue(
            connection, &error, "OSU_SS1CTRL/GGIO1.AnOut1.subVal.f",
            IEC61850_FC_SV);
        if (error != IED_ERROR_OK) {
          printf("Error reading value from server.");
          exit(1);
        }

        // Get the second value from the server
        data_to_client[1] = IedConnection_readFloatValue(
            connection, &error, "OSU_SS1CTRL/GGIO2.AnOut1.subVal.f",
            IEC61850_FC_SV);
        if (error != IED_ERROR_OK) {
          printf("Error reading value from server.");
          exit(1);
        }

        // Write to the data buffer
        if (writeFile() == 0) {
          printf("\nError occurred while writing to file. Exiting.");
          exit(1);
        }
      } else {
        printf("\nAn error occurred while locking the data model.");
        exit(1);
      }

      // Begin data transmission
      if (error == IED_ERROR_OK) {
        // Read data from the control center
        if (readFile() == 0) {
          printf("\n Error reading from file. Exiting.");
          exit(1);
        }

        // Write the first value to the server IED model
        IedConnection_writeFloatValue(connection, &error,
                                      "OSU_SS1CTRL/GGIO3.AnOut1.subVal.f",
                                      IEC61850_FC_SV, data_to_server[0]);
        if (error != IED_ERROR_OK) {
          printf("\nError writing first power generation value.");
          exit(1);
        }

        // Write the second.
        IedConnection_writeFloatValue(connection, &error,
                                      "OSU_SS1CTRL/GGIO4.AnOut1.subVal.f",
                                      IEC61850_FC_SV, data_to_server[1]);
        if (error != IED_ERROR_OK) {
          printf("\nError writing second power generation value.");
          exit(1);
        }

        IedServer_unlockDataModel(iedServer);
      }
      Thread_sleep(1000);
    }

  } else {
    printf("\nConnection failed.");
  }

  IedConnection_destroy(connection);
}
