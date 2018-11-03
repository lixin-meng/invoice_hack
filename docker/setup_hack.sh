[[ -d cfd_deployment ]] || mkdir -p /project

chmod +x /entry_point.sh  && \
  cd /project && \
  tar -xzvf ../hack.tar.gz && rm -rf ../hack.tar.gz   && \
  chown -R cfd:cfd /project && \
  cd /project/hack && \
  /opt/conda/bin/conda shell.posix activate chat_flow && \
  export PATH=/opt/conda/envs/chat_flow/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/root/.local/bin:/root/bin && \
  export PYTHONPATH=/opt/conda/env/chat_flow/lib/python3.6/site-packages
  export PYTHON_PATH=/opt/conda/env/chat_flow/lib/python3.6/site-packages
  export CONDA_PYTHON_EXE=/opt/conda/envs/chat_flow/bin/python && \
  export CONDA_PREFIX=/opt/conda/envs/chat_flow && \
  export CONDA_DEFAULT_ENV=chat_flow && \
  export CONDA_EXE=/opt/conda/bin/conda && \
  export CONDA_SHLVL=1




