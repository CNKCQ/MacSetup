# -*- coding: utf-8 -*-
import os
import sys
import time
import hashlib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

# 项目根目录
project_path = "/Users/KingCQ/opensource/OSCHINA/"
# 编译成功后.app所在目录
app_path = "/Users/KingCQ/opensource/OSCHINA/build/Build/Products/Release-iphoneos/OSCHINA.app"
# 指定项目下编译目录
build_path = "build"
# 打包后ipa存储目录
targerIPA_parth = "/Users/KingCQ/Desktop"
infoPlist = "/Users/KingCQ/opensource/OSCHINA/Info.plist"

# firm的api token
fir_api_token = "349e895ca7aceeafd4bca1eac5e0ab3b"

from_addr = "wangchengqvan@163.com"
password = "wcq249718"
smtp_server = "smtp.163.com"
to_addr = ['1920452890@qq.com','2280534011@qq.com','1844368740@qq.com']


# 清理项目 创建build目录
def clean_project_mkdir_build():
    os.system('cd %s;xcodebuild clean' % project_path) # clean 项目
    os.system('cd %s;mkdir build' % project_path)
    os.system('`/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" %s`' % infoPlist)
    os.system('`/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" %s`' % infoPlist)
    os.system('`/usr/libexec/PlistBuddy -c "Print CFBundleVersion" %s`' % infoPlist)
def build_project():
    print("build release start")
    os.system ('xcodebuild -list')
    os.system ('cd %s;xcodebuild -workspace OSCHINA.xcworkspace  -scheme OSCHINA -configuration release -derivedDataPath %s ONLY_ACTIVE_ARCH=NO || exit' % (project_path,build_path))
# CONFIGURATION_BUILD_DIR=./build/Release-iphoneos

# 打包ipa 并且保存在桌面
def build_ipa():
    global ipa_filename
    ipa_filename = time.strftime('OSCHINA_%Y-%m-%d-%H-%M-%S.ipa',time.localtime(time.time()))
    os.system ('xcrun -sdk iphoneos PackageApplication -v %s -o %s/%s'%(app_path,targerIPA_parth,ipa_filename))
    print('~~~~~~~~~~~~~~~~~~~结束编译，处理成功~~~~~~~~~~~~~~~~~~~')
#上传
def upload_fir():
    if os.path.exists("%s/%s" % (targerIPA_parth,ipa_filename)):
        print('正在上传到fir.im....')
        # 直接使用fir 有问题 这里使用了绝对地址 在终端通过 which fir 获得
        ret = os.system("/usr/local/bin/fir p '%s/%s' -T '%s'" % (targerIPA_parth,ipa_filename,fir_api_token))
    else:
        print("没有找到ipa文件")

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 发邮件
def send_mail():
    msg = MIMEText('OSCHINA iOS测试项目已经打包完毕，请前往 http://fir.im/OSCHINA 下载测试！', 'plain', 'utf-8')
    msg['From'] = _format_addr('自动打包系统 <%s>' % from_addr)
    msg['To'] = _format_addr('OSCHINA测试人员 <%s>' % to_addr)
    msg['Subject'] = Header('OSCHINA iOS客户端打包程序', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
    print('OSCHINA iOS测试项目已经打包完毕，请前往 http://fir.im/OSCHINA 下载测试！')

def main():
    # 清理并创建build目录
    clean_project_mkdir_build()
    # 编译coocaPods项目文件并 执行编译目录
    build_project()
    # 打包ipa 并制定到桌面
    build_ipa()
    # 上传fir
    upload_fir()
    # 发邮件
    send_mail()

# 执行
# main()
