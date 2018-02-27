from django.db import models


class Suite(models.Model):
    content = models.TextField()

    def __str__(self):
        case_names = (line.strip() for line in self.content.splitlines()
                                   if line and line[0] not in ' *')
        return ' '.join(f'<Case: {case}>' for case in case_names)


class Result(models.Model):
    log_content = models.TextField()
    suite_content = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    origin_suite = models.ForeignKey(Suite, on_delete=models.SET_NULL, null=True)
