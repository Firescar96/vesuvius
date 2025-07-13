pnpm run build-only
docker build -t gcr.io/firescar96/vesuvius-website:current -f website-dockerfile .
docker push gcr.io/firescar96/vesuvius-website:current
kubectl get pods | grep vesuvius-website | awk '{print $1}' | xargs kubectl delete pod