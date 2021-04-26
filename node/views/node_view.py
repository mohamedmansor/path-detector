import logging

from django.shortcuts import get_object_or_404
from node.models import Connection, NodeName
from node.serializers import NodeSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q


logger = logging.getLogger('requests')


class ConnectNodesViewSet(viewsets.GenericViewSet):
    """nodes Viewset"""

    def create(self, request):
        """
        Connect Node ViewSet that Connect two nodes
        if the one of nodes or both doesn't exists it'll automatically create it.
        """
        serializer = NodeSerializer(data=self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        from_node, from_node_created = NodeName.objects.get_or_create(name=serializer.validated_data.get('from_node'))
        to_node, to_node_created = NodeName.objects.get_or_create(name=serializer.validated_data.get('to_node'))

        is_new, connection = Connection.connect_nodes(from_node, to_node)

        if not is_new:
            return Response({"details": "Nodes already connected before"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "From": from_node.name,
            "To": to_node.name
        }, status=status.HTTP_201_CREATED)


class PathViewSet(viewsets.GenericViewSet):
    """Path Viewset"""

    @action(detail=False, methods=['GET'], url_path='path')
    def path(self, request):
        from_node = self.request.GET.get('from', None)
        to_node = self.request.GET.get('to', None)

        if not from_node:
            return Response({"details": "Missing the from node"}, status=status.HTTP_400_BAD_REQUEST)

        if not from_node:
            return Response({"details": "Missing the from node"}, status=status.HTTP_400_BAD_REQUEST)

        initial_connection = Connection.objects.filter(from_node__name=from_node.upper())
        final_connection = Connection.objects.filter(to_node__name=to_node.upper())

        if not initial_connection.exists() or not final_connection.exists():
            return Response({"details": "No mathing path"}, status=status.HTTP_400_BAD_REQUEST)

        is_last = False
        nodes = []
        while not is_last:
            node_name = from_node.upper()
            connection = Connection.objects.filter(Q(from_node__name=node_name))
            if not connection:
                is_last = True

            final_node = connection.filter(Q(to_node__name=to_node.upper()))
            if final_node:
                is_last = True
                nodes.append(node_name)
            node_name = connection.last().to_node.name
            nodes.append(connection.last().from_node.name)

        path = ', '.join(nodes)
        return Response({"Path": path}, status=status.HTTP_200_OK)
