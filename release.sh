cd website
NODE_ENV='production'; pnpm run build-only
docker build -t gcr.io/firescar96/vesuvius-website:current -f website-dockerfile .
docker push gcr.io/firescar96/vesuvius-website:current
kubectl get pods | grep vesuvius-website | awk '{print $1}' | xargs kubectl delete pod

cd ../backend
docker build -t gcr.io/firescar96/vesuvius-backend:current -f backend-dockerfile .
docker push gcr.io/firescar96/vesuvius-backend:current
kubectl get pods | grep vesuvius-backend | awk '{print $1}' | xargs kubectl delete pod