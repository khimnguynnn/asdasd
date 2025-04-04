import smtplib
from kubernetes import client, config, watch
from kubernetes.client import ApiException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

logging.basicConfig(level=logging.DEBUG)

def get_smtp_config():
    """Lấy thông tin SMTP từ ConfigMap trong Kubernetes hoặc từ biến môi trường."""
    v1 = client.CoreV1Api()
    try:
        config_map = v1.read_namespaced_config_map("smtp-config", "kube-system")
        smtp_config = {
            "SMTP_SERVER": config_map.data["SMTP_SERVER"],
            "SMTP_PORT": config_map.data["SMTP_PORT"],
            "SMTP_USER": config_map.data["SMTP_USER"],
            "SMTP_PASSWORD": config_map.data["SMTP_PASSWORD"],
            "FROM_EMAIL": config_map.data["FROM_EMAIL"],
            "TO_EMAIL": config_map.data["TO_EMAIL"].split(",")
        }
        return smtp_config
    except ApiException as e:
        print(f"❌ Lỗi khi lấy ConfigMap: {e}")
        return None

def send_email(subject, body, smtp_config):
    """Gửi email thông qua SMTP server lấy từ ConfigMap."""
    try:
        msg = MIMEMultipart()
        from_email = smtp_config["FROM_EMAIL"]
        msg['From'] = from_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        to_email_list = smtp_config["TO_EMAIL"]
        msg['To'] = ", ".join(to_email_list)

        server = smtplib.SMTP(smtp_config["SMTP_SERVER"], smtp_config["SMTP_PORT"])
        server.starttls()
        server.login(smtp_config["SMTP_USER"], smtp_config["SMTP_PASSWORD"])
        text = msg.as_string()
        server.sendmail(from_email, to_email_list, text)
        server.quit()

        print("✅ Email đã được gửi thành công!")

    except Exception as e:
        print(f"❌ Lỗi khi gửi email: {e}")

def list_pods():
    """Liệt kê tất cả các Pod trong namespace 'grn'"""
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace='grn', watch=False)
    for pod in pods.items:
        print(f"📌 Pod: {pod.metadata.name} | Namespace: {pod.metadata.namespace} | Status: {pod.status.phase}")

def watch_pods():
    """Lắng nghe sự kiện Pod trong namespace 'grn'"""
    v1 = client.CoreV1Api()
    w = watch.Watch()
    print("🔍 Đang giám sát các Pod trong namespace 'grn'...")
    
    smtp_config = get_smtp_config()
    if not smtp_config:
        print("❌ Không thể lấy thông tin SMTP từ ConfigMap. Dừng chương trình.")
        return

    for event in w.stream(v1.list_namespaced_pod, namespace='grn'):
        pod = event["object"]
        event_type = event['type']
        
        if event_type in ['ADDED', 'DELETED']:
            subject = f"Pod Event: {event_type}"
            body = f"Pod: {pod.metadata.name}\nNamespace: {pod.metadata.namespace}\nStatus: {pod.status.phase}\nEvent: {event_type}"
            
            send_email(subject, body, smtp_config)

def main():
    try:
        try:
            config.load_incluster_config()
            print("✅ Kết nối bằng Service Account trong cluster")
        except config.ConfigException:
            config.load_kube_config()
            print("✅ Kết nối bằng kubeconfig")

        list_pods()
        watch_pods()

    except Exception as e:
        print(f"❌ Lỗi khi kết nối Kubernetes API: {e}")

if __name__ == "__main__":
    main()
