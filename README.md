# rt-container-benchmark
This is a benchmark for Real-Time Containers


Real-Time containers 

1. git clone --depth 1 --single-branch --branch v5.0.21 git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git
2. Install build tools needed for kernel compilation. 
sudo apt install git build-essential kernel-package fakeroot libncurses5-dev libssl-dev ccache bison flex
3. Create a kernel config based on our current kernel config and loaded modules.
make localmodconfig
4. Run kernel configurator.
make menuconfig
5. Go to General setup ─> Control Group Support ─> CPU controller ─> Group scheduling for SCHED_RR/FIFO
6. Go to General setup ─> Kernel .config support and enable access to .config through /proc/config.gz
7. Compile & Install the kernel
make -j20
sudo make modules_install -j20
sudo make install -j20
8. Reboot the system
