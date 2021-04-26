
from rest_framework import serializers


class NodeSerializer(serializers.Serializer):
    from_node = serializers.CharField(required=True)
    to_node = serializers.CharField(required=True)


class PathSerializer(serializers.Serializer):
    path = serializers.CharField(required=True)
