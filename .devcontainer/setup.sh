#!/bin/bash
set -eo pipefail

log() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] $1"
}

check_network() {
    log "=== 开始网络连通性验证 ==="
    
    # 测试PostgreSQL容器连通性
    if ping -c 3 $DB_HOST &>/dev/null; then
        log "[成功] 网络能访问PostgreSQL容器(postgres)"
    else
        log "[失败] 无法访问PostgreSQL容器" >&2
        return 1
    fi

    # 测试Redis容器连通性
    if ping -c 3 $REDIS_HOST &>/dev/null; then
        log "[成功] 网络能访问Redis容器(redis)"
    else
        log "[失败] 无法访问Redis容器" >&2
        return 1
    fi
}

check_database() {
    log "=== 开始数据库连接验证 ==="
    local max_retries=10
    local count=0

    # PostgreSQL连接测试
    while ! PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c '\q' &>/dev/null; do
        ((count++))
        if [ $count -gt $max_retries ]; then
            log "[错误] PostgreSQL连接失败超过${max_retries}次" >&2
            return 1
        fi
        log "[重试] 正在尝试连接PostgreSQL (${count}/${max_retries})..."
        sleep 2
    done
    log "[成功] PostgreSQL数据库连接正常"

    # Redis连接测试
    if ! redis-cli -h $REDIS_HOST ping | grep -q PONG; then
        log "[错误] Redis连接失败" >&2
        return 1
    fi
    log "[成功] Redis连接正常"
}

main() {
    log "===== 开始环境验证 ====="
    check_network
    check_database
    log "===== 所有检查通过 ====="
}


main