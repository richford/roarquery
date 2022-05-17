from typing import cast
from typing import List
from roarquery.utils import bytes2json
from roarquery.utils import _FuegoResponse


TRIALS_BYTES = b"""
[
{
    "CreateTime": "2022-03-30T15:53:34.246805Z",
    "Data": {
        "correct": true,
        "grade": "KG"
    },
    "ID": "trial-01",
    "Path": "databases/(default)/documents/prod/roar-prod/users/0001/runs/run-1/trials/trial-01",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:53:34.246805Z"
}
,
{
    "CreateTime": "2022-03-30T15:58:10.022896Z",
    "Data": {
        "correct": false,
        "grade": "KG"
    },
    "ID": "trial-02",
    "Path": "databases/(default)/documents/prod/roar-prod/users/0001/runs/run-1/trials/trial-02",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:58:10.022896Z"
}
,
{
    "CreateTime": "2022-03-30T15:53:18.428104Z",
    "Data": {
        "correct": false,
        "grade": "KG"
    },
    "ID": "trial-03",
    "Path": "databases/(default)/documents/prod/roar-prod/users/0001/runs/run-1/trials/trial-03",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:53:18.428104Z"
}
,
{
    "CreateTime": "2022-03-30T15:54:05.697036Z",
    "Data": {
        "correct": true,
        "grade": "KG"
    },
    "ID": "trial-04",
    "Path": "databases/(default)/documents/prod/roar-prod/users/0001/runs/run-1/trials/trial-04",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:54:05.697036Z"
}
,
{
    "CreateTime": "2022-03-30T15:57:59.397325Z",
    "Data": {
        "correct": true,
        "grade": "KG"
    },
    "ID": "trial-05",
    "Path": "databases/(default)/documents/prod/roar-prod/users/0001/runs/run-1/trials/trial-05",
    "ReadTime": "2022-05-17T11:58:49.966593Z",
    "UpdateTime": "2022-03-30T15:57:59.397325Z"
}
,
{
    "CreateTime": "2022-03-30T15:54:02.891105Z",
    "Data": {
        "correct": true,
        "grade": "KG"
    },
    "ID": "trial-06",
    "Path": "databases/(default)/documents/prod/roar-prod/users/0001/runs/run-1/trials/trial-06",
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
    "Path": "prod/roar-prod/users/0001/runs/run-1",
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
    "Path": "prod/roar-prod/users/0001/runs/run-2",
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
    "Path": "prod/roar-prod/users/0001/runs/run-3",
    "ReadTime": "2020-03-01T00:00:00.000Z",
    "UpdateTime": "2020-03-01T00:00:00.000Z"
}
]
"""


RUNS = cast(List[_FuegoResponse], bytes2json(RUNS_BYTES))
TRIALS = cast(List[_FuegoResponse], bytes2json(TRIALS_BYTES))
