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

    def get_queryset(self):
        if self.search:
            query = self.request.GET.get('query', None)
            if query:
                # https://docs.djangoproject.com/en/4.0/topics/db/queries/#complex-lookups-with-q-objects
                lookup = Q(title__icontains=query) | \
                         Q(description__icontains=query) | \
                         Q(location__icontains=query)

                filtered_qs = Photo.objects.filter(lookup)

            else:
                filtered_qs = Photo.objects.filter(published=True)

        elif self.homepage:
            filtered_qs = Photo.objects.filter(published=True)

        else:
            collection = get_object_or_404(Collection, slug=self.kwargs['collection_slug'])
            if not collection.published:
                raise Http404()
            filtered_qs = Photo.objects.filter(published=True, collections__in=[collection])

        # Retrieve `sort` query string value, otherwise None
        sort = self.request.GET.get('sort')
        if sort == "new":
            # Order by descending date (most recent earlier)
            return filtered_qs.order_by('-date_taken')

        elif sort == "old":
            # Order by ascending date (oldest earlier)
            return filtered_qs.order_by('date_taken')

        # Order by featured (featured at start) then by descending date (most recent earlier)
        return filtered_qs.order_by('-featured', '-date_taken')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_homepage'] = self.homepage
        context['is_collection'] = self.collection
        context['is_search'] = self.search

        if self.search:
            context['search_query'] = self.request.GET.get('query', '')
            return context

        if self.collection:
            context['collection'] = get_object_or_404(Collection,
                                                      slug=self.kwargs['collection_slug'])

        context['sorting'] = self.request.GET.get('sort', 'default')
        return context


class PhotoDetailView(DetailView):
    model = Photo
    # Return a 404 if the photo isn't published
    queryset = Photo.objects.filter(published=True)
