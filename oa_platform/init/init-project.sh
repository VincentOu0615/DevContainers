#!/bin/bash
set -e # 遇到错误立即退出

log() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] $1"
}

# 修改数据库等待逻辑
wait_for_db() {
  log "等待数据库就绪..."
  local count=0
  until PGPASSWORD=oa_pass psql -h host.docker.internal -U oa_admin -d oa_system -c '\q'; do
    ((count++))
    if [ $count -gt 30 ]; then
      log "数据库连接超时！" >&2
      exit 1
    fi
    log "尝试数据库连接(${count}/30)..."
    sleep 2
  done
  log "数据库已就绪！"
}

# 初始化后端项目
init_backend() {
  cd /workspace/backend
  if [ ! -d "oa-system" ]; then
    log "初始化Spring Boot项目..."
    mvn -B archetype:generate \
      -DgroupId=com.oa.platform \
      -DartifactId=oa-system \
      -DarchetypeArtifactId=maven-archetype-quickstart \
      -DinteractiveMode=false
    
    # log "配置POM文件..."
#     cat <<EOF > oa-system/pom.xml
# <?xml version="1.0" encoding="UTF-8"?>
# <project xmlns="http://maven.apache.org/POM/4.0.0"
#          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#          xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
#     <modelVersion>4.0.0</modelVersion>

#     <parent>
#         <groupId>org.springframework.boot</groupId>
#         <artifactId>spring-boot-starter-parent</artifactId>
#         <version>3.1.0</version>
#     </parent>

#     <groupId>com.oa.platform</groupId>
#     <artifactId>oa-system</artifactId>
#     <version>1.0.0</version>

#     <properties>
#         <java.version>17</java.version>
#     </properties>

#     <dependencies>
#         <dependency>
#             <groupId>org.springframework.boot</groupId>
#             <artifactId>spring-boot-starter-web</artifactId>
#         </dependency>
#         <dependency>
#             <groupId>org.springframework.boot</groupId>
#             <artifactId>spring-boot-starter-data-jpa</artifactId>
#         </dependency>
#     </dependencies>
# </project>
# EOF
  fi

  log "后端初始化完成！"

}

init_frontend() {
  cd /workspace/frontend
  if [ ! -d "oa-admin" ]; then
    echo "创建Vue项目..."
    npm create vue@latest oa-admin -- --typescript --vue-router --pinia --eslint-with-prettier --force
    cd oa-admin && yarn install
  fi

  log "前端初始化完成！"
}

main() {
  wait_for_db
  init_backend
  init_frontend
}

main 2>&1 | tee /workspace/init.log