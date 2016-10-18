# -*- coding: utf-8 -*-
import os
import sys
import time
import hashlib
from fabric.state import env
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

# 项目根目录
env.project_path = os.path.dirname(os.path.realpath(__file__))
env.project_name = os.path.basename('{0.project_path}'.format(env))

# 编译成功后.app所在目录
env.app_path = '{0.project_path}/build/Build/Products/Release-iphoneos/{0.project_name}.app'.format(env)
# 指定项目下编译目录
env.build_path = "build"
# 打包后ipa存储目录
env.target_ipa_path = '{0.project_path}'.format(env)
env.ipa_filename = '{0.project_name}.ipa'.format(env)
env.infoPlist = '{0.project_path}/{0.project_name}/Info.plist'.format(env)


# 需要手动配置的全局参数
env.fir_api_token = "349e895ca7aceeafd4bca1eac5e0ab3b"
env.pgyer_user_key = '77052141e0dd09784a065d3df33b792f'
env.pgyer_api_key = '1d20194f501175be5ff08473b986295a'
env.from_address = "发件" # 发送邮件地址
env.password = "密码" # 发送邮件密码
env.smtp_server = "smtp.163.com"
to_address = ['收件'] # 收件地址


# 清理项目 创建build目录
def clean_project_mkdir_build():
    os.system('cd {0.project_path}/;xcodebuild clean'.format(env)) # clean 项目
    os.system('cd {0.project_path}/;mkdir build'.format(env))
    os.system('`/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" {0.infoPlist}`'.format(env))
    os.system('`/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" {0.infoPlist}`'.format(env))
    os.system('`/usr/libexec/PlistBuddy -c "Print CFBundleVersion" {0.infoPlist}`'.format(env))
def build_project():
    print("build release start")
    # os.system ('xcodebuild -list')
    os.system ('cd {0.project_path}/;xcodebuild -workspace {0.project_name}.xcworkspace  -scheme {0.project_name} -configuration Release -derivedDataPath {0.build_path} ONLY_ACTIVE_ARCH=NO || exit'.format(env))
# CONFIGURATION_BUILD_DIR=./build/Release-iphoneos

# 打包ipa 并且保存在桌面
def build_ipa():
    # ipa_filename = time.strftime('OSCHINA_%Y-%m-%d-%H-%M-%S.ipa',time.localtime(time.time()))
    os.system ('xcrun -sdk iphoneos PackageApplication -v {0.app_path} -o {0.target_ipa_path}/{0.ipa_filename}'.format(env))
    print('~~~~~~~~~~~~~~~~~~~结束编译，处理成功~~~~~~~~~~~~~~~~~~~')
#上传
def upload_to_fir():
    if os.path.exists("{0.target_ipa_path}/{0.ipa_filename}".format(env)):
        print('正在上传到fir.im....')
        # 直接使用fir 有问题 这里使用了绝对地址 在终端通过 which fir 获得
        ret = os.system('/usr/local/bin/fir p {0.target_ipa_path}/{0.ipa_filename} -T {0.fir_api_token}'.format(env))
    else:
        print("没有找到ipa文件")
def upload_to_pgyer():
    if os.path.exists("{0.target_ipa_path}/{0.ipa_filename}".format(env)):
        print('正在上传到pyger....')
        # 直接使用fir 有问题 这里使用了绝对地址 在终端通过 which fir 获得
        ret = os.system('ipa distribute:pgyer -u {0.pgyer_user_key} -a {0.pgyer_api_key}'.format(env))
    else:
        print("没有找到ipa文件")

# 发邮件 https://docs.python.org/2.7/library/email-examples.html
def send_mail():
    msg = MIMEText('{0.project_name} iOS测试项目已经打包完毕，请前往 http://fir.im/ {0.project_name} 下载测试！'.format(env), 'plain', 'utf-8')
    msg['From'] = '自动打包系统 <{0.from_address}>'.format(env)
    msg['To'] = '{0.project_name}测试人员 <%s>'.format(env)%(to_address)
    msg['Subject'] = Header('{0.project_name} iOS客户端打包程序'.format(env), 'utf-8').encode()
    server = smtplib.SMTP('{0.smtp_server}'.format(env), 25)
    server.set_debuglevel(1)
    print('{0.from_address}hello word'.format(env))
    server.login('{0.from_address}'.format(env), '{0.password}'.format(env))
    server.sendmail('{0.from_address}'.format(env), to_address, msg.as_string())
    server.quit()
    print('{0.project_name} iOS测试项目已经打包完毕，请前往 http://fir.im/ {0.project_name} 下载测试！'.format(env))
    os.system('say 打包 完毕，请 下载测试！')

def main():
    # 清理并创建build目录
    clean_project_mkdir_build()
    # 编译coocaPods项目文件并 执行编译目录
    build_project()
    # 打包ipa 并制定到桌面
    build_ipa()
    # 上传fir
    # upload_to_fir()
    upload_to_pgyer()
    # 发邮件
    send_mail()
# 执行
main()
