#include <zconf.h>
#include "wrapper.h"
#include <fcntl.h>

#define MAX_SIZE 1024
//define MAX_SIZE sizeof(planet_type)

int MQcreate (mqd_t * mq, char * name)
{
    /* Creates a mailslot with the specified name. Uses mq as reference pointer, so that you can 	reach the handle from anywhere */
    /* Should be able to handle messages of any size */
    /* Should return 1 on success and 0 on fail */

    struct mq_attr attr = {
            0,
            10,
            MAX_SIZE,
            0
    };

    *mq = mq_open(name, O_CREAT | O_RDWR/* | O_NONBLOCK*/, S_IRWXU | S_IRGRP | S_IROTH, &attr);
    printf("Wrapper create: %s\n", strerror(errno));
    if (*mq == (mqd_t)-1) {
        return 0;
    } else {
        return 1;
    }
}

int MQconnect(mqd_t * mq, char * name)
{
    /* Connects to an existing mailslot for writing Uses mq as reference pointer, so that you can 	reach the handle from anywhere*/
    /* Should return 1 on success and 0 on fail*/
    *mq = mq_open(name, O_RDWR);
    //printf("Wrapper connect: %s\n", strerror(errno));
    if (*mq == (mqd_t)-1)
        return 0;
    else
        return 1;
}

ssize_t MQread(mqd_t * mq, void **refBuffer)
{
    /* Read a msg from a mailslot, return nr Uses mq as reference pointer, so that you can 		reach the handle from anywhere */
    /* of successful bytes read              */
    ssize_t bytes = mq_receive(*mq, (char*)*refBuffer, MAX_SIZE, NULL);
    if (bytes >= 0) {
        return bytes;
    } else
        return 0;
}

int MQwrite(mqd_t * mq, void * sendBuffer)
{
    /* Write a msg to a mailslot, return nr Uses mq as reference pointer, so that you can 	     reach the handle from anywhere*/
    /* of successful bytes written         */
    int res = mq_send(*mq, (char*)sendBuffer, MAX_SIZE, 1);
    printf("Wrapper send: %s\n", strerror(errno));
    if (res != -1)
        return 1;
    else
        return 0;
}

int MQclose(mqd_t * mq, char * name)
{
    /* close a mailslot, returning whatever the service call returns Uses mq as reference pointer, so that you can
    reach the handle from anywhere*/
    /* Should return 1 on success and 0 on fail*/
    int res = mq_close(*mq);
    if (res == 0) {
        res = mq_unlink(name);
        return res == 0 ? 1 : 0;
    } else {
        return 0;
    }
}
