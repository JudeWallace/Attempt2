# -*- coding: utf-8 -*-
"""
Creates a scheduler to be used throughout all modules
"""
import sched
import time

s = sched.scheduler(time.time, time.sleep)
