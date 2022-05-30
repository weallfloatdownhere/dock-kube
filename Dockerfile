FROM python:3.8-slim as baseline
RUN apt -y update
RUN mkdir -p /usr/share/bin /root/.ssh
RUN apt -y install git curl openssl openssh-client sshpass apache2-utils
WORKDIR /bin
RUN curl -L --silent https://github.com/rancher/rke/releases/download/v1.3.11/rke_linux-amd64 -o /bin/rke && chmod +x /bin/rke
RUN curl -L --silent https://dl.k8s.io/release/v1.24.0/bin/linux/amd64/kubectl -o /bin/kubectl && chmod +x /bin/kubectl
RUN curl -L --silent https://github.com/mikefarah/yq/releases/download/v4.25.2/yq_linux_amd64 -o /bin/yq && chmod +x /bin/yq
RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
RUN helm plugin install https://github.com/databus23/helm-diff

RUN git config --global user.name "Gitops installer"
RUN git config --global user.email "gitops@noreply.local"

FROM baseline as compiler
ENV PYTHONUNBUFFERED 1
RUN apt -y install python3-dev gcc
RUN python3 -m pip install --upgrade pip

RUN pip3 install setuptools==62.1.0
RUN pip3 install wheel==0.37.1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --no-cache-dir --no-cache netaddr==0.8.0
RUN pip3 install --no-cache-dir --no-cache cryptography==36.0.2
RUN pip3 install --no-cache-dir --no-cache ansible-core==2.12.3
RUN pip3 install --no-cache-dir --no-cache netaddr==0.8.0
RUN pip3 install --no-cache-dir --no-cache PyYAML==6.0
RUN pip3 install --no-cache-dir --no-cache kubernetes==21.7.0
RUN pip3 install --no-cache-dir --no-cache dnspython3==1.15.0
RUN pip3 install --no-cache-dir --no-cache jsonpatch==1.32

RUN ansible-galaxy collection install ansible.netcommon -p /root/ansible_collections
RUN ansible-galaxy collection install ansible.utils -p /root/ansible_collections
RUN ansible-galaxy collection install ansible.posix -p /root/ansible_collections
RUN ansible-galaxy collection install community.crypto -p /root/ansible_collections
RUN ansible-galaxy collection install community.general -p /root/ansible_collections
RUN ansible-galaxy collection install kubernetes.core -p /root/ansible_collections

FROM baseline as finale
WORKDIR /root
ENV VIRTUAL_ENV=/opt/venv
COPY --from=compiler $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=compiler /root/ansible_collections /root/.ansible/collections/ansible_collections
COPY ./ansible/ansible.cfg /etc/ansible/ansible.cfg
COPY ./ansible /usr/share/bin/ansible
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENTRYPOINT ["python3", "/usr/share/bin/ansible/entrypoint.py"]
