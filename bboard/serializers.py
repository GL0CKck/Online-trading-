from .models import Rubric, Bb
from rest_framework import serializers


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'name')

class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = ('id','title','price','published','rubric')

