"""
README生成工具（Windows兼容版）
"""

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
import yaml  # 需要安装PyYAML库

def main():
    # 基础配置
    base_dir = Path(__file__).parent.parent  # 假设脚本在scripts目录
    readme_path = base_dir / "README.md"
    
    # 初始化内容
    content = [
        "# OA 云办公平台开发环境",
        "",
        "## 项目概述",
        "基于Dev Containers的标准化开发环境，提供以下核心服务：",
        ""
    ]

    # 添加服务列表
    service_info = parse_docker_compose(base_dir / ".devcontainer" / "docker-compose.yml")
    content.extend(gen_service_section(service_info))

    # 添加目录结构
    content.extend([
        "",
        "## 目录结构",
        "```bash",
        *gen_directory_tree(base_dir, depth=3, excludes=[".git", "node_modules", "target"]),
        "```"
    ])

    # 添加环境变量表
    env_vars = parse_env_vars(
        base_dir / ".devcontainer" / "docker-compose.yml",
        base_dir / ".devcontainer" / "setup.sh"
    )
    content.extend(gen_env_table(env_vars))

    # 添加快速开始指南
    content.extend([
        "",
        "## 快速开始",
        "```bash",
        "# 初始化开发环境",
        "./scripts/init-project.sh",
        "",
        "# 验证环境",
        "./scripts/validate_env.sh",
        "```"
    ])

    # 添加版本信息
    content.extend(gen_version_section(base_dir))

    # 写入文件
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))
    print(f"README生成完成：{readme_path}")

def parse_docker_compose(compose_path: Path) -> dict:
    """解析docker-compose.yml获取服务信息"""
    if not compose_path.exists():
        return {}
    
    with open(compose_path, encoding="utf-8") as f:
        compose = yaml.safe_load(f)
    
    services = {}
    for name, config in compose.get("services", {}).items():
        services[name] = {
            "image": config.get("image", ""),
            "ports": config.get("ports", []),
            "env": [e for e in config.get("environment", []) if "=" in e]
        }
    return services

def gen_service_section(services: dict) -> list:
    """生成服务配置部分"""
    lines = ["```yaml"]
    for name, config in services.items():
        lines.append(f"{name}:")
        lines.append(f"  image: {config['image']}")
        if config["ports"]:
            lines.append(f"  ports: {config['ports']}")
        if config["env"]:
            lines.append("  environment:")
            for e in config["env"]:
                lines.append(f"    - {e}")
    lines.append("```")
    return lines

def gen_directory_tree(root: Path, depth: int, excludes: list) -> list:
    """生成目录树结构"""
    lines = []
    prefix = "│   "
    
    def walk_dir(path: Path, current_depth: int, pre: str = ""):
        if current_depth < 0:
            return
        name = path.name
        if name in excludes:
            return
        
        if path.is_dir():
            lines.append(f"{pre}├── {name}/")
            entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            for i, entry in enumerate(entries):
                is_last = i == len(entries) - 1
                walk_dir(
                    entry, 
                    current_depth - 1,
                    pre + (prefix if not is_last else "    ")
                )
    
    walk_dir(root, depth)
    return lines[1:]  # 跳过根目录显示

def parse_env_vars(*files: Path) -> dict:
    """从文件解析环境变量"""
    envs = {}
    pattern = re.compile(r"\${?(?P<var>[A-Z_]+)(:-(?P<default>[^}]+))?}?")
    
    for file in files:
        if not file.exists():
            continue
        with open(file, encoding="utf-8") as f:
            text = f.read()
            for match in pattern.finditer(text):
                var = match.group("var")
                default = match.group("default") or ""
                desc = re.search(fr"#\s*{var}:\s*(.+)$", text, re.M)
                envs[var] = {
                    "default": default,
                    "description": desc.group(1) if desc else "暂无描述"
                }
    return envs

def gen_env_table(env_vars: dict) -> list:
    """生成环境变量表格"""
    lines = [
        "",
        "## 核心环境变量",
        "| 变量名 | 默认值 | 描述 |",
        "|--------|--------|------|"
    ]
    for var, info in sorted(env_vars.items()):
        default = f"`{info['default']}`" if info["default"] else ""
        lines.append(f"| {var} | {default} | {info['description']} |")
    return lines

def gen_version_section(base_dir: Path) -> list:
    """生成版本信息"""
    git_hash = ""
    try:
        git_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=base_dir,
            shell=True,
            text=True
        ).strip()
    except Exception:
        git_hash = "unknown"
    
    return [
        "",
        "## 版本信息",
        f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 环境版本: {git_hash}"
    ]

if __name__ == "__main__":
    main()