/**
 * File:	lkmasg2_writer.c
 * Adapted for Linux 5.15 by: John Aedo
 * Group 24: Akeen Lewis, David Ferguson, Christopher Flannery, McgGreggor Kennison
 * Class:	COP4600-SP23
 */

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/mutex.h>
#define DEVICE_NAME "lkmasg2_writer"
#define CLASS_NAME "char"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("John Aedo");
MODULE_DESCRIPTION("lkmasg2 Writer Kernel Module");
MODULE_VERSION("0.2");

static int major_number;
static struct class* lkmasg2Class = NULL;
static struct device* lkmasg2Device = NULL;

extern char shared_buffer[1024];
extern struct mutex buffer_mutex;
static short shared_buffer_size = 0;

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

    lkmasg2Class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(lkmasg2Class)) {
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "lkmasg2 Writer - Error encountered couldn't register device class\n");
        return PTR_ERR(lkmasg2Class);
    }

    lkmasg2Device = device_create(lkmasg2Class, NULL, MKDEV(major_number, 0), NULL, DEVICE_NAME);
    if (IS_ERR(lkmasg2Device)) {
        class_destroy(lkmasg2Class);
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "lkmasg2 Writer - Error encountered, couldn't to create the device\n");
        return PTR_ERR(lkmasg2Device);
    }

    mutex_init(&buffer_mutex);
    return 0;
}

void cleanup_module(void) {
    device_destroy(lkmasg2Class, MKDEV(major_number, 0));
    class_unregister(lkmasg2Class);
    class_destroy(lkmasg2Class);
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
    if (len > sizeof(shared_buffer) - shared_buffer_size) {
        printk(KERN_INFO "lkmasg2 Writer - Buffer has %ld bytes remaining, attempting to write %ld, truncating input.\n", sizeof(shared_buffer) - shared_buffer_size, len);
        len = sizeof(shared_buffer) - shared_buffer_size;
    }

    if (copy_from_user(shared_buffer + shared_buffer_size, buffer, len)) {
        printk(KERN_ERR "lkmasg2 Writer - Error, couldn't copy from user space\n");
        mutex_unlock(&buffer_mutex);
        return -EFAULT;
    }

    shared_buffer_size += len;
    printk(KERN_INFO "lkmasg2 Writer - Wrote %ld bytes to the buffer.\n", len);

    mutex_unlock(&buffer_mutex);
    printk(KERN_INFO "lkmasg2 Writer - Exiting write() function\n");
    return len;
}