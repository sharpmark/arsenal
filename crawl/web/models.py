# -*- coding: utf-8 -*-
from django.db import models

class Link(models.Model):

    #parent = models.ForeignKey('Link', null=True)

    href = models.URLField(unique=True)
    timestamp = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
