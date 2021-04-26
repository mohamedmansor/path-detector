from django.db import models


class NodeName(models.Model):
    name = models.CharField(max_length=1, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'NodeName'
        managed = True
        verbose_name = 'Node'
        verbose_name_plural = 'Nodes'
    


class Connection(models.Model):
    from_node = models.OneToOneField(NodeName, on_delete=models.CASCADE, related_name='from_node')
    to_node = models.OneToOneField(NodeName, on_delete=models.CASCADE, related_name='to_node')

    def __str__(self):
        return self.from_node.name + " <-> " + self.to_node.name

    class Meta:
        db_table = 'Connection'
        managed = True
        verbose_name = 'Connection'
        verbose_name_plural = 'Connections'
        unique_together = ('from_node', 'to_node')

    

    @staticmethod
    def connect_nodes(from_node, to_node):
        connection, created = Connection.objects.get_or_create(from_node=from_node, to_node=to_node)
        if not created:
            return False, connection
        return True, connection