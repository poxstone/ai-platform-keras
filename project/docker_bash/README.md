# Example simple docker proccess

- Create file and assign executable permissions:
```bash
# create file
touch entrypoint.sh;
# assign permissions
chmod +x entrypoint.sh;
```

```bash
GOOGLE_CLOUD_PROJECT="my-project-id";
R_VERSION="1.0";

# build
docker build -t "gcr.io/${GOOGLE_CLOUD_PROJECT}/r_script:${R_VERSION}" -f Dockerfile ./;
# run
docker run -it --rm --net host "gcr.io/${GOOGLE_CLOUD_PROJECT}/r_script:${R_VERSION}";
```
