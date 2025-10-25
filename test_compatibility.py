#!/usr/bin/env python3
"""
跨平台兼容性测试脚本
测试项目在Windows和Linux上的基本功能
"""

import os
import sys
import platform
import subprocess
import json
from pathlib import Path

def test_environment():
    """测试环境配置"""
    print("🔍 环境检查")
    print("=" * 50)
    
    # 系统信息
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"Python版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")
    
    # 检查必要文件
    required_files = [
        "backend/app.py",
        "backend/requirements.txt",
        "vue-project/package.json",
        "start.sh",
        "start.bat",
        "stop.sh", 
        "stop.bat"
    ]
    
    print("\n📁 文件检查:")
    for file_path in required_files:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
    
    return all(os.path.exists(f) for f in required_files)

def test_backend_dependencies():
    """测试后端依赖"""
    print("\n🐍 后端依赖检查")
    print("=" * 50)
    
    try:
        # 检查Python包
        import flask
        print(f"✅ Flask: {flask.__version__}")
    except ImportError:
        print("❌ Flask 未安装")
        return False
    
    try:
        import flask_cors
        print("✅ flask-cors 已安装")
    except ImportError:
        print("❌ flask-cors 未安装")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv 已安装")
    except ImportError:
        print("❌ python-dotenv 未安装")
        return False
    
    return True

def test_frontend_dependencies():
    """测试前端依赖"""
    print("\n📦 前端依赖检查")
    print("=" * 50)
    
    # 检查Node.js
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js 未安装或不可用")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Node.js 未安装或不可用")
        return False
    
    # 检查npm
    try:
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
        else:
            print("❌ npm 未安装或不可用")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ npm 未安装或不可用")
        return False
    
    return True

def test_environment_files():
    """测试环境配置文件"""
    print("\n🔧 环境配置检查")
    print("=" * 50)
    
    # 检查后端环境文件
    backend_env_example = "backend/env.example"
    backend_env = "backend/.env"
    
    if os.path.exists(backend_env_example):
        print("✅ backend/env.example 存在")
    else:
        print("❌ backend/env.example 不存在")
        return False
    
    if os.path.exists(backend_env):
        print("✅ backend/.env 存在")
    else:
        print("⚠️  backend/.env 不存在 (需要手动创建)")
    
    # 检查前端环境文件
    frontend_env_example = "vue-project/env.example"
    frontend_env = "vue-project/.env"
    
    if os.path.exists(frontend_env_example):
        print("✅ vue-project/env.example 存在")
    else:
        print("❌ vue-project/env.example 不存在")
        return False
    
    if os.path.exists(frontend_env):
        print("✅ vue-project/.env 存在")
    else:
        print("⚠️  vue-project/.env 不存在 (需要手动创建)")
    
    return True

def test_scripts():
    """测试启动脚本"""
    print("\n🚀 脚本检查")
    print("=" * 50)
    
    # Linux/Mac脚本
    if os.path.exists("start.sh"):
        print("✅ start.sh 存在")
        # 检查脚本权限
        if os.access("start.sh", os.X_OK):
            print("✅ start.sh 有执行权限")
        else:
            print("⚠️  start.sh 没有执行权限")
    else:
        print("❌ start.sh 不存在")
    
    if os.path.exists("stop.sh"):
        print("✅ stop.sh 存在")
    else:
        print("❌ stop.sh 不存在")
    
    # Windows脚本
    if os.path.exists("start.bat"):
        print("✅ start.bat 存在")
    else:
        print("❌ start.bat 不存在")
    
    if os.path.exists("stop.bat"):
        print("✅ stop.bat 存在")
    else:
        print("❌ stop.bat 不存在")
    
    return True

def main():
    """主测试函数"""
    print("🌍 TripTeller 跨平台兼容性测试")
    print("=" * 60)
    
    tests = [
        ("环境检查", test_environment),
        ("后端依赖", test_backend_dependencies),
        ("前端依赖", test_frontend_dependencies),
        ("环境配置", test_environment_files),
        ("启动脚本", test_scripts)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试失败: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n📊 测试结果总结")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！项目已准备好跨平台运行。")
        print("\n📝 下一步:")
        print("1. 配置API密钥 (参考 API_KEYS.md)")
        print("2. 运行启动脚本:")
        if platform.system() == "Windows":
            print("   start.bat")
        else:
            print("   ./start.sh")
    else:
        print(f"\n⚠️  有 {total - passed} 项测试失败，请检查上述问题。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
