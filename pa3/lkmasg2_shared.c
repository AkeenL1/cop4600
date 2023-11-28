#include <linux/module.h>
#include <linux/mutex.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("John Aedo");
MODULE_DESCRIPTION("Shared resources for lkmasg2 modules");
MODULE_VERSION("0.1");

struct mutex buffer_mutex;
char shared_buffer[1024];
EXPORT_SYMBOL(buffer_mutex);
EXPORT_SYMBOL(shared_buffer);
