from bs4 import BeautifulSoup  
import requests  
global num  
num=0  
def getList(url):  
    help=[]  
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'}  
    #get从网页获取信息  
    res = requests.get(url,headers=headers)  
    #解析内容  
    soup = BeautifulSoup(res.text,'html.parser')  
    info_divs = soup.select('.NavList a')#寻找子网页链接  
    if info_divs==[]:  
        return []  
    for j in info_divs:#存储所有子网页链接  
         text=str(j)  
         help.append(text.split('"')[1])  
    return help  
  
#爬取详细信息  
def helpinfo(url):  
    msg =[]  
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'}  
    res = requests.get(url,headers=headers)  
    soup = BeautifulSoup(res.text,'html.parser')  
    if res.text==[]:  
        return []  
   
    info_divs = soup.select('p')#寻找需要的文字内容  
    for j in info_divs:  
        t=str(j).split("<p")  
        if t[1][0]=='>':  
             tt=t[1][1:]  
             tttt=tt.split("</p>")#精化文字内容  
             msg.append(tttt[0])  
     
    return msg  
   
#将信息写入txt文件  
def writeFile(info):  
    if  info[0][0]=='['or info==[] or info[0][0]=='<'or info[0]==[]:  
     return#抛弃一些无效值  
    global num  
    title='E:\\ruanxu1\\result_'+str(num)+'.txt'#存储位置  
    f = open(title,'a',encoding='utf8')  
    f.write(info+'\n')  
    print(info)  
    f.close()  
    num=num+1  
  
def changenavigate(link):#加前缀1  
   t1=str(link).split('/')  
   tt=""  
   for j in t1:  
       if j!="..":  
           if j!="topic":  
                tt+="/"+str(j)  
   res="https://help.eclipse.org/2019-09/topic"+tt  
   return res  
  
def changenavigate1(link):#加前缀2  
   t1=str(link).split('/')  
   tt=""  
   for j in t1:  
       if j!="..":  
           tt+="/"+str(j)  
   res="https://help.eclipse.org/2019-09/nav"+tt  
   
   return res  
  
def get(link):  
 helps=helpinfo(link)  
 if helps!=[]:  
    for help in helps:  
          writeFile(str(help)) #保存网页内容  
  
def spider(url):  
    list =getList(url)  
    if list==[]:#没有子网页了  
       link=url  
       if link[0]=='h':  
          get(link)  
    else:#可以往下追寻，递归爬取子网页  
     for j in list:  
        link = j  
        sublink=changenavigate(link)  
        sublink1=changenavigate1(link)  
        spider(sublink)  
        spider(sublink1)  
         
  
  
               
#主函数  
def main():  
   print('-----分隔符','-------')      
   url ='https://help.eclipse.org/2019-09/nav/1'  
   #顶端网址  
   spider(url)  
          
   
if __name__ == '__main__':  
    main()  
