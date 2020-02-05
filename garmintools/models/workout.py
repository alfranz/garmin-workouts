class Workout(object):
    _WORKOUT_ID_FIELD = "workoutId"
    _WORKOUT_NAME_FIELD = "workoutName"
    _WORKOUT_OWNER_ID_FIELD = "ownerId"

    _CYCLING_SPORT_TYPE = {
        "sportTypeId": 2,
        "sportTypeKey": "cycling"
    }

    _INTERVAL_STEP_TYPE = {
        "stepTypeId": 3,
        "stepTypeKey": "interval",
    }

    _REPEAT_STEP_TYPE = {
        "stepTypeId": 6,
        "stepTypeKey": "repeat",
    }

    _POWER_TARGET_DIFF = 0.05

    def __init__(self, config, ftp, power_target_diff=_POWER_TARGET_DIFF):
        self.config = config
        self.ftp = ftp
        self.power_target_diff = power_target_diff

    def create_workout(self, workout_id=None, workout_owner_id=None):
        return {
            self._WORKOUT_ID_FIELD: workout_id,
            self._WORKOUT_OWNER_ID_FIELD: workout_owner_id,
            self._WORKOUT_NAME_FIELD: self.config["name"],
            "description": self._generate_description(),
            "sportType": self._CYCLING_SPORT_TYPE,
            "workoutSegments": [
                {
                    "segmentOrder": 1,
                    "sportType": self._CYCLING_SPORT_TYPE,
                    "workoutSteps": self._steps(self.config["steps"])
                }
            ]
        }

    @staticmethod
    def get_workout_id(workout):
        return workout[Workout._WORKOUT_ID_FIELD]

    @staticmethod
    def get_workout_name(workout):
        return workout[Workout._WORKOUT_NAME_FIELD]

    @staticmethod
    def get_workout_owner_id(workout):
        return workout[Workout._WORKOUT_OWNER_ID_FIELD]

    def _generate_description(self):
        return "TODO: TSS, Stress, Intensity, Time in Zones"

    def _steps(self, steps_config):
        steps, step_order, child_step_id = self._steps_recursive(steps_config, 0, 0)
        return steps

    def _steps_recursive(self, steps_config, step_order, child_step_id):
        if not steps_config:
            return [], step_order, child_step_id

        steps_config_agg = [(1, steps_config[0])]

        for step_config in steps_config[1:]:
            (repeats, prev_step_config) = steps_config_agg[-1]
            if prev_step_config == step_config:  # repeated step
                steps_config_agg[-1] = (repeats + 1, step_config)
            else:
                steps_config_agg.append((1, step_config))

        steps = []
        for repeats, step_config in steps_config_agg:
            step_order = step_order + 1
            if isinstance(step_config, list):
                child_step_id = child_step_id + 1

                repeat_step_order = step_order
                repeat_child_step_id = child_step_id

                nested_steps, step_order, child_step_id = self._steps_recursive(step_config, step_order, child_step_id)
                steps.append(self._repeat_step(repeat_step_order, repeat_child_step_id, repeats, nested_steps))
            else:
                steps.append(self._interval_step(step_config, step_order))

        return steps, step_order, child_step_id

    def _repeat_step(self, step_order, child_step_id, repeats, nested_steps):
        return {
            "type": "RepeatGroupDTO",
            "stepOrder": step_order,
            "stepType": self._REPEAT_STEP_TYPE,
            "childStepId": child_step_id,
            "numberOfIterations": repeats,
            "workoutSteps": nested_steps
        }

    def _interval_step(self, step_config, step_order):
        return {
            "type": "ExecutableStepDTO",
            "stepOrder": step_order,
            "stepType": self._INTERVAL_STEP_TYPE,
            "endCondition": self._end_condition(step_config),
            "endConditionValue": self._end_condition_value(step_config),
            "targetType": self._target_type(step_config),
            "targetValueOne": self._target_value_one(step_config),
            "targetValueTwo": self._target_value_two(step_config)
        }

    @staticmethod
    def _get_duration(step_config):
        return step_config.get("duration")

    def _end_condition(self, step_config):
        duration = self._get_duration(step_config)
        type_id = 2 if duration else 1
        type_key = "time" if duration else "lap.button"
        return {
            "conditionTypeId": type_id,
            "conditionTypeKey": type_key
        }

    def _end_condition_value(self, step_config):
        duration = self._get_duration(step_config)
        return Workout._calculate_duration(duration) if duration else None

    @staticmethod
    def _calculate_duration(duration):
        (minutes, seconds) = duration.split(":")
        return int(minutes) * 60 + int(seconds)

    @staticmethod
    def _get_power(step):
        return step.get("power")

    def _target_type(self, step_config):
        power = self._get_power(step_config)
        type_id = 2 if power else 1
        type_key = "power.zone" if power else "no.target"
        return {
            "workoutTargetTypeId": type_id,
            "workoutTargetTypeKey": type_key
        }

    def _target_value_one(self, step_config):
        power = self._get_power(step_config)
        return self._calculate_power(power, self.ftp, -self.power_target_diff) if power else None

    def _target_value_two(self, step_config):
        power = self._get_power(step_config)
        return self._calculate_power(power, self.ftp, +self.power_target_diff) if power else None

    @staticmethod
    def _calculate_power(power, ftp, diff):
        final_power = int(power) * (1 + diff)
        return round(final_power * ftp / 100)
