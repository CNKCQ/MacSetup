# -*- coding: utf-8 -*-

import os
import sys

from fabric.colors import blue, cyan, green, magenta, red, yellow
from fabric.decorators import task
from fabric.operations import local
from fabric.state import env
from fabric.utils import puts

from ipa import *

env.version = '0.8.8'
env.pgyer_user_key = '77052141e0dd09784a065d3df33b792f'
env.pgyer_api_key = '1d20194f501175be5ff08473b986295a'

env.project_name = os.path.basename(os.path.dirname(__file__))
env.from_address = '你好'
# ============
# =  Hello   =
# ============
@task(default=True, alias='别名测试')
def h():
    """atuo exc world"""
    puts('*' * 50)
    puts(cyan('  Fabric 使用指南\n'))
    puts(green('  查看所有命令: fab -l'))
    puts(green('  查看命令: fab -d 命令'))
    puts(yellow('  带参数命令请输入: fab 命令:参数'))
    puts('*' * 50)
@task
def upload_to_pgyer():
    """自动打包上传到蒲公英"""
    ipa = '{}.ipa'.format(env.project_name)
    if os.path.exists(ipa):
        os.remove(ipa)
    local('ipa build')
    local('ipa distribute:pgyer -u {0.pgyer_user_key} -a {0.pgyer_api_key}'.format(env))
@task
def upload_to_fir():
    """自动打包上传到fir"""
    main()
