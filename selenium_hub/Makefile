K8S_DIR = k8s
NAMESPACE = selenium-grid

run:
	kubectl apply -f $(K8S_DIR)/namespace.yml
	kubectl apply -f $(K8S_DIR)/hub.yml
	kubectl apply -f $(K8S_DIR)/node.yml

destroy:
	kubectl delete -f $(K8S_DIR)/

list_svc:
	kubectl get svc -n $(NAMESPACE)

list_rc:
	kubectl get replicaset -n $(NAMESPACE)

list_dep:
	kubectl get deployment -n $(NAMESPACE)


list_pods:
	kubectl get pods -n $(NAMESPACE)

list_nodes:
	kubectl get nodes
logs:
	kubectl logs -n $(NAMESPACE) $(POD) -f
watch_logs:
	watch kubectl logs $(POD) -n $(NAMESPACE)
exec:
	kubectl exec -it $(POD) -n $(NAMESPACE) -- /bin/bash
forward_port:
	kubectl port-forward -n selenium-grid svc/selenium-hub 4444:4444