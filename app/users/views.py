from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import MessageSerializer
from .documents import MessageDocument
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from management.logger.loggers import baselogger


class MessageViewSet(viewsets.ViewSet, LimitOffsetPagination):
    lookup_field='message_name'
    permission_classes=(IsAuthenticated,)

    messageserializer=MessageSerializer
    searchdocument= MessageDocument

    def list(self, request):
        q=Q ('match_all')
        search = self.searchdocument.search().query(q)
        response=search.execute()

        results=self.paginate_queryset(response, request, view=self)
        serializer=self.messageserializer(results, many=True)
        baselogger.warning("LOGGER WORKS")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description')
        }
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            message_doc = MessageDocument(
                name=serializer.validated_data['name'],
                description=serializer.validated_data['description']
            )
            message_doc.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def retrieve(self, request, message_name=None):
        q = Q('match', name=message_name)
        search = self.searchdocument.search().query(q)
        response = search.execute()

        if response.hits.total.value == 0:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

        result = response.hits.hits[0]
        serializer = self.messageserializer(result['_source'])

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, message_name=None):
        q = Q('match', name=message_name)
        search = self.searchdocument.search().query(q)
        response = search.execute()

        if response.hits.total.value == 0:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

        doc_id = response.hits.hits[0]['_id']
        data = request.data
        serializer = self.messageserializer(data=data)
        if serializer.is_valid():
            serialized_data = serializer.validated_data
            update_doc = self.searchdocument(meta={'id': doc_id}, **serialized_data)
            update_doc.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, message_name):
        q = Q('match', name=message_name)
        search = self.searchdocument.search().query(q)

        count = search.count()
        if count == 0:
            return Response({'res': 'No message found!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            search.delete()
            return Response({'res': f'{count} message(s) deleted!'}, status=status.HTTP_200_OK)


 