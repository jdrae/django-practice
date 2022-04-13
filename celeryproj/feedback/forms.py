from django import forms
from .tasks import send_feedback_email_task

class FeedbackForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    message = forms.CharField(
        label="Message", widget=forms.Textarea(attrs={'rows': 5})
    )
    honeypot = forms.CharField(widget=forms.HiddenInput(), required=False)

    def send_email(self):
        # hidden input 이라 일반 사용자는 모르는데 스팸은 자동으로 인풋을 채움
        if self.cleaned_data['honeypot']:
            return False
        # 유저가 사이트를 계속 이용하는 동안,
        # 비동기적으로 이메일 전송 작업을 진행함(백그라운드에서)
        send_feedback_email_task.delay(
            self.cleaned_data['email'], self.cleaned_data['message']
        )