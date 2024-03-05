from rest_framework import serializers
from ..models.creator import Creator

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        exclude = ('password',)
