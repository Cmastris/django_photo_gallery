from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Collection, Photo


class PhotoListView(ListView):
    model = Photo
    paginate_by = 6  # Display 6 photos per page
    homepage = False
    collection = False
    search = False

    def get_filtered_photos(self):
        """Return a filtered Photo queryset, depending on the page type.
        https://docs.djangoproject.com/en/4.0/ref/models/querysets/
        """
        if self.homepage:
            return Photo.objects.filter(published=True)
        else:
            collection = get_object_or_404(Collection, slug=self.kwargs['collection_slug'])
            if not collection.published:
                raise Http404()
            return Photo.objects.filter(published=True, collections__in=[collection])

    def get_sorted_photos(self, qs):
        """Sort and return a Photo queryset depending on the `sort` query string (if applicable).
        https://docs.djangoproject.com/en/4.0/ref/models/querysets/

        Args:
            qs (QuerySet): the (filtered) QuerySet to be sorted.
        """
        # Retrieve `sort` query string value, otherwise None
        sort = self.request.GET.get('sort')
        if sort == "new":
            # Order by descending date (most recent earlier)
            return qs.order_by('-date_taken')

        elif sort == "old":
            # Order by ascending date (oldest earlier)
            return qs.order_by('date_taken')

        # Order by featured (featured at start) then by descending date (most recent earlier)
        return qs.order_by('-featured', '-date_taken')

    def get_queryset(self):
        filtered_qs = self.get_filtered_photos()
        return self.get_sorted_photos(filtered_qs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_homepage'] = self.homepage
        context['is_collection'] = self.collection
        context['is_search'] = self.search
        context['sorting'] = self.request.GET.get('sort', 'default')

        if self.collection:
            context['collection'] = get_object_or_404(Collection,
                                                      slug=self.kwargs['collection_slug'])

        return context


class SearchView(PhotoListView):
    search = True

    def get_filtered_photos(self):
        """Return a filtered queryset of Photos whose primary content includes the search query.
        https://docs.djangoproject.com/en/4.0/ref/models/querysets/
        """
        query = self.request.GET.get('query', None)
        if query is not None:
            # https://docs.djangoproject.com/en/4.0/topics/db/queries/#complex-lookups-with-q-objects
            lookup = Q(title__icontains=query) | \
                     Q(description__icontains=query) | \
                     Q(location__icontains=query)

            return Photo.objects.filter(lookup)

        return Photo.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('query', '')
        return context


class PhotoDetailView(DetailView):
    model = Photo
    # Return a 404 if the photo isn't published
    queryset = Photo.objects.filter(published=True)
