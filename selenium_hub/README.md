# Selenium Nodes On Kubernetes:

**Hub Settings:**

- Configure as per need:

[Node Configuration](./k8s/node.yml)

```yaml
      containers:
      - name: selenium-node-chrome
        image: selenium/node-firefox:4.33.0-20250525
        env:
        ...
        ...
        - name: SE_NODE_MAX_SESSIONS
          value: "2" # max num of sessions
```

**Note that processing a single request requires:**
- In headless alteast: => 1GB ram, 0.8CPU 
- This also depends on weather a firefox or chrome.
- Make sure to modify resource section

```yaml
        resources:
          requests:
            cpu: "1"
            memory: "1Gi"
          limits:
            cpu: "2"
            memory: "3Gi"
```

> Hub accessible on URL: ``http://localhost:4444/wd/hub`` if using locally.



## Commands:

- Run: ``make run``
- Expose hub on localhost: ``make forward_port``
- Stop hub: ``make stop_hub``


For other commands refer: [Makefile](./Makefile)
