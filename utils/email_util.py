import smtplib
import logging
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] (%(name)s) %(message)s')
log = logging.getLogger(__name__)

GODADDY_SMTP = 'smtpout.secureserver.net'
TO_LIST = ['tcheng@cincoai.com']


def send_feedback_email(to_list, sender, subject, content):
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = sender
    recipients = ','.join(to for to in to_list)
    msg['To'] = recipients
    flag = True
    try:
        smtp = smtplib.SMTP(GODADDY_SMTP)
        smtp.sendmail(sender, recipients, msg.as_string())
    except Exception as e:
        log.exception(e)
        flag = False
    finally:
        smtp.quit()
    return flag