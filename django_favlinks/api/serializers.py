from rest_framework import serializers
from django_favlinks import models


class TagListField(serializers.Field):
    def to_representation(self, obj):
        return [tag.name for tag in obj.all()]

    def to_internal_value(self, data):
        if isinstance(data, list):
            return data
        return data.split(",")


class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagListField()

    class Meta:
        model = models.Bookmark
        fields = "__all__"

    # def create(self, validated_data):
    #     tags = validated_data.pop('tags', [])
    #     bookmark = Bookmark.objects.create(**validated_data)
    #     bookmark.tags.set(*tags)
    #     return bookmark

    # def update(self, instance, validated_data):
    #     tags = validated_data.pop('tags', [])
    #     instance = super().update(instance, validated_data)
    #     instance.tags.set(*tags)
    #     return instance
