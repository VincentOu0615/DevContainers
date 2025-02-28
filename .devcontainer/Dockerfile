FROM mcr.microsoft.com/devcontainers/base:bullseye

# 安装实用工具
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    git

# 安装网络测试工具
RUN apt-get update && \
    apt-get install --fix-missing && \
    apt-get install -y --no-install-recommends \
    iputils-ping 

# 安装Java环境
RUN apt-get update && \
    apt-get install --fix-missing && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    maven \
    postgresql-client \
    redis-tools

# 安装Node.js环境
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g yarn

# 配置开发环境
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> /etc/bash.bashrc && \
    echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> /etc/bash.bashrc

# 清理缓存
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制 app.py 到容器的 /app 目录
COPY setup.sh .

# 定义启动命令
CMD ["bash", "/app/setup.sh"]