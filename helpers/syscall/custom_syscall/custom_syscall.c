#include <linux/kernel.h>

asmlinkage long sys_custom_syscall_hello(void) {
	printk("struharv SYSCALL");
	return 0;
}