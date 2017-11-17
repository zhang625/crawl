# 新闻联播爬虫

## 功能介绍
  新闻联播的title和链接，并且将内容发送到指定邮箱，将每日的新闻联播内容储存到mongodb，储存内容是title和链接
## 代码布置
  1. 需要安装scrapy，我使用的版本是1.3.3，python版本是3.5.2
  2. 需要在setting里面配置数据库，详见scrapy文档
  3. 使用scrapy内置的邮件发送一直报错，所以使用了python的邮件模块，需要在newsSPider.py里面的_sendMail方法里进行配置
  4. newsCrawl.bat是批处理文件，将这个文件布置在windows的定时任务里面，爬虫会每天定时爬文件，文件的执行地址需要按照项目更改