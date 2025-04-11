# # students/nfc_utils.py

# import nfc
# from django.http import HttpResponse

# def write_nfc_url(student):
#     # Construct the NFC URL for the student profile
#     student_url = f"http://localhost:8000/profile/{student.id}/"

#     # Initialize NFC reader
#     clf = nfc.ContactlessFrontend('usb')  # Use 'usb' for USB NFC reader
#     if not clf:
#         return None  # NFC reader not connected

#     try:
#         def connected(tag):
#             tag.ndef.records = [nfc.ndef.UriRecord(student_url)]
#             return True

#         clf.connect(rdwr={'on-connect': connected})
#         clf.close()
#         return True
#     except Exception as e:
#         print(f"Error writing to NFC tag: {e}")
#         return False

# nfc_utils.py
# nfc_utils.py
import nfc

class NFCWriteError(Exception):
    pass

def write_nfc_url(student):
    student_url = f"http://localhost:8000/profile/{student.id}/"
    
    try:
        # Initialize NFC reader
        clf = nfc.ContactlessFrontend('usb')
        if not clf:
            raise NFCWriteError("NFC reader not connected.")  # NFC reader not connected

        # Write URL to NFC
        def connected(tag):
            tag.ndef.records = [nfc.ndef.UriRecord(student_url)]
            return True

        clf.connect(rdwr={'on-connect': connected})
        clf.close()
        return True
    except Exception as e:
        raise NFCWriteError(f"NFC write failed: {str(e)}")
