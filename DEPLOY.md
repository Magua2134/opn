# GitHub Pages 部署指南

## 前置准备

1. 注册 GitHub 账号（如果还没有的话）：https://github.com
2. 安装 Git：https://git-scm.com/downloads

## 部署步骤

### 第一步：创建 GitHub 仓库

1. 登录 GitHub
2. 点击右上角的 "+" 图标，选择 "New repository"
3. 仓库名称建议：`OPN`（或你喜欢的其他名称）
4. 选择 "Public"（公开仓库）
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

### 第二步：初始化本地仓库

打开命令行（PowerShell 或 CMD），进入项目目录：

```powershell
cd c:\Users\12248\Desktop\OPN
```

初始化 Git 仓库：

```powershell
git init
```

### 第三步：配置 Git

```powershell
git config user.name "你的GitHub用户名"
git config user.email "你的GitHub邮箱"
```

### 第四步：添加文件并提交

```powershell
git add .
git commit -m "Initial commit: OPN首码项目页面"
```

### 第五步：连接到 GitHub 仓库

将下面的 `yourusername` 替换为你的 GitHub 用户名：

```powershell
git remote add origin https://github.com/yourusername/OPN.git
git branch -M main
git push -u origin main
```

### 第六步：启用 GitHub Pages

1. 进入你的 GitHub 仓库页面
2. 点击 "Settings"（设置）
3. 在左侧菜单中找到 "Pages"
4. 在 "Build and deployment" 部分：
   - Source 选择 "Deploy from a branch"
   - Branch 选择 "main" 分支
   - 文件夹选择 "/ (root)"
5. 点击 "Save"

### 第七步：等待部署完成

- 通常需要 1-5 分钟
- 部署成功后，你会在 Pages 页面看到访问链接
- 访问地址格式：`https://yourusername.github.io/OPN/`

## 更新页面内容

如果后续需要修改页面内容：

1. 修改 `index.html` 文件
2. 提交并推送更改：

```powershell
git add .
git commit -m "更新页面内容"
git push
```

3. GitHub Pages 会自动重新部署

## 自定义域名（可选）

如果你有自己的域名：

1. 在仓库根目录创建 `CNAME` 文件，内容为你的域名（例如：`opn.example.com`）
2. 在你的域名 DNS 管理中添加 CNAME 记录，指向 `yourusername.github.io`
3. 在 GitHub Pages 设置中填写你的自定义域名

## 常见问题

**Q: 页面无法访问？**
A: 检查是否正确启用了 GitHub Pages，等待几分钟让部署完成。

**Q: 图片无法加载？**
A: 确保图片链接是绝对 URL 并且可以公开访问。

**Q: 如何修改页面内容？**
A: 直接编辑 `index.html` 文件，然后提交并推送到 GitHub。
