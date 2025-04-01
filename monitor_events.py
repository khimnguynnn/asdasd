from kubernetes import client, config
from kubernetes.client.rest import ApiException
from urllib3.exceptions import InsecureRequestWarning

def list_pods():

    v1 = client.CoreV1Api()
    try:
        pods = v1.list_pod_for_all_namespaces(watch=False)
        for pod in pods.items:
            print(f"📌 Pod: {pod.metadata.name} | Namespace: {pod.metadata.namespace} | Status: {pod.status.phase}")
    except ApiException as e:
        print(f"❌ Lỗi khi lấy danh sách Pod: {e}")

def main():
    try:
        config.load_incluster_config()
        list_pods()
    except Exception as e:
        print(f"❌ Lỗi khi kết nối Kubernetes API: {e}")

if __name__ == "__main__":
    main()
