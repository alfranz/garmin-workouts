from typing import Optional
from pydantic import BaseModel
from garminworkouts.models.pace import PaceRange

from pydantic import model_validator


class WorkoutStep(BaseModel):
    duration: Optional[float] = None  # duration in seconds
    distance: Optional[float] = None  # distance in meters
    target: Optional[str]  # should refer to a RunningZone

    @model_validator(mode="after")
    def check_duration_or_distance(self):
        duration = self.duration
        distance = self.distance
        if not (duration is None) ^ (distance is None):
            raise ValueError("Exactly one of duration or distance must be provided")
        return self


class RunningWorkoutConfig(BaseModel):
    name: str
    description: Optional[str]
    zones: list[PaceRange]
    steps: list[WorkoutStep]

    class Config:
        arbitrary_types_allowed = True


class RunningWorkout:
    def __init__(self, config: RunningWorkoutConfig):
        self.config = config

    def create_workout(self):
        workout_steps = []

        # Create a dictionary for easy lookup of zones by name
        zones_dict = {zone.name: zone for zone in self.config.zones}

        for order, step in enumerate(self.config.steps, start=1):
            step_data = {
                "type": "ExecutableStepDTO",
                # "stepId": step_id,
                "stepOrder": order,
                "stepType": {
                    "stepTypeId": 3,  # Assuming interval step for simplicity
                    "stepTypeKey": "interval",
                    "displayOrder": 3,
                },
                "childStepId": None,
                "description": None,
                "endCondition": {
                    "conditionTypeId": 3 if step.distance else 2,
                    "conditionTypeKey": "distance" if step.distance else "time",
                    "displayOrder": 3 if step.distance else 2,
                    "displayable": True,
                },
                "endConditionValue": step.distance if step.distance else step.duration,
                "preferredEndConditionUnit": (
                    {"unitId": 2, "unitKey": "kilometer", "factor": 100000.0}
                    if step.distance
                    else None
                ),
                "endConditionCompare": None,
                "targetType": {
                    "workoutTargetTypeId": 6,  # Assuming pace zone for simplicity
                    "workoutTargetTypeKey": "pace.zone",
                    "displayOrder": 6,
                },
                "targetValueOne": None,
                "targetValueTwo": None,
                "targetValueUnit": None,
                "zoneNumber": None,
                "secondaryTargetType": None,
                "secondaryTargetValueOne": None,
                "secondaryTargetValueTwo": None,
                "secondaryTargetValueUnit": None,
                "secondaryZoneNumber": None,
                "endConditionZone": None,
                "strokeType": {
                    "strokeTypeId": 0,
                    "strokeTypeKey": None,
                    "displayOrder": 0,
                },
                "equipmentType": {
                    "equipmentTypeId": 0,
                    "equipmentTypeKey": None,
                    "displayOrder": 0,
                },
                "category": None,
                "exerciseName": None,
                "workoutProvider": None,
                "providerExerciseSourceId": None,
                "weightValue": None,
                "weightUnit": None,
            }

            if step.target:
                zone = zones_dict[step.target]
                step_data["description"] = (
                    f"{zone.pace.lower_bound} - {zone.pace.upper_bound} min/km"
                )
                step_data["targetValueOne"] = self.convert_pace_min_per_km_to_m_per_s(
                    zone.pace.lower_bound
                )
                step_data["targetValueTwo"] = self.convert_pace_min_per_km_to_m_per_s(
                    zone.pace.upper_bound
                )

            workout_steps.append(step_data)

        workout = {
            "workoutId": None,  # or some generated ID
            "ownerId": None,  # or some owner ID
            "workoutName": self.config.name,
            "description": self.config.description,
            "updatedDate": None,
            "createdDate": None,
            "sportType": {
                "sportTypeId": 1,
                "sportTypeKey": "running",
                "displayOrder": 1,
            },
            "subSportType": None,
            "trainingPlanId": None,
            "author": None,
            "sharedWithUsers": None,
            "estimatedDurationInSecs": None,
            "estimatedDistanceInMeters": None,
            "workoutSegments": [
                {
                    "segmentOrder": 1,
                    "sportType": {
                        "sportTypeId": 1,
                        "sportTypeKey": "running",
                        "displayOrder": 1,
                    },
                    "poolLengthUnit": None,
                    "poolLength": None,
                    "avgTrainingSpeed": None,
                    "estimatedDurationInSecs": None,
                    "estimatedDistanceInMeters": None,
                    "estimatedDistanceUnit": None,
                    "estimateType": None,
                    "description": None,
                    "workoutSteps": workout_steps,
                }
            ],
            "poolLength": None,
            "poolLengthUnit": None,
            "locale": None,
            "workoutProvider": None,
            "workoutSourceId": None,
            "uploadTimestamp": None,
            "atpPlanId": None,
            "consumer": None,
            "consumerName": None,
            "consumerImageURL": None,
            "consumerWebsiteURL": None,
            "workoutNameI18nKey": None,
            "descriptionI18nKey": None,
            "avgTrainingSpeed": None,
            "estimateType": None,
            "estimatedDistanceUnit": None,
            "workoutThumbnailUrl": None,
            "isSessionTransitionEnabled": None,
            "shared": False,
        }

        return workout
