from bs4 import BeautifulSoup

#1.tag:标签
#2.NavigableString:标签里的内容
#3.attrs:属性
#4.BeautifulSoup:表示整个文档
#5.comment；特殊的NavigableString，输出的内容不包含特殊符号
'''1.find_all:字符串过滤：会查找与字符串完全匹配的内容
   2.正则表达式搜索：
   使用search（）方法来匹配内容
   t_list=bs.find_all(re.compile(''a''))
   print(t_list)
   方法：传入一个函数（方法），根据函数的要求来搜索
   def name_is_exists(tag):
       return tag.has_attr('name')
    t_list=bs.find_all(name_is_exists)
    
    3.参数选择
    t_list=bs.find_all(id="head")
    t_list=bs.find_all(class_True)
    for item in t_list:
        print(item)
    4.文本参数：
    for item in t_list:
    t_list=bs.find_all(text="hao123"，“地图”)
    t_list=bs.find_all(text=re.compile("\d")#查找包含特定文本的内容
    
    5.limit：限定个数
    
    6.选择器
    t_list=bs.select('title')  #通过标签查找
    t_list=bs.select('.mnav')  #通过类名来查找
    t_list=bs.select('#u1')    #通过id来查找    
    t_list=bs.select('a[class='bri']')    #通过属性来查找
    t_list=bs.select("head>title")  #通过子标签来查找











'''