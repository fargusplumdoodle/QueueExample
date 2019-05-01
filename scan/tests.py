from django.test import TestCase
import time
from collections import deque
from .Queue import Queue, Job
from .AbstractTool import DummyTool


class TestQueue(TestCase):
    def setUp(self):
        # creates a queue
        self.q = Queue()
        self.q.start()  # running queue system

    def tearDown(self):
        # stops queue system
        self.q.stop()

    @staticmethod
    def get_job():
        tool = DummyTool(run_command="sleep 5")
        alias = "dummy_tool"
        user = 'nobody'
        host = 'nobody'
        return Job(tool, user, alias, host)

    def test_add_job_normally(self):
        # creating example job
        job = self.get_job()

        # adding job to the queue
        self.q.add(job)

        """
        there is a slight possibility that this will give us a false negative
        if the system runs the job between the last statement and the next one.
        Theres no real way around that as far as I can tell unless we were to stop
        the system first
        """
        assert job in self.q.job_queue  # a job should be in the queue if it was added to it

    def test_add_bad_job(self):
        job = "not a job object"
        passed = False

        # adding job to the queue
        try:
            # this should raise an assertion error when we add non job objects to Queue
            self.q.add(job)
        except AssertionError:
            passed = True

        assert passed  # For some reason the system lets you add non job objects to queue
        assert job not in self.q.job_queue  # the system should not add a non-job object to queue

    def test_handle_finished_jobs(self):
        """
        This will ensure that the system can remove jobs from the queue
        that have been finished
        """
        # adding 5 finished jobs to the runnin jobs set
        for x in range(5):
            j = self.get_job()

            # setting job to be finished
            j.tool.finished = True

            # adding finished job to queue
            self.q.running_jobs.add(j)

        passed = False
        for x in range(6):
            # the longest it should take to remove a job from the queue is probably 3 seconds
            time.sleep(0.5)
            if len(self.q.running_jobs) == 0:
                passed = True

        assert passed  # after 3 seconds all of the jobs should have been removed from the queue

    def test_start_ready_jobs_simple(self):
        # here we are just going to add some jobs and see if they get ran

        # clearing queue
        self.q.job_queue = deque()

        # adding 4 jobs to queue
        for x in range(4):
            self.q.add(self.get_job())

        # giving some time for the loop to do its thing
        for x in range(12):
            # the longest it should take to remove a job from the queue is probably 3 seconds
            time.sleep(0.5)
            if len(self.q.job_queue) == 0:
                break
                # this is just to cut down on testing time, this loop could be replaced with time.sleep(3)

        assert len(self.q.job_queue) == 0  # after 3 seconds all jobs should have been removed from the queue

