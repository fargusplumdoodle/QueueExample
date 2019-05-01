import random
import time
import threading
from collections import deque
from QueueExample.conf import MAX_SCANS


class Queue(threading.Thread):
    """
    Queue class.
        - Accessed from the settings file.
        - The Queue runs in its own thread.
        - Job objects can be added through Queue.add() function

    Procedure:
        1. start any jobs if they are ready
        2. handle any jobs that are finished
        3. sleep for an arbitrary amount of time to
            prevent unnecessarily overworking the CPU
        4. Repeat
    """

    def __init__(self):
        super(Queue, self).__init__()
        self.job_queue = deque()
        self.running_jobs = set()
        self.running = True

    def stop(self):
        self.running = False

    def add(self, job):
        """
        Procedure:
            1. Validate input
            2. Add job to end of queue
            3. return scan id

        :param job: Must be of Type job
        :return: scan_id (int)
        """
        # 1.
        assert type(job) == Job  # cant add non jobs to queue

        # 2.
        self.job_queue.appendleft(job)

        # 3.
        return job.id

    def __execute_tool(self, tool):
        """
        This does not remove the tool from the queue, it is assumed that self.job_queue.pop()

        :param tool: Tool from the queue

        Procedure:
            1. Run tool in seperate thread
            2. Update tools status
            3. Move tool to the running jobs set

        To be ran internally from the self.start_ready_jobs function
        """
        # 1.
        tool.tool.start()

        # 2.
        tool.status = "RUNNING"

        # 3.
        self.running_jobs.add(tool)

    def __start_ready_jobs(self):
        # TODO: add documentation
        # TODO: make queue smarter
        if len(self.job_queue) > 0 and len(self.running_jobs) < MAX_SCANS:
            # starting each job in order on the queue
            for x in range(len(self.job_queue)):
                # Removing a job from the queue and executing it
                self.__execute_tool(self.job_queue.pop())

    def __handle_finished_jobs(self):
        """
        Procedure:
            1. Go through each running job
            2. if job is finished
                2.1. add job to list of finished jobs
            3. go through finished jobs list
                3.1. remove job
                3.2. update status
        """
        done_jobs = []
        # 1.
        for job in self.running_jobs:
            # 2.
            if job.tool.finished:
                # 2.1
                done_jobs.append(job)
        # 3.
        for job in done_jobs:
            # 3.1
            self.running_jobs.remove(job)

            # 3.2
            # TODO: this would be quite different in production.
            #   at the moment this does nothing
            job.status = "FINISHED"

    def run(self):
        """
        This will only run until the Queue.stop variable is false
        Procedure:
            1. start any jobs if they are ready
            2. handle any jobs that are finished
            3. sleep for an arbitrary amount of time to
                prevent unnecessarily overworking the CPU
            4. Repeat
        """
        while self.running:
            # 1.
            self.__start_ready_jobs()

            # 2.
            self.__handle_finished_jobs()

            # 3.
            time.sleep(1)


class Job(object):
    def __init__(self, tool, user, alias, host):
        """
        Job class:
            for the queueing system!

           :param tool: A subclass of the AbstractTool class

            THE FOLLOWING PARAMETERS/ATTRIBUTES SHOULD BE REPLACED BY A TOOL_OUTPUT OBJECT
            Then they could be referenced from the tool output object.
            For example: Job.tool_output.user

           :param user: string username
           :param alias: string alias
           :param host: string host
        """
        self.tool = tool
        self.status = "PENDING"

        # TODO: Replace these attibutes with a reference to the ToolOutput table
        self.user = user
        self.alias = alias
        self.host = host

        # This ID will be replaced with the ID from the database
        # Maybe it will have to be referenced through the ToolOutput attribute
        self.id = random.choice(range(100))

    def __str__(self):
        return str(self.tool) + '_' + str(self.id)

"""
while False:  # TODO: FLIP
    # if we are able to run a job right now
    if len(self.job_queue) > 0 and len(self.job_queue) < MAX_SCANS:
        # we can run a job, which one do we want
        for x in self.job_queue:
            # seeing if we can run job x
            for running_job in self.running_jobs:
                if x.host == running_job.host:
                    # this host is being scanned, skipping
                    continue
                else:
                    x.run()  # runs job
                    self.running_jobs.add(x)

    self.execute_tool(self.job_queue[0])

    # removing finished jobs
    kick = []
    for x in self.running_jobs:
        if x.is_finished:
            kick.append(x)
    for x in kick:
        self.running_jobs.remove(x)

time.sleep(1)
"""
