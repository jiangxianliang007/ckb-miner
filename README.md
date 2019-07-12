# ckb-miner
批量部署 ckb 挖矿程序的脚本

## 开发环境
```
Ubuntu 18.04.2
Python 3.6.8
```
## 安装依赖
```
apt-get update
apt install -y python3-pip 
pip3 install paramiko
```
## 创建钱包

请见 [官方手册](https://docs.nervos.org/getting-started/wallet)

## 运行ckb 同步节点

请见 [官方手册](https://docs.nervos.org/getting-started/run-node)

同步节点需要将ckb.toml 配置中 listen_address 值改成 0.0.0.0:8114 ,同时确保8114端口防火墙允许外部服务器访问

## 自定义配置修改
脚本中变量 username、passwd、remotedir、iplist、miner_threads、ckb_node_ip 运行时请自行修改。
```
username      # 登录到挖矿服务器的用户
passwd          # 登录到挖矿服务器的用户密码
remotedir       # 远程服务器ckb运行目录
iplist                # 远程服务器列表 
miner_threads    # 运行的ckb miner 线程数，最好比服务器CPU核数少1 
ckb_node_ip      # ckb 同步节点IP
```
## 运行脚本
```
python3 run_ckb_miner.py 

1 run_ckb_miner
2 kill_ckb_miner
3 quit

输入1：运行ckb 挖矿
输入2：关闭ckb 挖矿
```

