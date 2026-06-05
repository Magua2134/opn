
@echo off
chcp 65001 >nul
echo ========================================
echo     OPN首码项目 - 重新部署
echo ========================================
echo.

REM 删除旧的.git文件夹（如果存在）
if exist ".git" (
    echo [清理] 删除旧的git仓库...
    rmdir /s /q ".git"
    echo ✅ 已清理
    echo.
)

echo [1/6] 初始化Git仓库...
git init
if %errorlevel% neq 0 (
    echo ❌ Git初始化失败！
    pause
    exit /b 1
)
echo ✅ 初始化成功
echo.

echo [2/6] 配置Git用户...
git config user.name "Magua2134"
git config user.email "magua@example.com"
echo ✅ 配置完成
echo.

echo [3/6] 添加所有文件...
git add .
echo ✅ 文件已添加
echo.

echo [4/6] 提交代码...
git commit -m "Initial commit: OPN首码项目页面"
if %errorlevel% neq 0 (
    echo ❌ 提交失败！
    pause
    exit /b 1
)
echo ✅ 提交成功
echo.

echo [5/6] 连接GitHub仓库...
git remote add origin https://github.com/Magua2134/OPN.git
echo ✅ 连接成功
echo.

echo [6/6] 推送到GitHub...
echo.
echo ========================================
echo   正在推送...
echo   注意：首次推送可能需要GitHub认证！
echo ========================================
echo.
git push -u origin main --force
echo.

if %errorlevel% equ 0 (
    echo.
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
    echo.
    echo ========================================
    echo   ❌ 推送失败！
    echo ========================================
    echo.
    echo 请确认:
    echo 1. GitHub仓库 https://github.com/Magua2134/OPN 是否已创建？
    echo 2. 仓库名称是否为 OPN （注意大小写）？
    echo 3. 仓库是否为 Public（公开）？
    echo.
)

pause

