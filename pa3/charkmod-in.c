/**
 * File:	lkmasg2_writer.c
 * Adapted for Linux 5.15 by: John Aedo
 * Group 24: Akeen Lewis, David Ferguson, Christopher Flannery, McgGreggor Kennison
 * Class:	COP4600-SP23
 */

#include <linux/module.h>
#include <linux/device.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/mutex.h>

#define DEVICE_NAME "charkmod_in"
#define CLASS_NAME "chark_writer"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("John Aedo");
MODULE_DESCRIPTION("lkmasg2 Writer Kernel Module");
MODULE_VERSION("0.2");

static int major_number;
static struct class* lkmasg2WriterClass = NULL;
static struct device* lkmasg2WriterDevice = NULL;

char shared_buffer[1025] = {0};

//extern struct mutex buffer_mutex;
short shared_buffer_size = 0;
EXPORT_SYMBOL(shared_buffer_size);
EXPORT_SYMBOL(shared_buffer);
DEFINE_MUTEX(buffer_mutex);
EXPORT_SYMBOL(buffer_mutex);

static int open(struct inode *, struct file *);
static int close(struct inode *, struct file *);
static ssize_t write(struct file *, const char *, size_t, loff_t *);

static struct file_operations fops = {
        .owner = THIS_MODULE,
        .open = open,
        .release = close,
        .write = write,
};

int init_module(void) {
    printk(KERN_INFO "lkmasg2 Writer module successfully installed\n");

    major_number = register_chrdev(0, DEVICE_NAME, &fops);
    if (major_number < 0) {
        printk(KERN_ALERT "lkmasg2 Writer - Error Encountered major_number less than 0\n");
        return major_number;
    }

    lkmasg2WriterClass = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(lkmasg2WriterClass)) {
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "lkmasg2 Writer - Error encountered couldn't register device class\n");
        return PTR_ERR(lkmasg2WriterClass);
    }

    lkmasg2WriterDevice = device_create(lkmasg2WriterClass, NULL, MKDEV(major_number, 0), NULL, DEVICE_NAME);
    if (IS_ERR(lkmasg2WriterDevice)) {
        class_destroy(lkmasg2WriterClass);
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "lkmasg2 Writer - Error encountered, couldn't to create the device\n");
        return PTR_ERR(lkmasg2WriterDevice);
    }

    mutex_init(&buffer_mutex);
    return 0;
}

void cleanup_module(void) {
    device_destroy(lkmasg2WriterClass, MKDEV(major_number, 0));
    class_unregister(lkmasg2WriterClass);
    class_destroy(lkmasg2WriterClass);
    unregister_chrdev(major_number, DEVICE_NAME);
}

static int open(struct inode *inodep, struct file *filep) {
    printk(KERN_INFO "lkmasg2 Writer: device opened.\n");
    return 0;
}

static int close(struct inode *inodep, struct file *filep) {
    printk(KERN_INFO "lkmasg2 Writer: device closed.\n");
    return 0;
}

static ssize_t write(struct file *filep, const char *buffer, size_t len, loff_t *offset) {
    printk(KERN_INFO "lkmasg2 Writer - Entered write().\n");
    mutex_lock(&buffer_mutex);

    printk(KERN_INFO "lkmasg2 Writer - Acquired the lock.\n");
    if (copy_from_user(shared_buffer, buffer, len))
    {
        printk(KERN_ERR "lkmasg2 Writer - Error, couldn't copy from user space\n");
        return -EFAULT;
    }

    shared_buffer_size = strlen(shared_buffer);

    if (len == 1 && buffer[0] == 8)
    {
        printk(KERN_INFO "lkmasg2 Writer - Success, Empty String\n");
        return 0;
    }

    if (len > sizeof(shared_buffer))
    {
        len = sizeof(shared_buffer);
        shared_buffer_size = sizeof(shared_buffer);
    }
    printk(KERN_INFO "lkmasg2 Writer - Wrote %ld bytes to the buffer.\n", len);

    mutex_unlock(&buffer_mutex);
    printk(KERN_INFO "lkmasg2 Writer - Exiting write() function\n");
    return len;
}