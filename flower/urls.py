from __future__ import absolute_import

#import os

from django.conf.urls import url, include

# from .api import events
# from .api import control
# from .api import tasks
# from .api import workers
# from .views import auth
from .views import monitor
from .views.broker import BrokerView
# from .views.workers import WorkerView
from .views.tasks import TaskView, TasksView, TasksDataTable
from .views.error import NotFoundErrorHandler
from .views.dashboard import DashboardView, DashboardUpdateHandler
#from .utils import gen_cookie_secret


urlpatterns = [
    # App
    url(r"", DashboardView.as_view(), name='main'),
    url(r"dashboard", DashboardView, name='dashboard'),
    # url(r"worker/(.+)", WorkerView, name='worker'),
    # url(r"task/(.+)", TaskView, name='task'),
    url(r"tasks", TasksView.as_view(), name='tasks'),
    # url(r"tasks/datatable", TasksDataTable),
    url(r"broker", BrokerView.as_view(), name='broker'),
    # # Worker API
    # url(r"api/workers", workers.ListWorkers),
    # url(r"api/worker/shutdown/(.+)", control.WorkerShutDown),
    # url(r"api/worker/pool/restart/(.+)", control.WorkerPoolRestart),
    # url(r"api/worker/pool/grow/(.+)", control.WorkerPoolGrow),
    # url(r"api/worker/pool/shrink/(.+)", control.WorkerPoolShrink),
    # url(r"api/worker/pool/autoscale/(.+)", control.WorkerPoolAutoscale),
    # url(r"api/worker/queue/add-consumer/(.+)", control.WorkerQueueAddConsumer),
    # url(r"api/worker/queue/cancel-consumer/(.+)",
    #     control.WorkerQueueCancelConsumer),
    # # Task API
    # url(r"api/tasks", tasks.ListTasks),
    # url(r"api/task/types", tasks.ListTaskTypes),
    # url(r"api/queues/length", tasks.GetQueueLengths),
    # url(r"api/task/info/(.*)", tasks.TaskInfo),
    # url(r"api/task/apply/(.+)", tasks.TaskApply),
    # url(r"api/task/async-apply/(.+)", tasks.TaskAsyncApply),
    # url(r"api/task/send-task/(.+)", tasks.TaskSend),
    # url(r"api/task/result/(.+)", tasks.TaskResult),
    # url(r"api/task/abort/(.+)", tasks.TaskAbort),
    # url(r"api/task/timeout/(.+)", control.TaskTimout),
    # url(r"api/task/rate-limit/(.+)", control.TaskRateLimit),
    # url(r"api/task/revoke/(.+)", control.TaskRevoke),
    # # Events WebSocket API
    # url(r"api/task/events/task-sent/(.*)", events.TaskSent),
    # url(r"api/task/events/task-received/(.*)", events.TaskReceived),
    # url(r"api/task/events/task-started/(.*)", events.TaskStarted),
    # url(r"api/task/events/task-succeeded/(.*)", events.TaskSucceeded),
    # url(r"api/task/events/task-failed/(.*)", events.TaskFailed),
    # url(r"api/task/events/task-revoked/(.*)", events.TaskRevoked),
    # url(r"api/task/events/task-retried/(.*)", events.TaskRetried),
    # url(r"api/task/events/task-custom/(.*)", events.TaskCustom),
    # # WebSocket Updates
    # url(r"update-dashboard", DashboardUpdateHandler),
    # # Monitors
    url(r"monitor", monitor.Monitor, name='monitor'),
    # url(r"monitor/succeeded-tasks", monitor.SucceededTaskMonitor),
    # url(r"monitor/failed-tasks", monitor.FailedTaskMonitor),
    # url(r"monitor/completion-time", monitor.TimeToCompletionMonitor),
    # url(r"monitor/broker", monitor.BrokerMonitor),
    # Error
    # (r".*", NotFoundErrorHandler),
]
