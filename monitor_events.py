from kubernetes import client, config, watch

configuration = client.Configuration()
configuration.verify_ssl = False

def main():
    config.load_incluster_config()

    v1 = client.CoreV1Api()
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
    except KeyboardInterrupt:
        print("\nDừng theo dõi.")
    finally:
        w.stop()

if __name__ == '__main__':
    main()
