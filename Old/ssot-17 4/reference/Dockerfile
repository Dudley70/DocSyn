FROM mcr.microsoft.com/devcontainers/base:bookworm
RUN useradd -m vscode &&     apt-get update && apt-get install -y --no-install-recommends python3 python3-pip make git &&     rm -rf /var/lib/apt/lists/*
USER vscode
WORKDIR /workspaces/ssot-5
