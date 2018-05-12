#!/bin/sh

# 全局总下载位置
downloadPath="$HOME/tools"

# 全局总安装路径
installPath="/application"

# 确保不接收任何参数
[ ${#} -eq 0 ] || {
    echo "$0 need 0 parameter but you give ${#}"
    exit 1
}

# 状态展示
. /etc/init.d/functions

function sureOk {
    [ $1 -eq 0 ] && {
        action "$2 is" /bin/true
    } || {
        action "$2 is" /bin/false
        exit $1
    }
}

# 获取系统版本
[ $(awk -F "[ .]+" '{print $3}' /etc/redhat-release) == "6" ] && {
    CentosVersion="6"
} || {
    CentosVersion="7"
}

# 开机启动加载文件
onbootFile="/etc/rc.local"

# 全局变量
globalPath="/etc/profile"

# 个人bash设置
vitrualEnvPath="$HOME/.pyenv"
userBashConf="$HOME/.bashrc"

# 全局下载位置
soureDownloadPath="$HOME/tools"

# 全局安装目录
installPath="/application"

# 软件名
pythonSoftName="Python"
nginxSoftName="nginx"
nginxServerName="www"

# 软件版本
pythonVersion="3.6.4"
nginxVersion="1.12.2"
nginxHidenVersion="2.2.15"

# 软件执行目录
pythonBinPath="bin"
nginxBinPath="sbin"

# 软件启动目录
nginxStartCmd="nginx"

# 软件解压后包名
pythonPkgPath="${pythonSoftName}-${pythonVersion}"
nginxPkgPath="${nginxSoftName}-${nginxVersion}"

# 软件下载压缩包名
pythonPkgName="${pythonPkgPath}.tgz"
nginxPkgName="${nginxPkgPath}.tar.gz"

# 软件核心配置文件
nginxConfFile="${installPath}/${nginxSoftName}/conf/nginx.conf"

# 软件下载 URL
pythonDownloadUrl="https://www.python.org/ftp/python/${pythonVersion}/${pythonPkgName}"
nginxDownloadUrl="http://nginx.org/download/${nginxPkgName}"

# 软件运行所需要的用户
rootUser="root"
mysqlRunUser="mysql"
nginxRunUser="nginx"

# 软件相关依赖包
pythonRelayPkg="zlib-devel:gcc:gcc-c++:openssl-devel:sqlite-devel:wget"
nginxRelayPkg="pcre-devel:openssl-devel:gcc-c++:wget"
pythonVirtualPkg="virtualenvwrapper"

# 相关编译参数
nginxConfigure="\
--user=${nginxRunUser}:\
--group=${nginxRunUser}:\
--with-http_ssl_module:\
--with-http_stub_status_module:\
--prefix=$installPath/$nginxPkgPath"

pythonConfigure="\
--enable-optimizations:\
--prefix=$installPath/${pythonPkgPath}:\
--with-ssl"


# 初始化下载目录
[ -d $soureDownloadPath ] || {
    mkdir $soureDownloadPath
    sureOk $? "init DownloadPath"
}

# 安装对应软件依赖包
# SoftName RelayPkg
function GoYumRelayPkg {
    echo "yum install $1 RelayPkg ...ing"
    yum install -y $(echo $2|tr ":" " ") &> /dev/null
    sureOk $? "yum install $1 RelayPkg"
}

function envYumRelayPkg {
    GoYumRelayPkg $pythonSoftName $pythonRelayPkg
    GoYumRelayPkg $nginxSoftName $nginxRelayPkg
}

# 添加软件运行态用户
# RunUser
function GoAddRunUser {
    id $1 &> /dev/null
    [ $? -eq 0 ] || {
        useradd $1 -s /sbin/nologin -M
    }
    sureOk $? "Add User $1"
}

function envAddRunUser {
    GoAddRunUser $nginxRunUser
}

# 下载软件的源码包
# DownloadUrl PkgName
function GoDownload {
    cd $soureDownloadPath
    if [ ! -f $3 ]; then
        echo "download $2 ...ing, please wait ...ing"
        wget $1
    fi
    sureOk $? "download $2"    
}

function envPkgDownload {
    GoDownload $nginxDownloadUrl $nginxSoftName $nginxPkgName
    GoDownload $pythonDownloadUrl $pythonSoftName $pythonPkgName
}

# 解压软件源码包
# PkgName
function GoUntar {
    cd $soureDownloadPath
    echo "Untar $1 ...ing"
    tar -xf $1
    sureOk $? "Untar $1"    
}

function envUntarPkg {
    GoUntar $nginxPkgName
    GoUntar $pythonPkgName
}

# 设置编译参数
# PkgPath Configure SoftName "make/cmake"
function GoConfigure {
    cd $soureDownloadPath/$1
    echo "configure $3 ...ing, please wait ...ing"
    ./configure $(echo $2|tr ":" " ") &> /dev/null
    sureOk $? "configure $3"

}

function envConfigure {
    GoConfigure $nginxPkgPath $nginxConfigure $nginxSoftName 
    GoConfigure $pythonPkgPath $pythonConfigure $pythonSoftName
}

# 编译源码
# PkgPath SoftName
function GoMake {
    cd $soureDownloadPath/$1
    echo "Make $2 ...ing, manybe need a long time, please wait ...ing"
    make &> /dev/null
    sureOk $? "make $2"
}

function envMake {
    GoMake $nginxPkgPath $nginxSoftName
    GoMake $pythonPkgPath $pythonSoftName
}

# 安装软件
# PkgPath SoftName
function GoMakeInstall {
    cd $soureDownloadPath/$1
    echo "make install $2 ...ing"
    make install &> /dev/null
    sureOk $? "make install $2"
}

function envMakeInstall {
    GoMakeInstall $nginxPkgPath $nginxSoftName
    GoMakeInstall $pythonPkgPath $pythonSoftName
}

# 创建软件对应的软链接
# PkgPath SoftName
function GoCreateSoftLink {
    ln -s $installPath/$1 $installPath/$2
    sureOk $? "CreateSoftLink $2"
}

function envCreateSoftLink {
    GoCreateSoftLink $nginxPkgPath $nginxSoftName
    GoCreateSoftLink $pythonPkgPath $pythonSoftName
}

function GoGlobalSet {
    echo $1 $2
    # 获取 export所在行
    exportLineNum=`sed -n '/export PATH=/=' $globalPath`
    # 判断 是否存在 export
    if [ -z "$exportLineNum" ]; then
        # 不存在直接追加
        echo "export PATH=\"$installPath/$1/$2:\$PATH\"" >> $globalPath
        sureOk $? "GoGlobalSet $1"
    else
        # 存在则通过sed找到对应的行，然后通过awk进行分割然后再进行拼接，通过 -v 参数接收一个额外字符
        middlePath=$(echo `sed -n '/export PATH=/p' $globalPath`| awk -F '[ "]' -v v=$installPath/$1/$2  '{print $1,$2"\""$3":"v"\""}')
        # 通过 sed 替换掉指定的export行
        sed -i "${exportLineNum} s#.*#$middlePath#g" $globalPath
        sureOk $? "GoGlobalSet $1"
    fi  
}

function envGlobalSet {
    GoGlobalSet $nginxSoftName $nginxBinPath
    GoGlobalSet $pythonSoftName $pythonBinPath
}


# 隐藏nginx版本信息，需要在nginx源码包解压之后，编译之前执行
function nginxHidenVersion {
    cd $soureDownloadPath/$nginxPkgPath
    sed -i "s/${nginxVersion}/${nginxHidenVersion}/g" src/core/nginx.h
    sed -i "s/nginx\//${nginxServerName}\//g" src/core/nginx.h
    sed -i "s/\"NGINX\"/\"`echo ${nginxServerName}|tr '[a-z]' '[A-Z]'`\"/g" src/core/nginx.h
    sed -i "s/Server: nginx/Server: ${nginxServerName}/g" src/http/ngx_http_header_filter_module.c
    sed -i "s/<center>nginx</<center>${nginxServerName}</g" src/http/ngx_http_special_response.c
    sureOk $? "nginxHidenVersion"
}

# 初始化nginx初始配置
function initNginxConf {
    # 备份一下
    cp $nginxConfFile{,.bak_$(date +%F)}
    # 再清空
    cat /dev/null > $nginxConfFile
    cat >>$nginxConfFile<<EOF
worker_processes  $(grep "cpu cores" /proc/cpuinfo |awk '{print $4}');
events {
    worker_connections  1024;
}
http {
	include       mime.types;
	default_type  application/octet-stream;
	sendfile        on;
	keepalive_timeout  65;
	include extra/*.conf;
}
EOF
    # 创建存放虚拟主机目录，所有的虚拟主机存放在这个目录
    mkdir -p $installPath/$nginxSoftName/conf/extra
    sureOk $? "initNginxConf"
}

function main_UniversitySalaryRunEnv {
    envYumRelayPkg
    envAddRunUser
    envPkgDownload
    envUntarPkg
    nginxHidenVersion
    envConfigure
    envMake
    envMakeInstall
    envCreateSoftLink
    envGlobalSet
    initNginxConf
    
}
main_UniversitySalaryRunEnv
#sureOk $? "UniversitySalaryRunEnv"


function AliyunPipConf {
    [ -d $HOME/.pip ] || {
        mkdir $HOME/.pip -p
        sureOk $? "init .pip dir"
    }
    cd $HOME/.pip
    echo -e "[global]\ntrusted-host=mirrors.aliyun.com\nindex-url=http://mirrors.aliyun.com/pypi/simple/" > pip.conf
    sureOk $? "AliyunPipConf"
}
AliyunPipConf

function pyVitrualenvInstall {
    . $globalPath
    pip3 install $pythonVirtualPkg &> /dev/null
    sureOk $? "pyVitrualenvInstall"
}
pyVitrualenvInstall

function createPyVitrualenv {
    [ -d $vitrualEnvPath ] || {
        mkdir -p $vitrualEnvPath
        sureOk $? "init vitrualEnvPath"
    }
    cat >>$userBashConf<<EOF
export VIRTUALENV_USE_DISTRIBUTE=1
export WORKON_HOME=$vitrualEnvPath
export VIRTUALENVWRAPPER_PYTHON=$installPath/$pythonSoftName/$pythonBinPath/python3.6
. $installPath/$pythonSoftName/$pythonBinPath/virtualenvwrapper.sh
export PIP_VIRTUALENV_BASE=\$WORKON_HOME
export PIP_RESPECT_VIRTUALENV=true
EOF
    sureOk $? "createPyVitrualenv"
}
createPyVitrualenv

function persionPyVirtualCmdAlias {
    sed -i "9i alias mkenv='mkvirtualenv'\nalias rmenv='rmvirtualenv'\nalias outenv='deactivate'" $userBashConf
    sureOk $? "persionPyVirtualCmdAlias"
}
persionPyVirtualCmdAlias

function initPythonVirtualEnv {
   AliyunPipConf
   pyVitrualenvInstall
   createPyVitrualenv
   persionPyVirtualCmdAlias
   
}
initPythonVirtualEnv
# sureOK $? "initPythonVirtualEnv"

# 安装数据库

# 是否安装源, 没有则安装
# mysqlRepoConf mysqlRepoUrlOs6 mysqlRepoUrlOs7
function initMysqlRepo {
    [ -f $1 ] || {
        if [ $CentosVersion == "6" ]; then
            rpm -ivh $2 &> /dev/null
            sureOk 0 "initMysqlRepo"
        else
            rpm -ivh $3 &> /dev/null
            sureOk 0 "initMysqlRepo"
        fi
    }
}
# initMysqlRepo

# 安装mysql
# mysqlServer
function mysqlInstall {
    yum install -y $1 &> /dev/null
    sureOk $? "mysqlInstall"
}
# mysqlInstall

# 初始化mysql配置数据库
# mysqlConf serverRune
function initmysqlConf {
    \cp $1{,.$(date +%F)}
    cat /dev/null > $1
    cat >>$1<<EOF
[mysqld]
user=mysql
character_set_server=$2
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
symbolic-links=0
[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
EOF
    sed -i "4a character_set_server=$serverRune" $mysqlConf && sed -i "4a init_connection='$initCmd'" $mysqlConf
    sureOk $? "mysqlConf"
}


function mysqlYumInstall {
    mysqlRepoUrlOs6="https://repo.mysql.com//mysql57-community-release-el6-11.noarch.rpm"
    mysqlRepoUrlOs7="https://repo.mysql.com//mysql57-community-release-el7-11.noarch.rpm"
    mysqlRepoConf="/etc/yum.repos.d/mysql-community.repo"
    mysqlConf="/etc/my.cnf"
    mysqlServer="mysql-community-server"
    serverRune="utf8"

    initMysqlRepo $mysqlRepoConf $mysqlRepoUrlOs6 $mysqlRepoUrlOs7
    mysqlInstall $mysqlServer
    initmysqlConf $mysqlConf
}
# mysqlYumInstall

# 下载项目
function gitCloneUniversitySalaryMS {
    cd /
    echo $1
    git clone $1
    sureOk $? "gitCloneUniversitySalaryMS"
    chown -R $nginxRunUser.$nginxRunUser $2
}

# 初始化项目需要的虚拟环境
function iniUniversitySalaryMSPythonEnv {
    . $globalPath
    . $HOME/.bashrc
    mkvirtualenv $1  &> /dev/null
    sureOk $? "initUniversitySalaryMSPythonEnv"
}

# 进入虚拟环境安装相关依赖
function installPythonRelayPkg {
    pip3 install uwsgi
    . $userBashConf &>  /dev/null
    . $globalPath &>  /dev/null
    cd $2
    workon $1
    pip3 install -r requirements.txt
    sureOk $? "installPythonRelayPkg"
}

# 使用 uwsgi启动项目
function uwsgiStartUniversitySalaryMS {
    echo "uwsgi --ini $1 --uid $(id -u $2)" >> $onbootFile
    sureOk $? "add uwsgi to onboot"
    . $globalPath
    uwsgi --ini $1 --uid $(id -u $2) &
    sureOk $? "uwsgiStartUniversitySalaryMS"
}

# 配置项目nginx配置并且启动nginx
function startNginx {
    ln -s $1/USMS_nginx.conf $installPath/$nginxSoftName/conf/extra/USMS_nginx.conf
    sureOk $? "init soft link"
    $installPath/$nginxSoftName/$nginxBinPath/nginx
    sureOk $? "start nginx"
    echo "$installPath/$nginxSoftName/$nginxBinPath/nginx" >> $onbootFile
    sureOk $? "add nginx to onboot"
}

function UniversitySalaryMSOnlineEnv {
    UniversitySalaryMSGitUrl="https://github.com/jia2jiayuan/UniversitySalaryMS.git"
    UniversitySalaryMSEnvName="UniversitySalaryMS"
    UniversitySalaryMSPath="/UniversitySalaryMS"
    uwsgiConfPath="${UniversitySalaryMSPath}/USMS_uwsgi.ini"
    
    gitCloneUniversitySalaryMS $UniversitySalaryMSGitUrl $UniversitySalaryMSPath
    iniUniversitySalaryMSPythonEnv $UniversitySalaryMSEnvName
    installPythonRelayPkg $UniversitySalaryMSEnvName $UniversitySalaryMSPath
    startNginx $UniversitySalaryMSPath
    uwsgiStartUniversitySalaryMS $uwsgiConfPath $nginxRunUser
}
UniversitySalaryMSOnlineEnv
