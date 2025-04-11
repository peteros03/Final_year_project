import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ur_smart_student_cards.settings')
django.setup()

import nfc
from students.models import Student

def on_connect(tag):
    student_id = sys.argv[1]
    student = Student.objects.get(id=student_id)
    url = student.get_profile_url()
    tag.ndef.message = nfc.ndef.Message(nfc.ndef.UriRecord(url))
    print(f"Written to NFC card: {url}")
    return True

clf = nfc.ContactlessFrontend('usb')
print("Tap NFC card now...")
clf.connect(rdwr={'on-connect': on_connect})