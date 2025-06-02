# Selenium Nodes On Kubernetes:

Hub With 5 replicas of chrome node.

**Hub Settings:**

```text
SE_EVENT_BUS_PUBLISH_PORT => "4442"
SE_EVENT_BUS_SUBSCRIBE_PORT => "4443"
```

Hub accessible on port: ``4444``



**Nodes:**
```
SE_NODE_MAX_SESSIONS / Concurrency => 8
```

Each Node can handle 8 requests concurrently.


## Commands:

- Run: ``make run``
- Get Port on Local: ``make forward_port``

For other commands refer: [Makefile](./Makefile)
