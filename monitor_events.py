from kubernetes import client, config, watch

def list_pods(api_client):
    v1 = client.CoreV1Api(api_client=api_client)
    pods = v1.list_pod_for_all_namespaces(watch=False)
    for pod in pods.items:
        print(f"📌 Pod: {pod.metadata.name} | Namespace: {pod.metadata.namespace} | Status: {pod.status.phase}")

def watch_pods(api_client):
    v1 = client.CoreV1Api(api_client=api_client)
    w = watch.Watch()
    print("🔍 Đang giám sát các Pod trong cluster...")
    for event in w.stream(v1.list_pod_for_all_namespaces):
        pod = event["object"]
        print(f"📢 {event['type']} - Pod: {pod.metadata.name} | Namespace: {pod.metadata.namespace} | Status: {pod.status.phase}")

def main():
    try:
        configuration = client.Configuration()
        configuration.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
        configuration.verify_ssl = True
        
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as token_file:
            token = token_file.read().strip()
        
        configuration.api_key = {"authorization": "Bearer " + token}
        
        api_client = client.ApiClient(configuration)
        
        print("✅ Kết nối bằng Service Account trong cluster")
        list_pods(api_client)
        watch_pods(api_client)

    except Exception as e:
        print(f"❌ Lỗi khi kết nối Kubernetes API: {e}")

if __name__ == "__main__":
    main()
