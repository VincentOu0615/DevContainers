# OA 云办公平台开发环境

## 项目概述
基于Dev Containers的标准化开发环境，提供以下核心服务：

```yaml
app:
  image: ${DEVCONTAINER_NAME}:latest
```

## 目录结构
```bash
│   ├── .devcontainer/
│   ├── backend/
│       ├── oa-system/
│       │   ├── src/
│   ├── database/
│   │   ├── postgres/
│   │   │   ├── data/
│   │       ├── init/
│   │   ├── redis/
│   │       ├── data/
│   ├── frontend/
│   ├── init/
│   ├── scripts/
```

## 核心环境变量
| 变量名 | 默认值 | 描述 |
|--------|--------|------|
| DB_HOST |  | 暂无描述 |
| DB_NAME |  | 暂无描述 |
| DB_PASSWORD |  | 暂无描述 |
| DB_USER |  | 暂无描述 |
| DEVCONTAINER_NAME |  | 暂无描述 |
| REDIS_HOST |  | 暂无描述 |

## 快速开始
```bash
# 初始化开发环境
./scripts/init-project.sh

# 验证环境
./scripts/validate_env.sh
```

## 版本信息
- 生成时间: 2025-02-28 18:16:26
- 环境版本: 64d137c