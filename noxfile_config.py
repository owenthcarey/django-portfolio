# Default TEST_CONFIG_OVERRIDE for python repos.

# You can copy this file into your directory, then it will be imported from
# the noxfile.py.

# The source of truth:
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/noxfile_config.py

TEST_CONFIG_OVERRIDE = {
    # You can opt out from the test for specific Python versions.
    "ignored_versions": ["2.7", "3.6", "3.7", "3.8"],
    # Old samples are opted out of enforcing Python type hints
    # All new samples should feature the
    "enforce_type_hints": True,
    # An envvar key for determining the project id to use. Change it
    # to 'BUILD_SPECIFIC_GCLOUD_PROJECT' if you want to opt in using a
    # build specific Cloud project. You can also use your own string
    # to use your own Cloud project.
    "gcloud_project_env": "GOOGLE_CLOUD_PROJECT",
    # 'gcloud_project_env': 'BUILD_SPECIFIC_GCLOUD_PROJECT',
    # A dictionary you want to inject into your test. Don't put any
    # secrets here. These values will override predefined values.
    "envs": {"DJANGO_SETTINGS_MODULE": "mysite.settings"},
}
