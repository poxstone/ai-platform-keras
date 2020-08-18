# Execute Training
python -m trainer.task  --job-version ${MODEL_VERSION} --trainded-dir ${JOB_DIR} && \
# git add tag to trigger
git clone "${GIT_REPO}" "code_clone";
cd "code_clone";
git tag -d "${GIT_TAGNAME}";
git push -d origin "${GIT_TAGNAME}";
git tag -a "${GIT_TAGNAME}" "${GIT_COMMIT}" -m "";
git push origin "${GIT_TAGNAME}";
