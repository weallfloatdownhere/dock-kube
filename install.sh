#!/bin bash

IMAGE_NAME="silentreatmen7/dock-kube:dev"

mkdir -p ~/.local/bin

cat << EOF > ~/.local/bin/dockube
#!/bin/bash
docker run -it -v "$(pwd)/:/root/rke/" "$(IMAGE_NAME)" $@
EOF

chmod +x ~/.local/bin/dockube
