# Auto-Make-Money
An easy tool to help investors from Shanghai/Shenzhen Stock Market to apply for new-listed convertible bonds automatically.
Blog written in Chinese: [Click Here](https://mrxiao.net/kzz-auto.html)

*Attention: Since this is for Chinese investors, instructions below were all written in **Simplified Chinese.***

## 公告与注意事项
**注意，2020年10月22日更新，近日收到银河证券通知，“自2020年10月26日起，未签署《风险揭示书》的普通投资者，无法通过我司进行申购或买入可转债，已持有相关可转债的投资者可以选择继续持有、转股、回售或者卖出。”，应为证监会强制要求，请各位注意接听券商提醒来电。**

**经我了解，自2020年4月28日开始正式实施创业板新规定，要求个人投资者必须满足两年的A股交易经验，且需前20个交易日日均资产不少于10万元，先前已开通创业板账户权限不受影响；这样一来，之前未开通创业板权限且不符合新条件的投资者将无法参与创业板可转债打新，请悉知。**


## 部署 & 使用
### 同花顺交易客户端设置
同花顺下单客户端提前做好以下设置，不然会导致下单时价格出错以及客户端超时锁定：

- 系统设置 > 界面设置: 界面不操作超时时间设为 0
- 系统设置 > 交易设置: 默认买入价格/买入数量/卖出价格/卖出数量 都设置为 空

同时客户端**不能最小化也不能处于精简模式**；

**注意：对没有实体显示器的云服务器用户，可以参考以下方法保持桌面活跃；原生远程桌面在断开连接一段时间后桌面会休眠，导致pywinauto找不到窗口。**

**2021年01月20日更新: 新发现了不需要通过第三方远控软件保持桌面活跃的方法，详见[《Windows服务器 断开远程桌面RDP后保持桌面活跃(active)的方法》](https://mrxiao.net/disconnect-rdp-keep-windows-desktop-active.html)。**

### 使用步骤
1. 登录同花顺，打开委托平台，登录，按上述调整设置；
2. 在config.py中配置xiadan.exe的路径，一般在同花顺可执行文件同目录下；
3. 如果正处于交易时间段，可以使用`python main.py test`验证配置文件的有效性；通过`python main.py cron`开启定时任务；
4. （可选）在ServerChan申请SCKey并绑定微信，这样每天微信都会给你推送当日可转债申购情况啦！
5. 中签后券商会给发短信，抽签日一般是T+2，中签当日16点前保证账户有1000块余额就OK，中签后查询一下预期上市时间，经统计上市首日卖出收益最高。有开发能力的，可以通过[https://api.mrxiao.net/kzz](https://api.mrxiao.net/kzz)查询到当日可申购与上市可转债的信息，并实现自动化的可转债申购套利；
