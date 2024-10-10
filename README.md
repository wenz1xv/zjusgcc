# 舟山校区电量查询

通过“浙大后勤”微信公众号的接口，采集寝室用电信息。

# 配置
在configuration.yaml中，增加配置如下：
```yaml
homeassistant-sgcc:
  certificate: 'X' #此为微信公众号中抓取的certificate
  roomtag: 'X' #此为微信公众号中抓取的roomtag
```
重新启动Home Assistant
安装vertical-stack后，在卡片页添加以下内容
```
type: vertical-stack
cards:
  - type: entities
    entities:
      - entity: sensor.address
      - entity: sensor.allowance
      - entity: sensor.month_bill
      - entity: sensor.month_elec
      - entity: sensor.price
    title: 寝室
  - type: custom:flex-table-card
    title: 过去12个月用电情况
    entities:
      include: sensor.history*
    columns:
      - name: 月份
        data: name
      - name: 用电量
        data: state
      - name: 电费
        data: consume_bill
```


## 传感器
包含的传感器

| entity_id形式 | 含义 | 属性 | 备注 |
| ---- | ---- | ---- | ---- |
| sensor.address | 寝室地址 |
| sensor.allowance | 电费余额 |
| sensor.month_bill | 本月电费 |
| sensor.month_elec| 本月用电量 |
| sensor.price| 电价 |