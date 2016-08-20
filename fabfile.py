# -*- coding: utf-8 -*-

import os
import sys

from fabric.colors import blue, cyan, green, magenta, red, yellow
from fabric.decorators import task
from fabric.operations import local
from fabric.state import env
from fabric.utils import puts


env.version = '0.8.8'


# ============
# =  Hello   =
# ============
@task(default=True, alias='别名测试')
def h():
    puts('*' * 50)
    puts(cyan('  Fabric 使用指南\n'))
    puts(green('  查看所有命令: fab -l'))
    puts(green('  查看命令: fab -d 命令'))
    puts(yellow('  带参数命令请输入: fab 命令:参数'))
    puts('*' * 50)
