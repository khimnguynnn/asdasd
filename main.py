import os
import smtplib
from kubernetes import client, config, watch
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_host = os.getenv('SMTP_HOST')
smtp_port = int(os.getenv('SMTP_PORT'))
username = os.getenv('SMTP_USERNAME')
password = os.getenv('SMTP_PASSWORD')

from_email = os.getenv('FROM_EMAIL')
to_emails = os.getenv('TO_EMAILS').split(',')

def send_email(message):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['Subject'] = 'K8s Pod Scale Event Notification'
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # Bật mã hóa TLS
        server.login(username, password)

        for to_email in to_emails:
            msg['To'] = to_email
            server.sendmail(from_email, to_email, msg.as_string())
            print(f"Email sent successfully to {to_email}!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

def monitor_k8s_events():
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    w = watch.Watch()

    for event in w.stream(v1.list_namespaced_event, namespace='grn'):
        if 'scale' in event['message'].lower():
            message = f"Event Type: {event['type']}\nEvent Message: {event['message']}\nPod: {event['involvedObject']['name']}"
            print(f"Detected scale event: {message}")
            send_email(message)

if __name__ == '__main__':
    monitor_k8s_events()
