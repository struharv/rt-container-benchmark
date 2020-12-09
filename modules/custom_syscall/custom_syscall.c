#include <linux/kernel.h>
#include <linux/string.h>


asmlinkage long sys_custom_syscall_hello(void) {
	printk("struharv SYSCALL");
	trace_printk("struharv START");
	return 0;
}

asmlinkage long sys_custom_syscall_hello_end(void) {
	printk("struharv SYSCALL");
	trace_printk("struharv END");
	return 0;
}