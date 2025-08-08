import urllib.request
from collections import OrderedDict
import datetime
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义规则URL
url1 = "https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt"
url2 = "https://anti-ad.net/easylist.txt"

# 创建两个目录
rules_dir = "rules"  # 未合并规则保存目录
merge_dir = "rules-merge"  # 合并后规则保存目录

# 确保目录存在
os.makedirs(rules_dir, exist_ok=True)
os.makedirs(merge_dir, exist_ok=True)

# 下载规则内容
def download_rules(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8').splitlines()
    except Exception as e:
        logging.error(f"下载失败: {url} - {str(e)}")
        return []

# 下载两个规则文件
rules1 = download_rules(url1)
rules2 = download_rules(url2)

# 检查规则是否下载成功
if not rules1 or not rules2:
    logging.error("错误：至少有一个规则下载失败")
    exit(1)

# 保存未合并的规则文件
with open(os.path.join(rules_dir, "filter_1.txt"), 'w', encoding='utf-8') as f:
    f.write("\n".join(rules1))

with open(os.path.join(rules_dir, "anti-ad-easylist.txt"), 'w', encoding='utf-8') as f:
    f.write("\n".join(rules2))

# 合并规则并去重（保留顺序）
combined_rules = OrderedDict()
for rule in rules1 + rules2:
    # 保留非空行和有效规则（跳过注释/元数据）
    stripped = rule.strip()
    if stripped and not stripped.startswith(('!', '#', '[')):
        combined_rules[stripped] = None

# 准备文件头信息
total_rules = len(combined_rules)
timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
header = f"""! Title: Merged AdGuard Rules
! Description: Combined rules from AdGuardTeam and anti-AD
! Sources:
!   {url1}
!   {url2}
! Total rules: {total_rules:,}
! Updated: {timestamp}
!
"""

# 合并后的文件保存路径
output_filename = f"merge_{timestamp.replace(' ', '_').replace(':', '-')}.txt"
output_path = os.path.join(merge_dir, output_filename)

# 写入合并后的文件
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(header)
    f.write("\n".join(combined_rules.keys()))

logging.info(f"原始规则已保存到 {rules_dir}/ 目录")
logging.info(f"合并完成！原始规则: {len(rules1)+len(rules2):,} 条")
logging.info(f"去重后保留: {total_rules:,} 条")
logging.info(f"合并文件已保存到 {output_path}")
