# Auto-Make-Money
 An easy tool to help investors from SH&SZ Stock Market to apply for convertible bonds automatically.



*Attention: Since this is for Chinese investors, instructions below were all written in Simplified Chinese.*



### 部署 & 使用

同花顺下单客户端提前做好以下设置，不然会导致下单时价格出错以及客户端超时锁定：

- 系统设置 > 界面设置: 界面不操作超时时间设为 0
- 系统设置 > 交易设置: 默认买入价格/买入数量/卖出价格/卖出数量 都设置为 空

同时客户端不能最小化也不能处于精简模式；

**注意：请安装VNC进行远程控制，原生远程桌面在断开连接一段时间后桌面会休眠，导致pywin32找不到窗口。**

1. 登录同花顺，打开委托平台，登录，按上述调整设置；
2. 在config.py中配置xiadan.exe的路径，一般在同花顺可执行文件同目录下；
3. 每日在交易时段（9:30~15:00）执行main.py；
4. （可选）在ServerChan申请SCKey并绑定微信，这样每天微信都会给你推送当日可转债申购情况啦！
5. 中签后券商会给发短信，抽签日一般是T+2，中签当日16点前保证账户有1000块余额就OK，中签后查询一下预期上市时间，经统计上市首日卖出收益最高。