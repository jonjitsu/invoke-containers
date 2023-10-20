# Overview
Invoke your tasks within containers.

## Run your tasks within containers
Given a task to create a binary with go
```python
@task
def build(c):
    c.run(f"go build")
```
don't assume everyone has go installed, run the task in a container

```python
@container("go:1.20")
@task
def build(c):
    c.run(f"go build")
```

## Specify the container runner program to use
```sh
CONTAINER_INVOKE_PROGRAM="podman" inv build
```

## Temporarily invoke tasks on host (not in containers)
```sh
CONTAINER_INVOKE_ON_HOST=1 inv build
```

## TODO Run part of your task within one or more containers

```python
@task
def super_task(c):
    c.run("echo operation on host")

    with container("go:1.20"):
        c.run("go test")
        c.run("go build")

    with container("sphinxdoc/sphinx"):
        c.run("make html")
```
It's likely that this particular example would be better off split into several tasks using `@container` and using invokes task dependencies.

## TODO specify shared environment
By default each `c.run(COMMAND)` runs in it's own docker container which gets torn down between calls. ex:
```python
c.run(COMMAND1)
c.run(COMMAND2)
...
c.run(COMMANDn)
```
becomes approximately:
```sh
docker run IMAGE COMMAND1
docker run IMAGE COMMAND2
...
docker run IMAGE COMMANDn
```
This results in the internal container state being destroyed on each COMMAND.

If we instead want to create the container environment and then run each command in the single environment, similar to:

```sh
docker container create IMAGE
docker exec CID COMMAND1
docker exec CID COMMAND2
...
docker exec CID COMMANDn
docker container stop CID
docker container rm CID
```

```sh
INVOKE_CONTAINERS_REUSE_CONTAINER=1 \
inv build
```
