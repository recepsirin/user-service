from rest_framework import pagination, response


class Pagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 100

    def paginate(self, data):
        return response.Response({
            'pagination': {
                'total': self.page.paginator.count,
                'per_page': self.get_page_size(self.request),
                'page': self.request.query_params.get('page', None),
                'prev':  self.get_previous_link(),
                'next': self.get_next_link(),
            },
            'data': data
        })