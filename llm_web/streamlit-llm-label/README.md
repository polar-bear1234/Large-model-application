#### 功能：

    - 利用大模型（包括GPT4-Turbo、GPT3.5-Turbo、LlaMA2-7B、Qwen-7B）对告警数据打标签，支持：
		- 设定标签范围
		- 不设定标签范围

#### 环境：

    - python3.8以上（版本不要太老就行）
	- 执行命令，配置python环境： pip install -r requirements.txt

#### 启动：

    - 需要开外网（配环境的时候不要开外网）
	- 在该目录下执行命令： streamlit run streamlit_gpts.py


#### 测试告警用例：

应用系统业务告警：[2023-04-23T18:51:00.000+08:00]财资管理系统_财资web（江北）的响应时间发生突增异常，当前值为:6.869377,高于动态基线值:1.884699,同时对应交易量和响应率发生突变异常，请注意!  （交易响应变慢）

基金代销响应时间连续2分钟大于200ms。       （交易响应变慢）

19:38 19:39交易码:SCO006(初始化用户信息 (ECBPSC2001缓存))，1分钟业务成功率低，闻值: 90.0%，实际值: 54.443%.     （交易成功率低）

CPU和内存监控.CPU使用率 异常 CPU使用率:95%大于90%。         （cpu使用率高）

Swap交换空间使用率超过60%，请关注！,最新值60 %,【Swap:系统负责人处理】。          （内存使用率高）

sqifsceph02 Disk busy time rate is more than 90% on sde。               （磁盘IO繁忙）

LINUX_DISK_Hi::操作系统磁盘{#DEVICE}的I/O平均请求时延大于100ms，I/O负载较大请关注！     （磁盘IO延迟高）

WAS服务AppSrv01#server1的JVM空闲量小于1048576 B,最新值41.44 MB。             （jvm使用率高）

oacloud12aY_L3DB3，Out of memory detected in /u01/app/diag/rdbms/l3db/L3DB3/alert/log.xml at time/line number: Tue May 30 03:20:21 2023/115991.，告警类型:CRITICAL。      （内存溢出）。
