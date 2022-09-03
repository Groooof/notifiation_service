from core.sender.api import api
from core.sender import dto
import datetime as dt
import typing as tp
import asyncio
from random import randint
from dataclasses import dataclass
import abc


class Worker(metaclass=abc.ABCMeta):
    def __init__(self):
        self._active = False
        self._pause = False

    @abc.abstractmethod
    async def run(self):
        pass

    def pause(self):
        self._pause = True

    def unpause(self):
        self._pause = False

    def is_active(self):
        return self._active

    def is_paused(self):
        return self._pause

    def update(self, **kwargs):
        self.__dict__.update(**kwargs)


class Mailing(Worker):
    def __init__(self, text, phones):
        super().__init__()
        self.text: str = text
        self.phones: tp.Set[str] = set(phones)
        self._processed_phones: tp.Set[str]

    async def run(self):
        self._active = True
        for phone in self.phones:
            msg_id = randint(0, 99999)
            await api.send(msg_id, self.text, phone)
            while not self._pause: pass
        self._active = False


class TasksPlanner:
    def plan(self, loop: asyncio.AbstractEventLoop, coro: tp.Awaitable, date_start, date_stop) -> asyncio.Task:
        planning_coro = self._plan(coro, date_start, date_stop)
        return loop.create_task(planning_coro)

    async def _plan(self, task, date_start, date_stop):
        await self._wait_until(date_start)
        await self._run_until(date_stop, task)

    @staticmethod
    async def _wait_until(date: dt.datetime):
        time_for_waiting = (date - dt.datetime.now()).total_seconds()
        await asyncio.sleep(time_for_waiting if time_for_waiting > 0 else 0)

    @staticmethod
    async def _run_until(date: dt.datetime, task: asyncio.Task):
        time_for_working = (date - dt.datetime.now()).total_seconds()
        try:
            await asyncio.wait_for(task, time_for_working if time_for_working > 0 else 0)
        except asyncio.TimeoutError:
            task.cancel()


@dataclass
class PlannedWorker:
    worker: Mailing
    date_start: dt.datetime
    date_stop: dt.datetime
    task: asyncio.Task = None


class WorkersManager:
    planner: TasksPlanner = TasksPlanner()
    planned: tp.Dict[str, PlannedWorker] = {}

    def __init__(self):
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.get_event_loop()
            self.loop.run_forever()

    def plan(self, id: str, date_start: dt.datetime, date_stop: dt.datetime, worker: Worker):
        planner_task = self.planner.plan(self.loop, worker.run(), date_start, date_stop)
        self._add(id, date_start, date_stop, worker, planner_task)

    def cancel(self, id: str):
        self._get(id).task.cancel()
        self._del(id)

    def update(self, id: str, date_start: dt.datetime = None, date_stop: dt.datetime = None, **kwargs):
        planned = self._get(id)
        if planned.worker.is_active():
            raise Exception('Нельзя изменять параметры активного воркера')

        self.cancel(id)
        planned.worker.update(**kwargs)
        self.plan(id,
                  date_start if date_start is not None else planned.date_start,
                  date_stop if date_stop is not None else planned.date_stop,
                  planned.worker)

    def _add(self, id: str, date_start: dt.datetime, date_stop: dt.datetime, mailing: Mailing, task: asyncio.Task = None):
        self.planned[id] = PlannedWorker(mailing, date_start, date_stop, task)

    def _get(self, id: str):
        planned = self.planned.get(id, None)
        if planned is None:
            raise KeyError(f'Объекта с id "{id}" не существует')
        return planned

    def _del(self, id: str):
        self.planned[id].task.cancel()
        del self.planned[id]
