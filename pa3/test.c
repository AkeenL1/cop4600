#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>

#define BUFFER_LENGTH 256             // The buffer length
static char receive[BUFFER_LENGTH];  // The receive buffer from the LKM

int main() {
    int ret, fd_writer, fd_reader;
    char stringToSend[BUFFER_LENGTH];

    // Open the writer device
    fd_writer = open("/dev/lkmasg2_writer", O_WRONLY);
    if (fd_writer < 0){
        perror("Failed to open the writer device...");
        return errno;
    }

    // Open the reader device
    fd_reader = open("/dev/lkmasg2_reader", O_RDONLY);
    if (fd_reader < 0){
        perror("Failed to open the reader device...");
        close(fd_writer); // Close the already opened writer device
        return errno;
    }

    printf("Type in a short string to send to the kernel module:\n");
    scanf("%[^\n]%*c", stringToSend);  // Read in a string (with spaces)
    printf("Writing message to the writer device: [%s].\n", stringToSend);
    ret = write(fd_writer, stringToSend, strlen(stringToSend)); // Send the string to the LKM
    if (ret < 0){
        perror("Failed to write the message to the device.");
        return errno;
    }

    printf("Press ENTER to read back from the reader device...\n");
    getchar();

    printf("Reading from the reader device...\n");
    ret = read(fd_reader, receive, BUFFER_LENGTH); // Read the response from the LKM
    if (ret < 0){
        perror("Failed to read the message from the device.");
        return errno;
    }
    printf("The received message is: [%s]\n", receive);

    close(fd_reader);
    close(fd_writer);
    return 0;
}
