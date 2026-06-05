#!/usr/bin/env python3
"""
OPN首码项目 - SEO自动化检查脚本
功能：
1. 每日收录检查 - 百度/Google是否收录
2. 关键词排名跟踪 - 检查关键词排名变化
3. 内容更新提醒 - 提醒该更新内容了

用法：
    python seo_checker.py              # 运行完整检查
    python seo_checker.py --baidu       # 只检查百度收录
    python seo_checker.py --google      # 只检查Google收录
    python seo_checker.py --keywords    # 只检查关键词
"""

import os
import sys
import json
import datetime
import urllib.request
import urllib.parse
import re
import subprocess
from pathlib import Path

# ============ 配置 ============
SITE_URL = "https://magua2134.github.io/opn/"
SITE_DOMAIN = "magua2134.github.io/opn"

# 要跟踪的关键词列表（长尾词优先，更容易排上去）
KEYWORDS = [
    "OPN首码",
    "OPN首码注册",
    "OPN邀请码",
    "OPN项目",
    "OPN daily玩法",
    "涟上爬墙项目",
    "零撸赚钱项目",
    "2026手机赚钱",
]

# 内容更新提醒阈值（天）
CONTENT_UPDATE_DAYS = 7

# 结果保存路径
RESULT_FILE = "seo_status.json"
REPORT_FILE = "SEO_REPORT.md"

# ============ 工具函数 ============

def log(msg):
    """带时间戳的日志输出"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")

def fetch_url(url, timeout=15):
    """请求URL并返回内容"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36"
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        log(f"⚠️ 请求失败: {url} -> {e}")
        return None

# ============ 1. 百度收录检查 ============

def check_baidu_index():
    """检查百度是否收录"""
    log("🔍 检查百度收录...")
    
    # 使用百度搜索 site: 语法
    url = f"https://www.baidu.com/s?wd=site%3A{SITE_DOMAIN}"
    html = fetch_url(url)
    
    if html is None:
        return {"status": "unknown", "detail": "请求失败"}
    
    # 检查是否被收录
    if "没有找到该URL" in html or "很抱歉" in html:
        result = {"status": "not_indexed", "detail": "❌ 百度未收录"}
        log(f"   {result['detail']}")
        return result
    
    # 尝试提取收录数量
    match = re.search(r'找到相关结果约(\d+)个', html)
    if match:
        count = match.group(1)
        result = {"status": "indexed", "count": count, "detail": f"✅ 百度已收录，约{count}个结果"}
        log(f"   {result['detail']}")
        return result
    
    # 有结果但无法提取数量
    result = {"status": "likely_indexed", "detail": "✅ 百度可能已收录"}
    log(f"   {result['detail']}")
    return result


# ============ 2. Google收录检查 ============

def check_google_index():
    """检查Google是否收录"""
    log("🔍 检查Google收录...")
    
    # 使用Google搜索 site: 语法
    url = f"https://www.google.com/search?q=site%3A{SITE_DOMAIN}"
    html = fetch_url(url)
    
    if html is None:
        return {"status": "unknown", "detail": "请求失败（可能需要代理）"}
    
    # 检查是否被收录
    if "没有找到与" in html or "did not match" in html:
        result = {"status": "not_indexed", "detail": "❌ Google未收录"}
        log(f"   {result['detail']}")
        return result
    
    # 尝试提取收录数量
    match = re.search(r'约 ([0-9,]+) 条结果', html)
    if match:
        count = match.group(1)
        result = {"status": "indexed", "count": count, "detail": f"✅ Google已收录，约{count}条结果"}
        log(f"   {result['detail']}")
        return result
    
    match = re.search(r'About ([0-9,]+) results', html)
    if match:
        count = match.group(1)
        result = {"status": "indexed", "count": count, "detail": f"✅ Google已收录，约{count}条结果"}
        log(f"   {result['detail']}")
        return result
    
    # 能返回页面说明可能被收录
    result = {"status": "likely_indexed", "detail": "✅ Google可能已收录"}
    log(f"   {result['detail']}")
    return result


# ============ 3. 关键词排名检查 ============

def check_keyword_ranking(keyword):
    """检查关键词在百度的排名（粗略）"""
    log(f"   🔑 检查关键词: {keyword}")
    
    encoded = urllib.parse.quote(keyword)
    url = f"https://www.baidu.com/s?wd={encoded}"
    html = fetch_url(url)
    
    if html is None:
        return {"keyword": keyword, "rank": None, "found": False}
    
    # 检查当前网站是否出现在搜索结果中
    if SITE_DOMAIN in html or "opn" in html.lower():
        # 粗略估算排名（在结果中的位置）
        result = {"keyword": keyword, "rank": "前10页内", "found": True, "detail": f"✅ '{keyword}' 可能在搜索结果中出现"}
        log(f"      {result['detail']}")
        return result
    else:
        result = {"keyword": keyword, "rank": None, "found": False, "detail": f"❌ '{keyword}' 未在搜索结果中找到"}
        log(f"      {result['detail']}")
        return result


def check_all_keywords():
    """检查所有关键词"""
    log("🔍 检查关键词排名...")
    results = []
    for kw in KEYWORDS:
        result = check_keyword_ranking(kw)
        results.append(result)
    return results


# ============ 4. 内容更新检查 ============

def check_content_age():
    """检查内容更新时间"""
    log("🔍 检查内容更新时间...")
    
    try:
        # 获取最近一次git提交时间
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cd", "--date=short"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            last_commit_date = result.stdout.strip()
            last_commit = datetime.datetime.strptime(last_commit_date, "%Y-%m-%d")
            days_since_update = (datetime.datetime.now() - last_commit).days
            
            log(f"   最近更新: {last_commit_date} ({days_since_update}天前)")
            
            if days_since_update > CONTENT_UPDATE_DAYS:
                log(f"   ⚠️ 已超过{CONTENT_UPDATE_DAYS}天未更新，建议更新内容！")
                return {
                    "last_update": last_commit_date,
                    "days_since_update": days_since_update,
                    "needs_update": True,
                    "detail": f"⚠️ 已{days_since_update}天未更新，建议更新内容（阈值{CONTENT_UPDATE_DAYS}天）"
                }
            else:
                return {
                    "last_update": last_commit_date,
                    "days_since_update": days_since_update,
                    "needs_update": False,
                    "detail": f"✅ {days_since_update}天前更新过，内容较新"
                }
    except Exception as e:
        log(f"   ⚠️ Git检查失败: {e}")
    
    return {"last_update": "unknown", "days_since_update": None, "needs_update": None, "detail": "无法获取更新时间，请确认Git可用"}


# ============ 5. 网站可访问性检查 ============

def check_site_accessibility():
    """检查网站是否可以正常访问"""
    log("🔍 检查网站可访问性...")
    
    html = fetch_url(SITE_URL)
    if html is None:
        return {"status": "down", "detail": "❌ 网站无法访问！"}
    
    # 检查关键内容是否存在
    checks = {
        "标题包含OPN": "OPN" in html,
        "包含邀请码": "KDYL7W" in html,
        "包含联系方式": "362917919" in html,
    }
    
    all_ok = all(checks.values())
    if all_ok:
        result = {"status": "ok", "checks": checks, "detail": "✅ 网站正常访问，关键内容完整"}
    else:
        failed = [k for k, v in checks.items() if not v]
        result = {"status": "warning", "checks": checks, "detail": f"⚠️ 网站可访问，但部分内容缺失: {failed}"}
    
    log(f"   {result['detail']}")
    return result


# ============ 报告生成 ============

def load_history():
    """加载历史记录"""
    if os.path.exists(RESULT_FILE):
        try:
            with open(RESULT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"history": []}
    return {"history": []}

def save_history(record):
    """保存本次检查记录"""
    history = load_history()
    history["history"].append(record)
    # 只保留最近30次记录
    if len(history["history"]) > 30:
        history["history"] = history["history"][-30:]
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    log(f"✅ 结果已保存到 {RESULT_FILE}")

def generate_report(result):
    """生成Markdown报告"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# 📊 OPN首码项目 SEO 检查报告

> 生成时间：{now}

---

## 🌐 网站状态

| 项目 | 状态 |
|------|------|
| 网站可访问性 | {result['accessibility']['detail']} |
| 百度收录 | {result['baidu']['detail']} |
| Google收录 | {result['google']['detail']} |
| 内容更新 | {result['content_age']['detail']} |

## 🔑 关键词排名

| 关键词 | 状态 |
|--------|------|
"""
    for kw in result['keywords']:
        report += f"| {kw['keyword']} | {kw.get('detail', '未检查')} |\n"
    
    report += f"""
## 📋 建议

"""
    suggestions = []
    
    if result['baidu']['status'] == 'not_indexed':
        suggestions.append("- 🔴 **急需操作**：百度未收录，请前往 https://ziyuan.baidu.com 提交网站")
    
    if result['google']['status'] == 'not_indexed':
        suggestions.append("- 🟡 **建议操作**：Google未收录，请前往 https://search.google.com/search-console 提交")
    
    if result['content_age'].get('needs_update'):
        suggestions.append(f"- 🟡 **建议更新**：已{result['content_age']['days_since_update']}天未更新内容")
    
    not_found_keywords = [kw['keyword'] for kw in result['keywords'] if not kw['found']]
    if not_found_keywords:
        suggestions.append(f"- 🟡 **关键词优化**：以下关键词未在搜索结果中出现：{', '.join(not_found_keywords)}")
    
    if not suggestions:
        suggestions.append("- ✅ 一切正常，继续保持！")
    
    report += "\n".join(suggestions) + "\n\n"
    report += "---\n*本报告由 SEO 自动检查脚本生成*\n"
    
    return report

def save_report(report):
    """保存报告到文件"""
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)
    log(f"✅ 报告已保存到 {REPORT_FILE}")
    # 也打印到控制台
    print("\n" + "="*50)
    print(report)
    print("="*50)


# ============ 主函数 ============

def run_all_checks():
    """运行所有检查"""
    log("=" * 50)
    log("🚀 OPN首码项目 SEO 自动检查开始")
    log(f"   网站: {SITE_URL}")
    log("=" * 50)
    
    result = {
        "timestamp": datetime.datetime.now().isoformat(),
        "site_url": SITE_URL,
    }
    
    # 1. 网站可访问性
    result["accessibility"] = check_site_accessibility()
    
    # 2. 百度收录
    result["baidu"] = check_baidu_index()
    
    # 3. Google收录
    result["google"] = check_google_index()
    
    # 4. 关键词排名
    result["keywords"] = check_all_keywords()
    
    # 5. 内容更新
    result["content_age"] = check_content_age()
    
    # 保存结果
    save_history(result)
    
    # 生成报告
    report = generate_report(result)
    save_report(report)
    
    log("=" * 50)
    log("✅ SEO检查完成！")
    log(f"📄 详细报告: {REPORT_FILE}")
    log("=" * 50)
    
    return result


if __name__ == "__main__":
    # 解析命令行参数
    if "--baidu" in sys.argv:
        result = check_baidu_index()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif "--google" in sys.argv:
        result = check_google_index()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif "--keywords" in sys.argv:
        results = check_all_keywords()
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif "--help" in sys.argv:
        print(__doc__)
    else:
        run_all_checks()
