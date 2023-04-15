from mongoengine import (
    Document,
    FloatField,
    StringField,
    ListField,
    ReferenceField,
    DateTimeField,
)
from mongoengine.errors import ValidationError
from datetime import datetime


# Custom modules
from app.models.patientDbModel import Patient


class DefaultAttributes:
    meta = {"allow_inheritance": True}
    creation_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(DefaultAttributes, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.modified_date = datetime.datetime.now()
        return super(DefaultAttributes, self).save(*args, **kwargs)


# "MedicalRecord" model with validators
class MedicalRecord(Document):
    bloodSugarLevel = FloatField(required=True, min_value=0, max_value=500)
    height = FloatField(required=True, min_value=0, max_value=300)
    weight = FloatField(required=True, min_value=0, max_value=1000)
    allergies = ListField(StringField())
    medications = ListField(StringField())
    medicalHistory = ListField(StringField())
    systolicPressure = FloatField(required=True, min_value=0, max_value=300)
    diastolicPressure = FloatField(required=True, min_value=0, max_value=300)
    patientId = ReferenceField(Patient, required=True)

    # Custom validation method for the "MedicalRecord" model
    def clean(self):
        # Check if systolic pressure is greater than diastolic pressure
        if self.systolicPressure < self.diastolicPressure:
            raise ValidationError(
                "Systolic pressure cannot be less than diastolic pressure"
            )
