# 舟山校区电量查询

通过“浙大后勤”微信公众号的接口，采集寝室用电信息。


# 配置
在configuration.yaml中，增加配置如下：
```yaml
homeassistant-sgcc:
  certificate: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' #此为微信公众号中抓取的certificate
  roomtag: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' #此为微信公众号中抓取的roomtag
```
重新启动Home Assistant

## 传感器
包含的传感器

| entity_id形式 | 含义 | 属性 | 备注 |
| ---- | ---- | ---- | ---- |
| sensor.XXXXXXXXXX_balance | 电费余额 | last_update - 网端数据更新时间 |
| sensor.XXXXXXXXXX_current_level | 当前用电阶梯(峰平谷用户无此项) |
| sensor.XXXXXXXXXX_current_level_consume | 当前阶梯用电(峰平谷用户无此项) |
| sensor.XXXXXXXXXX_current_level_remain | 当前阶梯剩余额度(峰平谷用户无此项) |
| sensor.XXXXXXXXXX_current_pgv_type | 当前电价类别(阶梯用户无此项) | |可能的值:峰、平、谷、尖峰(?)|
| sensor.XXXXXXXXXX_current_price | 当前电价 |
| sensor.XXXXXXXXXX_year_consume | 本年度用电量 |
| sensor.XXXXXXXXXX_year_consume_bill | 本年度电费 |
| sensor.XXXXXXXXXX_history_* | 过去12个月用电 | name - 月份<br/>consume_bill - 该月电费| \*取值为1-12<br/> |

其中XXXXXXXXXX为北京国电用户户号

# 示例
历史数据采用[flex-table-card](https://github.com/custom-cards/flex-table-card)展示
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
