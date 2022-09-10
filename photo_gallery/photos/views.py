from django.views.generic import DetailView, ListView
from .models import Photo


class HomepageView(ListView):
    model = Photo
    # Exclude unpublished photos from photo list
    # Order by featured (featured at start) then by descending date (most recent earlier)
    queryset = Photo.objects.filter(published=True).order_by('-featured', '-date_taken')
    # TODO: implement pagination


class PhotoDetailView(DetailView):
    model = Photo
    # Return a 404 if the photo isn't published
    queryset = Photo.objects.filter(published=True)
