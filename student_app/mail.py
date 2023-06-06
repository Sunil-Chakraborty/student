
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile

def send_email_with_attachment(request):
    
    email_subject = 'Email with attachment'
    email_body = 'Please find the attachment'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['to.sunilc59@gmail.com', 'to.sunilc@gmail.com']
    file = request.FILES['file']
    temporary_file = TemporaryUploadedFile(file.name, file.content_type, file.size, file.charset, file.content_type_extra)
    temporary_file.write(file.read())

    email = EmailMessage(email_subject, email_body, from_email, recipient_list)
    #email.attach_file('/path/to/file.pdf')
    email.attach(temporary_file.name, temporary_file.read(), temporary_file.content_type)

    #email.attach_file('/personal/seq_question.docx')
    email.send()

