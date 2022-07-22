"""Fake bytes and json responses for mocking fuego calls."""
from roarquery.utils import bytes2json


TRIALS_BYTES = b"""
[
{
    "CreateTime": "2022-03-30T15:53:34.246805Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-01",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-01",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:53:34.246805Z"
}
,
{
    "CreateTime": "2022-03-30T15:58:10.022896Z",
    "Data": {
        "correct": false,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-02",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-02",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:58:10.022896Z"
}
,
{
    "CreateTime": "2022-03-30T15:53:18.428104Z",
    "Data": {
        "correct": false,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-03",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-03",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:53:18.428104Z"
}
,
{
    "CreateTime": "2022-03-30T15:54:05.697036Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-04",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-04",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:54:05.697036Z"
}
,
{
    "CreateTime": "2022-03-30T15:57:59.397325Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-05",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-05",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:57:59.397325Z"
}
,
{
    "CreateTime": "2022-03-30T15:54:02.891105Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-06",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-06",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:54:02.891105Z"
}
,
{
    "CreateTime": "2022-03-30T15:53:34.246805Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-01",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-01",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:53:34.246805Z"
}
,
{
    "CreateTime": "2022-03-30T15:58:10.022896Z",
    "Data": {
        "correct": false,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-02",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-02",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:58:10.022896Z"
}
,
{
    "CreateTime": "2022-03-30T15:53:18.428104Z",
    "Data": {
        "correct": false,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-03",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-03",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:53:18.428104Z"
}
,
{
    "CreateTime": "2022-03-30T15:54:05.697036Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-04",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-04",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:54:05.697036Z"
}
,
{
    "CreateTime": "2022-03-30T15:57:59.397325Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-05",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-05",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:57:59.397325Z"
}
,
{
    "CreateTime": "2022-03-30T15:54:02.891105Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-06",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-06",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:54:02.891105Z"
}
]
"""

TRIALS_1_BYTES = b"""
[
{
    "CreateTime": "2022-03-30T15:53:34.246805Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-01",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-01",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:53:34.246805Z"
}
,
{
    "CreateTime": "2022-03-30T15:58:10.022896Z",
    "Data": {
        "correct": false,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-02",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-02",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:58:10.022896Z"
}
,
{
    "CreateTime": "2022-03-30T15:53:18.428104Z",
    "Data": {
        "correct": false,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-03",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-03",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:53:18.428104Z"
}
,
{
    "CreateTime": "2022-03-30T15:54:05.697036Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-04",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-04",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:54:05.697036Z"
}
,
{
    "CreateTime": "2022-03-30T15:57:59.397325Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-05",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-05",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:57:59.397325Z"
}
,
{
    "CreateTime": "2022-03-30T15:54:02.891105Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "aa-0001"
    },
    "ID": "trial-06",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1/trials/trial-06",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:54:02.891105Z"
}
]
"""

TRIALS_4_BYTES = b"""
[
{
    "CreateTime": "2022-03-30T15:53:34.246805Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-01",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-01",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:53:34.246805Z"
}
,
{
    "CreateTime": "2022-03-30T15:58:10.022896Z",
    "Data": {
        "correct": false,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-02",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-02",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:58:10.022896Z"
}
,
{
    "CreateTime": "2022-03-30T15:53:18.428104Z",
    "Data": {
        "correct": false,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-03",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-03",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:53:18.428104Z"
}
,
{
    "CreateTime": "2022-03-30T15:54:05.697036Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-04",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-04",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:54:05.697036Z"
}
,
{
    "CreateTime": "2022-03-30T15:57:59.397325Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-05",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-05",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:57:59.397325Z"
}
,
{
    "CreateTime": "2022-03-30T15:54:02.891105Z",
    "Data": {
        "correct": true,
        "grade": "KG",
        "pid": "bb-0001"
    },
    "ID": "trial-06",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4/trials/trial-06",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:54:02.891105Z"
}
]
"""

RUNS_BYTES = b"""
[
{
    "CreateTime": "2020-01-01T00:00:00.000Z",
    "Data": {
        "name": "run-1",
        "timeStarted": "2020-01-01T00:00:00.000Z",
        "classId": "class-1",
        "completed": "true"
    },
    "ID": "run-1",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-1",
    "ReadTime": "2020-01-01T00:00:00.000Z",
    "UpdateTime": "2020-01-01T00:00:00.000Z"
}
,
{
    "CreateTime": "2020-02-01T00:00:00.000Z",
    "Data": {
        "name": "run-2",
        "timeStarted": "2020-02-01T00:00:00.000Z",
        "classId": "class-2",
        "completed": "true"
    },
    "ID": "run-2",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-2",
    "ReadTime": "2020-02-01T00:00:00.000Z",
    "UpdateTime": "2020-02-01T00:00:00.000Z"
}
,
{
    "CreateTime": "2020-03-01T00:00:00.000Z",
    "Data": {
        "name": "run-3",
        "timeStarted": "2020-03-01T00:00:00.000Z",
        "classId": "class-2",
        "completed": "true"
    },
    "ID": "run-3",
    "Path": "prod/roar-prod/users/aa-0001/runs/run-3",
    "ReadTime": "2020-03-01T00:00:00.000Z",
    "UpdateTime": "2020-03-01T00:00:00.000Z"
}
,
{
    "CreateTime": "2020-01-01T00:00:00.000Z",
    "Data": {
        "name": "run-4",
        "timeStarted": "2020-01-01T00:00:00.000Z",
        "classId": "class-1",
        "completed": "true"
    },
    "ID": "run-4",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-4",
    "ReadTime": "2020-01-01T00:00:00.000Z",
    "UpdateTime": "2020-01-01T00:00:00.000Z"
}
,
{
    "CreateTime": "2020-02-01T00:00:00.000Z",
    "Data": {
        "name": "run-5",
        "timeStarted": "2020-02-01T00:00:00.000Z",
        "classId": "class-2",
        "completed": "true"
    },
    "ID": "run-5",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-5",
    "ReadTime": "2020-02-01T00:00:00.000Z",
    "UpdateTime": "2020-02-01T00:00:00.000Z"
}
,
{
    "CreateTime": "2020-03-01T00:00:00.000Z",
    "Data": {
        "name": "run-6",
        "timeStarted": "2020-03-01T00:00:00.000Z",
        "classId": "class-2",
        "completed": "true"
    },
    "ID": "run-6",
    "Path": "prod/roar-prod/users/bb-0001/runs/run-6",
    "ReadTime": "2020-03-01T00:00:00.000Z",
    "UpdateTime": "2020-03-01T00:00:00.000Z"
}
]
"""

RUNS = bytes2json(RUNS_BYTES)
TRIALS_1 = bytes2json(TRIALS_1_BYTES)
TRIALS_4 = bytes2json(TRIALS_4_BYTES)
TRIALS = bytes2json(TRIALS_BYTES)
