INSTRUCTIONS
NOTE: Things wrapped in quotations are commands - DO NOT RUN THE COMMANDS WITH THE QUOTATIONS, THEY WILL NOT WORK!!!!

1. Make sure kernel modules get built into the DEV directory ( /dev )
- This is needed for the test, the test.c file expects the reader and writer files to exists in the /dev directory
2. Navigate to this directory and unzip using the method of your choice
3. Run the "make" command - this will run the makefile and compile all the files
4. Set the writer to the kernel THIS SHOULD BE DONE FIRST!!!!!!!
- To do so run "sudo insmod lkmasg2_writer.ko"
5. Set the reader to the kernel
- Run "sudo insmod lkmasg2_reader.ko"
- It may say "reader is already loaded" THIS IS OK!!!!
6. Run the test
- We've modified the test.c file to accept no arguments and simply run the writer and reader
- Simply run "sudo ./test"
- input whatever you want for the text, this should be a SHORT string
7. Check the logs from printk
- Simply run " sudo dmesg "

