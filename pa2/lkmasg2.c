/**
 * File:	lkmasg2.c
 * Adapted for Linux 5.15 by: John Aedo
 * Group 24: Akeen Lewis, David Ferguson, Christopher Flannery, McgGreggor Kennison
 * Class:	COP4600-SP23
 */

#include <linux/module.h>	  // Core header for modules.
#include <linux/device.h>	  // Supports driver model.
#include <linux/kernel.h>	  // Kernel header for convenient functions.
#include <linux/fs.h>		  // File-system support.
#include <linux/uaccess.h>	  // User access copy function support.
#define DEVICE_NAME "lkmasg2" // Device name.
#define CLASS_NAME "char"	  ///< The device class -- this is a character device driver

MODULE_LICENSE("GPL");						 ///< The license type -- this affects available functionality
MODULE_AUTHOR("John Aedo");					 ///< The author -- visible when you use modinfo
MODULE_DESCRIPTION("lkmasg2 Kernel Module"); ///< The description -- see modinfo
MODULE_VERSION("0.2");						 ///< A version number to inform users

/**
 * Important variables that store data and keep track of relevant information.
 */
static int major_number;

static struct class *lkmasg2Class = NULL;	///< The device-driver class struct pointer
static struct device *lkmasg2Device = NULL; ///< The device-driver device struct pointer
static char message[1025] = {0};
static char temp_message[sizeof(message)] = {0};
static short message_size = 0;
static int opens = 0;
static struct class* char_class = NULL;
static struct device* char_device = NULL;
/**
 * Prototype functions for file operations.
 */
static int open(struct inode *, struct file *);
static int close(struct inode *, struct file *);
static ssize_t read(struct file *, char *, size_t, loff_t *);
static ssize_t write(struct file *, const char *, size_t, loff_t *);

/**
 * File operations structure and the functions it points to.
 */
static struct file_operations fops =
	{
		.owner = THIS_MODULE,
		.open = open,
		.release = close,
		.read = read,
		.write = write,
};

/**
 * Initializes module at installation
 */
int init_module(void)
{
	printk(KERN_INFO "lkmasg2: installing module.\n");

	// Allocate a major number for the device.
	major_number = register_chrdev(0, DEVICE_NAME, &fops);
	if (major_number < 0)
	{
		printk(KERN_ALERT "lkmasg2 could not register number.\n");
		return major_number;
	}
	printk(KERN_INFO "lkmasg2: registered correctly with major number %d\n", major_number);

	// Register the device class
	lkmasg2Class = class_create(THIS_MODULE, CLASS_NAME);
	if (IS_ERR(lkmasg2Class))
	{ // Check for error and clean up if there is
		unregister_chrdev(major_number, DEVICE_NAME);
		printk(KERN_ALERT "Failed to register device class\n");
		return PTR_ERR(lkmasg2Class); // Correct way to return an error on a pointer
	}
	printk(KERN_INFO "lkmasg2: device class registered correctly\n");

	// Register the device driver
	lkmasg2Device = device_create(lkmasg2Class, NULL, MKDEV(major_number, 0), NULL, DEVICE_NAME);
	if (IS_ERR(lkmasg2Device))
	{								 // Clean up if there is an error
		class_destroy(lkmasg2Class); // Repeated code but the alternative is goto statements
		unregister_chrdev(major_number, DEVICE_NAME);
		printk(KERN_ALERT "Failed to create the device\n");
		return PTR_ERR(lkmasg2Device);
	}
	printk(KERN_INFO "lkmasg2: device class created correctly\n"); // Made it! device was initialized

	return 0;
}

/*
 * Removes module, sends appropriate message to kernel
 */
void cleanup_module(void)
{
	printk(KERN_INFO "lkmasg2: removing module.\n");
	device_destroy(lkmasg2Class, MKDEV(major_number, 0)); // remove the device
	class_unregister(lkmasg2Class);						  // unregister the device class
	class_destroy(lkmasg2Class);						  // remove the device class
	unregister_chrdev(major_number, DEVICE_NAME);		  // unregister the major number
	printk(KERN_INFO "lkmasg2: Goodbye from the LKM!\n");
	unregister_chrdev(major_number, DEVICE_NAME);
	return;
}

/*
 * Opens device module, sends appropriate message to kernel
 */
static int open(struct inode *inodep, struct file *filep)
{
	opens++;
    printk(KERN_INFO "lkmasg2: device opened.\n");
	return 0;
}

/*
 * Closes device module, sends appropriate message to kernel
 */
static int close(struct inode *inodep, struct file *filep)
{
	printk(KERN_INFO "lkmasg2: device closed.\n");
	return 0;
}

/*
 * Reads from device, displays in userspace, and deletes the read data
 */
static ssize_t read(struct file *filep, char *buffer, size_t len, loff_t *offset)
{
    if (len > message_size)
    {
        len = message_size;
    }
    int error_count = 0;
    error_count = copy_to_user(buffer, message, len);

    if (error_count == 0) {
        printk(KERN_INFO "lkmasg2: Success, copied %d characters\n", message_size);
        int i,k;
        for (i = 0, k = len; k < message_size; k++, i++)
        {

            temp_message[i] = message[k];
        }

        for (i = message_size - len; i < message_size; i++)
        {
            message[i] = 0;
        }

        message_size -= len;
        strcpy(message, temp_message);
        return 0;
    } else {
        printk(KERN_ERR "lkmasg2: Failed to send %d characters.\n", error_count);
        return -EFAULT; // Failed -- return a bad address message
    }
	printk(KERN_INFO "lkmasg2: Successfully read from device, displayed and deleted.");
	return 0;
}

/*
 * Writes to the device
 */
static ssize_t write(struct file *filep, const char *buffer, size_t len, loff_t *offset)
{

    if (copy_from_user(message, buffer, len))
    {
        printk(KERN_ERR "lkmasg2: Error, couldn't copy from user space\n");
        return -EFAULT;
    }

    message_size = strlen(message);

    if (len == 1 && buffer[0] == 8)
    {
        printk(KERN_INFO "lkmasg2: Success, Empty String\n");
        return 0;
    }

    if (len > sizeof(message))
    {
        len = sizeof(message);
        message_size = sizeof(message);
    }

    printk(KERN_INFO "lkmasg2: Success, wrote message from userspace: %s\n", message);

    return len;
}
