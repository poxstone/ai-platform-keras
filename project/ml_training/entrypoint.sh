# Execute Training
python -m trainer.task  --job-version "${MODEL_VERSION}" --trainded-dir "${JOB_DIR}";

## git add tag to trigger
#git clone "${GIT_REPO}" "code_clone";
#cd "code_clone";
#git tag -d "${GIT_TAGNAME}";
#git push -d origin "${GIT_TAGNAME}";
#git tag -a "${GIT_TAGNAME}" "${GIT_COMMIT}" -m "";
#git push origin "${GIT_TAGNAME}";
#
## publish image
#gcloud ai-platform versions create "${MODEL_NAME}${MODEL_VERSION}" --project "${GOOGLE_CLOUD_PROJECT}" \
#  --model "${MODEL_NAME}" \
#  --framework "tensorflow" \
#  --origin "${JOB_DIR}/${MODEL_NAME}/${MODEL_VERSION}/" \
#  --runtime-version "2.1" \
#  --python-version "3.7" \
#  --quite;
#