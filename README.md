# Garmin Connect Workouts Tools

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/alfranz/garmin-workouts/actions/workflows/ci.yml/badge.svg)](https://github.com/alfranz/garmin-workouts/actions/workflows/ci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/alfranz/garmin-workouts/master.svg)](https://results.pre-commit.ci/latest/github/alfranz/garmin-workouts/master)
[![codecov](https://codecov.io/github/alfranz/garmin-workouts/graph/badge.svg?token=1NKLC2J9RP)](https://codecov.io/github/alfranz/garmin-workouts)

Python commandline for managing Garmin Connect workouts.

*Note: This is a fork of the original project by [mkuthan](https://github.com/mkuthan/garmin-workouts)*

Features:

* Target power is set according to your current FTP.
* You can define custom pace zones for running workouts.
* All workouts under Your control stored as JSON files.
* Easy to understand workout format, see examples below.
* Workout parts like warm-up or cool-down are reusable.
* Schedule saved workouts
* The most important parameters (TSS, IF, NP) embedded in workout description field.

## Roadmap

* [x] add Running workouts

## Installation

Requirements:

* Python 3.9-3.11
* [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

Clone this repo:

```shell
git clone https://github.com/alfranz/garmin-workouts.git
```

And then install the CLI with `poetry`.

```shell
cd garmin-workouts
poetry install
```

## Usage

First call to Garmin Connect takes some time to authenticate user.

### Authentication

Define Garmin connect account credentials as `GARMIN_USERNAME` and `GARMIN_PASSWORD` environment variables:

```shell
export GARMIN_USERNAME=username
export GARMIN_PASSWORD=password
```

Alternatively use `-u` and `-p` command line arguments.

### Import Workouts

*Only running workouts have been tested.*

Import workouts into Garmin Connect from definitions in [YAML](https://yaml.org) files.
If the workout already exists it will be updated:

```shell
garminworkouts import 'sample_workouts/running//*.yaml'
```

Sample running workout definition:

```yaml
name: "Easy 10K with some strides"
description: |
      Easy 10K run at a conversational pace. 
      In the last 2K, do 4x20sec strides at 80% effort.
settings:
  type: "running"
  zones: { easy: "5:10-5:35", intervall: "3:20-3:40", rest: "5:30-10:00" }
steps:
  - { zone: "easy", distance: "8km" }
  - &STRIDES
    - &FAST { zone: "intervall", duration: "0:20" }
    - &SLOW { zone: "rest", duration: "1:30" }
  - *STRIDES
  - *STRIDES
  - *STRIDES
```

* Zones have to be defined as min/km with upper and lower pace targets, e.g. `5:10-5:35` format.

Each workout step can be defined with either `duration` or `distance` keys:

* Duration is defined as HH:MM:SS (or MM:SS, or SS) format.If the duration is not specified "Lap Button Press" will be used to move into next workout step.

* Distance can be specified in kms or meters but shall always include the unit, e.g. "400 meters", "400M", "1km", "1 kilometer".

Reusing workout definitions:

* `!include` is a custom YAML directive for including another file as a part of the workout.

Reusing workout steps:

```yaml
steps:
  - !include inc/warmup.yaml
  - { power: 70, duration: "20:00" }
  - { duration: "5:00" }
  - { power: 70, duration: "20:00" }
  - !include inc/cooldown.yaml
```

* Thanks to YAML aliases, workout steps can be easily reused once defined.

Sample Over-Under workout:

```yaml
steps:
  - { zone: "easy", distance: "8km" }
  - &STRIDES
    - &FAST { zone: "intervall", duration: "0:20" }
    - &SLOW { zone: "rest", duration: "1:30" }
  - *STRIDES
  - *STRIDES
  - *STRIDES
```

* All nested sections are mapped as repeated steps in Garmin Connect.
First repeat for warmup, second repeat for main interval (repeated 3 times) and the last one for cool down.

Check the `sample_workouts` folder to get an idea of the formatting possibilities.

### Get Workout

Print full workout definition (as JSON):

```shell
$ garminworkouts get --id [WORKOUT_ID]
{"workoutId": 188952654, "ownerId": 2043461, "workoutName": "VO2MAX 5x4", "description": "FTP 214, TSS 80, NP 205, IF 0.96", "updatedDate": "2020-02-11T14:37:56.0", ...
```

### Schedule  Workouts

Schedule preexisting workouts using the workout number (e.g. "<https://connect.garmin.com/modern/workout/234567894>")
The workout number is the last digits of the URL here: 234567894
Note: the date format is as follows: "2024-04-20"

```shell
garminworkouts schedule -d [DATE] -w [WORKOUT_ID]
```
