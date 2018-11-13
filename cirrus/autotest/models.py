from django.db import models
from django.forms.models import model_to_dict


class RestManager(models.Manager):
    def to_list(self):
        return list(map(model_to_dict, super().all()))


class RestModel(models.Model):
    objects = RestManager()

    def to_dict(self):
        return model_to_dict(self)

    class Meta:
        abstract = True


class Suite(RestModel):
    content = models.TextField()


class Job(RestModel):
    suite_reference = models.ForeignKey('Suite', on_delete=models.SET_NULL, null=True)
    suite_content = models.TextField()
    suts = models.TextField()
