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
    #print(soup);
    info_divs = soup.select('.logsubject')#寻找子网页链接  
    if info_divs==[]:  
        return []  
    for j in info_divs:#存储所有子网页链接  
         text=str(j)  
         help.append(text.split('"')[3])  
    return help  

def getPage(url):  
    help=[]  
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'}  
    #get从网页获取信息  
    res = requests.get(url,headers=headers)  
    #解析内容  
    soup = BeautifulSoup(res.text,'html.parser') 
    #print(soup);
    info_divs = soup.select('.logheader .logsubject')#寻找子网页链接  
    if info_divs==[]:  
        return []  
    nn=0
    for j in info_divs:#存储所有子网页链接  
        t1=str(j).split('>')[2]
        t1=t1.split('<')[0]
        help.append(t1)
   
    return help  
  
#爬取详细信息  
def helpinfo(url,name):  
    msg =[]  
    msg1 =[]  
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'}  
    res = requests.get(url,headers=headers)  
    soup = BeautifulSoup(res.text,'html.parser')  
    if res.text==[]:  
        return []  
   
    
    info_divs = soup.select('.commit-info .right')#寻找需求时间
    nn=0;
    t=[]
    for j in info_divs: 
        text=str(j)  
        t=text.split('"')[2]
        t1=t.split(' ')
        t2=t1[0]+"\t"+t1[1]
        msg.append(t2);

    info_divs = soup.select('.diff')#寻找需求更改的代码 
    nn=0;
    t=[]
    for j in info_divs: 
        text=str(j)  
        t=text.split('"')
        #print(t);
        for t1 in t:
            if t1=='hunk' or t1=='ctx' or t1=='del' or t1=='add':
                msg.append(t[nn+1]);
            if t1=='head':
                temp=t[nn+1]
                t2=temp.split(' ')
                t2[2]=t2[2].replace("a/","\n原文件: ")
                t2[3]=t2[3].replace("b/","新文件: ")
                t3='>'+t2[2]+' \n'+t2[3]
                msg.append(t3)
            nn=nn+1
    number=0
    msg1.append("需求名称: "+name)
    print(name)
    for j in msg: 
        text=str(j)
        t=text.split('<')[0]
        if len(t.split('>'))>1:
            t1=t.split('>')[1]
        t1=t1.replace("&lt;",'<')
        t1=t1.replace("&gt;",'>')
        t1=t1.replace("@@",'位置: ',1)
        t1=t1.replace("@@",' ',1)
        
        if number==0:
            t1="创建时间: "+t1
        if number==1:
            t1="修改时间: "+t1
        msg1.append(t1)
        number=number+1

    result=""
    for j in msg1: 
        text=str(j)
        #print(text)
        result=result+text+'\n'
        #print(result)
    return result  
   
#将信息写入txt文件  
def writeFile(info):  
   
    global num  
    title='E:\\ruanxu1\\result2.txt'#存储位置  
    f = open(title,'a',encoding='utf8')  
    f.write('---------------------------'+str(num)+'---------------------------\n'+info+'\n')  #需求编号
    #print(info)  
    f.close()  
    num=num+1  
  
def changenavigate(link):#加前缀1  
 
   res="https://git.eclipse.org"+link
   return res  
  
 
  
def get(link,name):  
 helps=helpinfo(link,name)  
 writeFile(str(helps)) #保存网页内容  
  
def spider(url):
    name=getPage(url)#获取需求名称
    list =getList(url)  
    if list==[]:#没有子网页了  
       link=url  
      
    else:#可以往下追寻，递归爬取子网页  
     for i in range(len(list)):  
        link = list[i]  
        if link[0]=='/'and link[1]=='c':  
            sublink=changenavigate(link)  
            subspider(sublink,name[i]) 
            
def subspider(url,name):  
     get(url,name)  
    

      
def page(url): 
    spider(url)
    num=50
    for i in range(1,200):
        spider('https://git.eclipse.org/c/pde/eclipse.pde.ui.git/log/?ofs='+str(num*i)+'&showmsg=1')#翻页
   

  
  
               
#主函数  
def main():  
   print('-----分隔符','-------')      
   url ='https://git.eclipse.org/c/pde/eclipse.pde.ui.git/log/?showmsg=1'  
   #顶端网址  
   #spider(url) 
   page(url)
          
   
if __name__ == '__main__':  
    main()  
