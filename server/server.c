#include "hal_thread.h"
#include "iec61850_server.h"
#include "static_model.h"
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <iso_connection_parameters.h>

/* import IEC 61850 device model created from SCL-File */
extern IedModel iedModel;

static int running = 0;
static IedServer iedServer = NULL;
//static char AUTH_PASSWORD[] = "InfoSec";

#define NUM_TO_SERVER 2
#define NUM_TO_CLIENT 2

static float data_to_server[NUM_TO_CLIENT];
static float data_to_client[NUM_TO_SERVER];

// Read from the data file
void readFile() {
  FILE *file;

  file = fopen("server_to_client.txt", "r");

  if (file == NULL) {
    printf("Error reading from file");
    exit(1);
  }

  fscanf(file, "%f", &data_to_client[0]);

  fscanf(file, "%f", &data_to_client[1]);

  //	printf("%f, %f\n", data[0], data[1]);

  fclose(file);
}

// Writes data to file
void writeFile() {
  FILE *file;

  file = fopen("client_to_server.txt", "w");

  if (file == NULL) {
    printf("Error occured while writing to file");
    exit(1);
  }

  fprintf(file, "%f ", data_to_server[0]);
  fprintf(file, "%f ", data_to_server[1]);

  fclose(file);
}

// Handles connections from client
static void connectionHandler(IedServer self, ClientConnection connection,
                              bool connected, void *parameter) {
  if (connected)
    printf("Connection opened\n");
  else
    printf("Connection closed\n");
}

void sigint_handler(int signalId) { running = 0; }

int main(int argc, char **argv) {
  int tcpPort = 102;

  // Create server
  iedServer = IedServer_create(&iedModel);

  IedServer_setConnectionIndicationHandler(
      iedServer, (IedConnectionIndicationHandler)connectionHandler, NULL);

  //Authentication
  AcseAuthenticationParameter auth =
    calloc(1, sizeof(struct sAcseAuthenticationParameter));
  auth->mechanism = ACSE_AUTH_PASSWORD;
  auth->value.password.octetString = "InfoSec";
 
  IsoServer isoServer = IedServer_getIsoServer(iedServer);
  IsoServer_setAuthenticator(isoServer, auth, IsoServer_getAuthenticatorParameter(iedServer));

  // Start server
  IedServer_start(iedServer, tcpPort);

  signal(SIGINT, sigint_handler);

  if (!IedServer_isRunning(iedServer)) {
    printf("Starting server failed! Exit.\n");
    IedServer_destroy(iedServer);
    exit(-1);
  } else {
    printf("Server is starting.\n");
    running = 1;
    IedServer_setWriteAccessPolicy(iedServer, IEC61850_FC_DC,
                                   ACCESS_POLICY_ALLOW);
    IedServer_setWriteAccessPolicy(iedServer, IEC61850_FC_CF,
                                   ACCESS_POLICY_ALLOW);
    IedServer_setWriteAccessPolicy(iedServer, IEC61850_FC_SV,
                                   ACCESS_POLICY_ALLOW);
    IedServer_setWriteAccessPolicy(iedServer, IEC61850_FC_SE,
                                   ACCESS_POLICY_ALLOW);
    IedServer_setWriteAccessPolicy(iedServer, IEC61850_FC_SP,
                                   ACCESS_POLICY_ALLOW);
  }

  // Main thread for server to run
  while (running) {

    printf("\n Data from client: %f %f", data_to_server[0], data_to_server[1]);

    printf("\n Data to client:   %f %f", data_to_client[0], data_to_client[1]);

    IedServer_lockDataModel(iedServer);

    // Read the data from control center
    readFile();

    // Update the models
    IedServer_updateFloatAttributeValue(
        iedServer, IEDMODEL_CTRL_GGIO1_AnOut1_subVal_f, data_to_client[0]);
    IedServer_updateFloatAttributeValue(
        iedServer, IEDMODEL_CTRL_GGIO2_AnOut1_subVal_f, data_to_client[1]);

    // Get the data from the client
    data_to_server[0] = IedServer_getFloatAttributeValue(
        iedServer, IEDMODEL_CTRL_GGIO3_AnOut1_subVal_f);
    data_to_server[1] = IedServer_getFloatAttributeValue(
        iedServer, IEDMODEL_CTRL_GGIO4_AnOut1_subVal_f);

    writeFile();
    IedServer_unlockDataModel(iedServer);

    Thread_sleep(1000);
  }

  // Stops Server
  IedServer_stop(iedServer);
  IedServer_destroy(iedServer);
}
