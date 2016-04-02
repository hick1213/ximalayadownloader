#coding=utf-8
import os
import urllib
import sys
import json
sys.path.append("..")
import re
import urllib2

class Xmly():

    URL_PRIFIX = "http://www.ximalaya.com/tracks/"
    def getJsonUrl(self,url):
        result = url.split('/')
        return result[len(result)-1]+".json"
    def getVoiceUrl(self,html):
        # print html
        jsonStr = json.loads(html)
        return jsonStr["title"].encode('utf-8'),jsonStr["play_path"]

    def download(self,url,filepath):
        jsonUrl = self.URL_PRIFIX + self.getJsonUrl(url)
        html = self.getHtml(jsonUrl)
        voiceTitle,voiceUrl = self.getVoiceUrl(html)
        self.downLoadFile(voiceUrl,filepath,voiceTitle+'.m4a')

    def getHtml(self,url):
        # print url
        response = urllib2.urlopen(url)  
        html = response.read()  
        # print html
        # with open('s.txt',"wb") as f:
        #   f.write(html)
        #   f.close()
        return html

    def changeStatus(self,status):
      sys.stdout.write(status + "\r")
      sys.stdout.flush()

    def downLoadFile(self,url,filepath,fileName):
        # 去掉空格否则转换格式会出问题
        fileName = fileName.replace(" ","")
        if os.path.exists(os.path.splitext(os.path.join(filepath,fileName))[0] + ".mp3"):
          print '已经存在:' + fileName
          return
        self.changeStatus("Downloading...")
        f = urllib2.urlopen(url) 
        if not os.path.exists(os.path.join(filepath,fileName)):
          with open(os.path.join(filepath,fileName), "wb") as code:
            code.write(f.read()) 
        self.change2MP3(os.path.join(filepath,fileName))

    def downloadalbum(self,url,filepath):
        self.changeStatus("Start get album list...")
        # 将正则表达式编译成Pattern对象
        pattern = re.compile(r'<a class="title"[^>]*')
 
        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
        ret = self.getHtml(url)
        # print ret
        match = pattern.findall(ret)
        for name in match:
          # print name
          # items = name.split(" ")
          # path = items[2].replace("href=\"","")
          # path = path.replace("\"","")
          # # print path
          # title = items[4].replace("title=\"","")
          # title = title.replace("\"","")
          # print title

          patternTmp = re.compile(r'href=[^\s]*')
          matchTmp = patternTmp.findall(name)
          path = matchTmp[0].replace("href=\"","")
          path = path.replace("\"","")

          patternTmp = re.compile(r'title=[^“]*')
          matchTmp = patternTmp.findall(name)
          
          title = matchTmp[0].replace("title=\"","")
          title = title.replace("\"","")


          self.download("http://www.ximalaya.com" + path,filepath)
        # if match:
        #   # 使用Match获得分组信息
        #   print match.group()

        # else:
        #   print 'not find'
 
    def change2MP3(self,file):
        self.changeStatus("change format...")
        if os.path.splitext(file)[1] != "mp3":
          cmd = "ffmpeg -i {0} {1}"
          # print file 
          # print os.path.splitext(file)[0]
          cmd = cmd.format(file,os.path.splitext(file)[0] + ".mp3")
          print cmd
          os.system(cmd)
          os.remove(file)

if __name__ == '__main__':
    # url = "http://www.ximalaya.com/1000623/sound/1035320"
    xmly = Xmly()
    # xmly.download(url,".")
    xmly.downloadalbum("http://www.ximalaya.com/1000623/album/209295",os.getcwd())
    # xmly.download("http://www.ximalaya.com//1000623/sound/1043163",os.getcwd())


