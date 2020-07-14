# Example simple docker proccess

- Create file and assign executable permissions:
```bash
# create file
touch entrypoint.sh;
# assign permissions
chmod +x entrypoint.sh;
```

```bash
PROJECT_ID="my-project-id";
R_VERSION="1.0";

# build
docker build -t "gcr.io/${PROJECT_ID}/r_script:${R_VERSION}" -f Dockerfile ./;
# run
docker run -it --rm --net host "gcr.io/${PROJECT_ID}/r_script:${R_VERSION}";
```
