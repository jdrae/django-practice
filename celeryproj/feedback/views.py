from django.views.generic import FormView

from .forms import FeedbackForm


class FeedbackView(FormView):
    template_name = 'feedback/index.html'
    form_class = FeedbackForm
    success_url = '/photo'

    def form_valid(self, form):
        form.send_email()
        return super(FeedbackView, self).form_valid(form)
