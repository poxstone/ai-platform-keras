# Execute Training
python -m trainer.task  --job-version ${MODEL_VERSION} --trainded-dir ${JOB_DIR} && \
git clone "${GIT_REPO}" "code_clone";
cd "code_clone";
git tag -a "${GIT_TAG}" -m "trained";
git push origin "${GIT_TAG}";