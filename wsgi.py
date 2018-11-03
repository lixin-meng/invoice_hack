import api.app as app
#
# https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app
#
# gunicorn -c env/gunicorn_config.py --chdir /project/hack wsgi:app.app
#
# if __name__ == "__main__":
#     app.run()
#
#
# ------------------------------------!!!!!---------------------------------------------
# Even though this looks like an empty file. DO NOT DELETE this without changing the
# entry point of the container image
# ------------------------------------!!!!!---------------------------------------------
#