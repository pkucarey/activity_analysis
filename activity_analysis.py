import sys  

import os
import jieba   
import numpy    #numpy计算包
import codecs   #codecs提供的open方法来指定打开的文件的语言编码，它会在读取的时候自动转换为内部unicode 
import pandas   #数据分析包
import matplotlib.pyplot as plt 
from wordcloud import WordCloud#词云包
from optparse import OptionParser  

USAGE = "usage:    python activity_analysis.py -i [input directory name] -o [output directory name] -k [top k]"  
total_segment=[]
stopwords=pandas.read_csv("stopwords.txt",index_col=False,quoting=3,names=['stopword'],sep="\t",encoding="utf8")#quoting=3全不引用
userStopWords=pandas.Series(['工作','活动'])

def words_stat(segment):
    words_df=pandas.DataFrame({'segment':segment})
    words_df.head()
    words_df=words_df[~words_df.segment.isin(stopwords.stopword)]
    words_df=words_df[~words_df.segment.isin(userStopWords)]
    words_stat=words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
    words_stat=words_stat.reset_index().sort_values(by="计数",ascending=False)
    return words_stat

def plot_stat(outputDir, words_stat, file_name, topK=100):
    wordcloud=WordCloud(font_path="simhei.ttf",background_color="white")
    wordcloud=wordcloud.fit_words(words_stat.head(topK).itertuples(index=False))
    plt.imshow(wordcloud)
    plt.savefig(outputDir + '/' + file_name.split("/")[-1].split(".")[0] + '.png', dpi=400)

def word_frequency(outputDir, file_name, topK=100):  
    file=codecs.open(file_name,'r')
    content=file.read()
    file.close()
    segment=[]
    segs=jieba.cut(content) #切词
    for seg in segs:
        if len(seg)>1 and seg!='\r\n':
            segment.append(seg)    
            total_segment.append(seg)
    
    plot_stat(outputDir, words_stat(segment), file_name)                

def main():    
    parser = OptionParser(USAGE)  
    parser.add_option("-i", dest="inputDir")  
    parser.add_option("-o", dest="outputDir")  
    parser.add_option("-k", dest="topK")  
    opt, args = parser.parse_args()   
    
    inputDir = opt.inputDir
    if inputDir is None:
        print(USAGE)
        sys.exit(1)
    
    if os.path.exists(inputDir) is False:
        print('input directory is not exist')
        
    outputDir = opt.outputDir
    if outputDir is None:
    	outputDir = inputDir + '/wordcloud/'
    
    if os.path.exists(outputDir) is False:
        os.mkdir(outputDir)
    
    topK = 100
    if opt.topK is not None:         
    	topK = int(opt.topK)

    files = os.listdir(inputDir)
    for file in sorted(files):
        file_path = os.path.join(inputDir, file)
        word_frequency(outputDir, file_path, topK)
    plot_stat(words_stat(total_segment), 'total')

main()
