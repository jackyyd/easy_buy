from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPage(PageNumberPagination):
    page_query_param = 'page'  # ?page=1
    page_size_query_param = 'pagesize'
    max_page_size = 10
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'counts': self.page.paginator.count,  # 总数
            'lists': data,  # 查询集分页的子集(当前页数据)
            'page': self.page.number,  # 页码
            'pages': self.page.paginator.num_pages,  # 总页数
            'pagesize': self.page_size  # 页容量
        })
