import asyncio
import json

from kubernetes_asyncio import client, config, watch


async def monitor(crds):
    print("Watching for changes in instances.k8s.truebrain.nl for namespace 'default'")
    stream = watch.Watch().stream(crds.list_namespaced_custom_object,
                                  "k8s.truebrain.nl",
                                  "v1",
                                  "default",
                                  "instances",
                                  _request_timeout=30)
    async for event in stream:
        del event["raw_object"]
        print(json.dumps(event, indent=4))


async def main():
    try:
        config.load_incluster_config()
    except Exception:
        await config.load_kube_config()
    crds = client.CustomObjectsApi()

    await monitor(crds)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
