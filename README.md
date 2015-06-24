# Hogwarts

A framework for writing and running text adventures.

## Description

My goal is to write a system that can be used to write and run text adventures. To run a text adventure game, you need a text adventure engine that:

* parses user input
* calls a command that checks if the input can be acted upon
* keeps track of game state.

Part of this project, therefore, is an engine that can do those things for arbitrary game data.

I recently gave a talk on how text adventures / text adventure frameworks work at Open Source Bridge. A rough transcript of the talk is up on [my blog] (http://astrosilverio.tumblr.com/); I'd suggest reading that if you really want to know what's going on.

Besides the engine, the framework should have an API to make gamemaking easy.

### Navigating this repo

Core bits of the engine are in these files:

* Parser: `Legilimens.py`
* Logic Handler: `LogicHandler.py`
* Command class: `Command.py`
* Main state holder: `MaraudersMap.py`
* Base stateful classes (`Player`, `Room`, `Thing`): `base.py`

### Project status

Right now, I've only worked on the engine, and not the API.

I'm mostly happy with parsing and logic (for now). I'm *not* happy with having only three possible stateful classes, working on improving that. Documentation currently only docstring form.

### Immediate To-Do

* Abstract Harry Potter out of file/class names
* Open a pull request for base stateful classes
* Revamp file structure
* Implement better stateful class system using ECS

## Prerequisites

* Python 2.*