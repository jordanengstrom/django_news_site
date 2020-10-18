from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from newsapi.news.models import Article
from newsapi.news.api.serializers import ArticleSerializer


# Function based view
@api_view(['GET', 'POST'])
def article_list_create_api_view(request):
    if request.method == 'GET':
        articles = Article.objects.filter(active=True)
        serializer = Article(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Article(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=
                            status.HTTP_400_BAD_REQUEST)


# Function based view
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail_api_view(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response({'error': {
                                    'code': 404,
                                    'message': 'Article not found!',
                                   }
                         }, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = Article(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Article(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
