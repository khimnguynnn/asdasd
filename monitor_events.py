from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    # Load cấu hình từ trong Pod
    config.load_incluster_config()
    
    # Tạo API Client bỏ qua xác thực SSL
    configuration = client.Configuration()
    configuration.verify_ssl = False
    api_client = client.ApiClient(configuration)
    v1 = client.CoreV1Api(api_client=api_client)
    w = watch.Watch()

    print("Đang theo dõi các sự kiện trên toàn bộ cluster...")

    try:
        for event in w.stream(v1.list_event_for_all_namespaces):
            print(f"\nType: {event['type']}")
            print(f"Namespace: {event['object'].metadata.namespace}")
            print(f"Name: {event['object'].metadata.name}")
            print(f"Reason: {event['object'].reason}")
            print(f"Message: {event['object'].message}")
            print(f"Timestamp: {event['object'].last_timestamp}")
    except ApiException as e:
        print(f"Exception when calling Kubernetes API: {e}")
    except KeyboardInterrupt:
        print("\nDừng theo dõi.")
    finally:
        w.stop()

if __name__ == '__main__':
    main()
