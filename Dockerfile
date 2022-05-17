FROM python:3.8-slim as baseline
RUN apt -y update
RUN apt -y install git curl python3-dev gcc openssl openssh-client

RUN apt -y upgrade
RUN python3 -m pip install --upgrade pip

RUN curl -L --silent https://github.com/rancher/rke/releases/download/v1.3.11/rke_linux-amd64 -o /bin/rke && chmod +x /bin/rke
RUN curl -L --silent https://dl.k8s.io/release/v1.24.0/bin/linux/amd64/kubectl -o /bin/kubectl && chmod +x /bin/kubectl

RUN pip3 install --no-cache-dir --no-cache setuptools==62.1.0
RUN pip3 install --no-cache-dir --no-cache wheel==0.37.1
RUN pip3 install --no-cache-dir --no-cache netaddr==0.8.0
RUN pip3 install --no-cache-dir --no-cache cryptography==36.0.2
RUN pip3 install --no-cache-dir --no-cache ansible-core==2.12.3
RUN pip3 install --no-cache-dir --no-cache paramiko==2.9.2
RUN pip3 install --no-cache-dir --no-cache netaddr==0.8.0
RUN pip3 install --no-cache-dir --no-cache PyYAML==6.0
RUN pip3 install --no-cache-dir --no-cache kubernetes==21.7.0
RUN pip3 install --no-cache-dir --no-cache dnspython3==1.15.0
RUN pip3 install --no-cache-dir --no-cache jsonpatch==1.32
RUN pip3 install --no-cache-dir --no-cache click==8.1.3

RUN ansible-galaxy collection install ansible.netcommon
RUN ansible-galaxy collection install ansible.utils
RUN ansible-galaxy collection install ansible.posix
RUN ansible-galaxy collection install community.crypto
RUN ansible-galaxy collection install community.general
RUN ansible-galaxy collection install kubernetes.core

RUN mkdir -p /usr/share/bin /mounted
COPY ./ansible /usr/share/bin/ansible

CMD ["ansible-playbook"]