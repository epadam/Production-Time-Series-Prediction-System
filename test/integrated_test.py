import numpy as np

from seldon_core.seldon_client import SeldonClient

url = !kubectl get svc ambassador -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

sc = SeldonClient(
    gateway="ambassador",
    gateway_endpoint="localhost:80",
    deployment_name="mlops-server",
    payload_type="ndarray",
    namespace="jx-staging",
    transport="rest",
)

response = sc.predict(data=np.array([twenty_test.data[0]]))

response.response.data
