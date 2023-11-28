/**
 * File:	lkmasg2_reader.c
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

#define DEVICE_NAME "lkmasg2_reader"
#define CLASS_NAME "char"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("John Aedo");
MODULE_DESCRIPTION("lkmasg2 Reader Kernel Module");
MODULE_VERSION("0.2");

static int major_number;
static struct class* lkmasg2Class = NULL;
static struct device* lkmasg2Device = NULL;

extern char shared_buffer[1024];
extern struct mutex buffer_mutex;
static short shared_buffer_size = 0;

static int open(struct inode *, struct file *);
static int close(struct inode *, struct file *);
static ssize_t read(struct file *, char *, size_t, loff_t *);

static struct file_operations fops = {
        .owner = THIS_MODULE,
        .open = open,
        .release = close,
        .read = read,
};

int init_module(void) {
    printk(KERN_INFO "lkmasg2 Reader module successfully installed\n");

    major_number = register_chrdev(0, DEVICE_NAME, &fops);
    if (major_number < 0) {
        printk(KERN_ALERT "lkmasg2 Reader Error Encountered could not register a major number\n");
        return major_number;
    }

    lkmasg2Class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(lkmasg2Class)) {
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "lkmasg2 reader Error Encountered Failed to register device class\n");
        return PTR_ERR(lkmasg2Class);
    }

    lkmasg2Device = device_create(lkmasg2Class, NULL, MKDEV(major_number, 0), NULL, DEVICE_NAME);
    if (IS_ERR(lkmasg2Device)) {
        class_destroy(lkmasg2Class);
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "lkmasg2 reader Error Encountered - Failed to create the device\n");
        return PTR_ERR(lkmasg2Device);
    }

    printk(KERN_INFO "lkmasg2 Reader: device class created correctly\n");
    return 0;
}

void cleanup_module(void) {
    device_destroy(lkmasg2Class, MKDEV(major_number, 0));
    class_unregister(lkmasg2Class);
    class_destroy(lkmasg2Class);
    unregister_chrdev(major_number, DEVICE_NAME);
}

static int open(struct inode *inodep, struct file *filep) {
    printk(KERN_INFO "lkmasg2 Reader: device opened.\n");
    return 0;
}

static int close(struct inode *inodep, struct file *filep) {
    printk(KERN_INFO "lkmasg2 Reader: device closed.\n");
    return 0;
}

static ssize_t read(struct file *filep, char *buffer, size_t len, loff_t *offset) {
    printk(KERN_INFO "lkmasg2 Reader - Entered read().\n");
    mutex_lock(&buffer_mutex);

    printk(KERN_INFO "lkmasg2 Reader - Acquired the lock.\n");
    if (len > shared_buffer_size) {
        printk(KERN_INFO "lkmasg2 Reader - Buffer has %d bytes of content, requested %ld.\n", shared_buffer_size, len);
        len = shared_buffer_size;
    }

    if (copy_to_user(buffer, shared_buffer, len)) {
        printk(KERN_ERR "lkmasg2 Reader - Error Encountered, couldn't send to user space\n");
        mutex_unlock(&buffer_mutex);
        return -EFAULT;
    }

    shared_buffer_size -= len;
    memmove(shared_buffer, shared_buffer + len, shared_buffer_size); // Shift remaining data in buffer
    printk(KERN_INFO "lkmasg2 Reader - Read %ld bytes from the buffer.\n", len);

    mutex_unlock(&buffer_mutex);
    printk(KERN_INFO "lkmasg2 Reader - Exiting read() function\n");
    return len;
}
