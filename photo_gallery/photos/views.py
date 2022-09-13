from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Collection, Photo


class PhotoListView(ListView):
    model = Photo
    paginate_by = 6  # Display 6 photos per page
    homepage = False

    def get_queryset(self):
        if self.homepage:
            filtered_qs = Photo.objects.filter(published=True)
        else:
            collection = get_object_or_404(Collection, slug=self.kwargs['collection_slug'])
            if not collection.published:
                raise Http404()
            filtered_qs = Photo.objects.filter(published=True, collections__in=[collection])

        # Order by featured (featured at start) then by descending date (most recent earlier)
        return filtered_qs.order_by('-featured', '-date_taken')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.homepage:
            context['collection'] = get_object_or_404(Collection,
                                                      slug=self.kwargs['collection_slug'])
        context['homepage'] = self.homepage
        return context


class PhotoDetailView(DetailView):
    model = Photo
    # Return a 404 if the photo isn't published
    queryset = Photo.objects.filter(published=True)
