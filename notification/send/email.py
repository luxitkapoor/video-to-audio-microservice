import smtplib, os
from email.message import EmailMessage
import json
def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        