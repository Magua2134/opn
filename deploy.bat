
@echo off
echo ========================================
echo     OPN首码项目 - 部署到GitHub Pages
echo ========================================
echo.

echo [1/8] 检查Git安装...
git --version
if %errorlevel% neq 0 (
    echo ❌ Git未安装！请先下载安装Git: https://git-scm.com/downloads
    pause
    exit /b 1
)
echo ✅ Git已安装
echo.

echo [2/8] 初始化Git仓库...
git init
echo.

echo [3/8] 配置Git用户信息...
echo 请输入你的GitHub用户名:
set /p GIT_NAME=
echo 请输入你的GitHub邮箱:
set /p GIT_EMAIL=
git config user.name "%GIT_NAME%"
git config user.email "%GIT_EMAIL%"
echo ✅ 配置完成
echo.

echo [4/8] 添加所有文件...
git add .
echo.

echo [5/8] 提交代码...
git commit -m "Initial commit: OPN首码项目页面"
echo.

echo [6/8] 连接GitHub仓库...
git remote add origin https://github.com/Magua2134/OPN.git
if %errorlevel% neq 0 (
    echo ℹ️ 远程仓库已存在，尝试更新URL...
    git remote set-url origin https://github.com/Magua2134/OPN.git
)
echo.

echo [7/8] 切换到main分支...
git branch -M main
echo.

echo [8/8] 推送到GitHub...
echo.
echo ========================================
echo   推送到GitHub仓库...
echo   注意：首次推送可能需要GitHub认证！
echo ========================================
echo.
git push -u origin main
echo.

if %errorlevel% equ 0 (
    echo ========================================
    echo   ✅ 部署成功！
    echo ========================================
    echo.
    echo 下一步:
    echo 1. 进入你的GitHub仓库: https://github.com/Magua2134/OPN
    echo 2. 点击 Settings -^> Pages
    echo 3. Source选择"Deploy from a branch"
    echo 4. Branch选择"main"，保存
    echo 5. 等待1-5分钟，访问: https://Magua2134.github.io/OPN/
    echo.
) else (
    echo ========================================
    echo   ❌ 推送失败！
    echo ========================================
    echo.
    echo 请检查:
    echo 1. GitHub仓库是否已创建
    echo 2. 网络连接是否正常
    echo 3. GitHub认证是否成功
    echo.
)

pause

