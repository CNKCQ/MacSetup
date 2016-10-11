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
project_path = os.path.dirname(os.path.realpath(__file__))
project_name = os.path.basename(project_path)

# 编译成功后.app所在目录
app_path = '%s/build/Build/Products/Release-iphoneos/%s.app' % (project_path, project_name)
# 指定项目下编译目录
build_path = "build"
# 打包后ipa存储目录
target_ipa_path = project_path
infoPlist = "%s/%s/Info.plist" % (project_path, project_name)


# firm的api token
fir_api_token = "349e895ca7aceeafd4bca1eac5e0ab3b"
pgyer_user_key = '77052141e0dd09784a065d3df33b792f'
pgyer_api_key = '1d20194f501175be5ff08473b986295a'
from_address = "wangchengqvan@163.com"
password = "wcq249718"
smtp_server = "smtp.163.com"
to_address = ['1920452890@qq.com','2280534011@qq.com','1844368740@qq.com']


# 清理项目 创建build目录
def clean_project_mkdir_build():
    os.system('cd %s/;xcodebuild clean' % project_path) # clean 项目
    os.system('cd %s/;mkdir build' % project_path)
    os.system('`/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" %s`' % infoPlist)
    os.system('`/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" %s`' % infoPlist)
    os.system('`/usr/libexec/PlistBuddy -c "Print CFBundleVersion" %s`' % infoPlist)
def build_project():
    print("build release start")
    # os.system ('xcodebuild -list')
    os.system ('cd %s/;xcodebuild -workspace %s.xcworkspace  -scheme %s -configuration Release -derivedDataPath %s ONLY_ACTIVE_ARCH=NO || exit' % (project_path ,project_name, project_name, build_path))
# CONFIGURATION_BUILD_DIR=./build/Release-iphoneos

# 打包ipa 并且保存在桌面
def build_ipa():
    global ipa_filename
    # ipa_filename = time.strftime('OSCHINA_%Y-%m-%d-%H-%M-%S.ipa',time.localtime(time.time()))
    ipa_filename = '%s.ipa' % project_name
    os.system ('xcrun -sdk iphoneos PackageApplication -v %s -o %s/%s'%(app_path,target_ipa_path,ipa_filename))
    print('~~~~~~~~~~~~~~~~~~~结束编译，处理成功~~~~~~~~~~~~~~~~~~~')
#上传
def upload_fir():
    if os.path.exists("%s/%s" % (target_ipa_path,ipa_filename)):
        print('正在上传到fir.im....')
        # 直接使用fir 有问题 这里使用了绝对地址 在终端通过 which fir 获得
        ret = os.system('/usr/local/bin/fir p %s/%s -T %s' % (target_ipa_path,ipa_filename,fir_api_token))
    else:
        print("没有找到ipa文件")
def upload_to_pgyer():
    if os.path.exists("%s/%s" % (target_ipa_path,ipa_filename)):
        print('正在上传到pyger....')
        # 直接使用fir 有问题 这里使用了绝对地址 在终端通过 which fir 获得
        ret = os.system('ipa distribute:pgyer -u %s -a %s' %(pgyer_user_key, pgyer_api_key))
    else:
        print("没有找到ipa文件")

# 发邮件 https://docs.python.org/2.7/library/email-examples.html
def send_mail():
    msg = MIMEText('%s iOS测试项目已经打包完毕，请前往 http://fir.im/ %s 下载测试！' % (project_name, project_name), 'plain', 'utf-8')
    msg['From'] = '自动打包系统 <%s>' % (from_address)
    msg['To'] = '%s测试人员 <%s>' % (project_name, to_address)
    msg['Subject'] = Header('%s iOS客户端打包程序' % project_name, 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_address, password)
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()
    print('%s iOS测试项目已经打包完毕，请前往 http://fir.im/ %s 下载测试！' % (project_name, project_name))
    os.system('say 打包 完毕，请 下载测试！')

def main():
    # 清理并创建build目录
    clean_project_mkdir_build()
    # 编译coocaPods项目文件并 执行编译目录
    build_project()
    # 打包ipa 并制定到桌面
    build_ipa()
    # 上传fir
    # upload_fir()
    upload_to_pgyer()
    # 发邮件
    send_mail()
# 执行
main()
