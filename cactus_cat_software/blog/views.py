from django.db.models import F
from django.views.generic import DetailView, ListView

from .models import BlogPost


class BlogListView(ListView):
    """Display all published blog posts."""

    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 12

    def get_queryset(self):
        return (
            BlogPost.objects.filter(status="published")
            .order_by(F("published_date").desc(nulls_last=True), "-created")
        )


class BlogDetailView(DetailView):
    """Display individual blog post."""

    model = BlogPost
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return BlogPost.objects.filter(status="published")
