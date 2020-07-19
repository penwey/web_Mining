# -*- coding: utf-8 -*-
import scrapy
from ScrapyTest.Utils import Liepin_Excel
from ScrapyTest.Utils import TimeHelper



class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    start_urls = ['https://www.liepin.cn/']

    def parse(self, response):
        urls = ['https://www.liepin.cn/zhaopin/?industries=&subIndustry=&dqs=050090&salary=&jobKind=&pubTime=&compkind=&compscale=&searchType=1&isAnalysis=&sortFlag=15&d_headId=13dfc96c55ab1f912020557afd4304eb&d_ckId=13dfc96c55ab1f912020557afd4304eb&d_sfrom=search_fp_bar&d_curPage=0&d_pageSize=40&siTag=uBwPJUVmv_V98y0J8OUR0g%7EfA9rXquZc5IkJpXC-Ycixw&key=%E9%A1%B9%E7%9B%AE%E7%BB%8F%E7%90%86']
        for url in urls:
            list0 = list()
            yield scrapy.Request(url, dont_filter=True, meta={'n': 1, 'list0': list0}, callback=self.parse2)

    def parse2(self, response):
        # 判断爬取次数，到达指定次数后停止
        n = response.meta['n']
        list0 = response.meta['list0']
        if n > 9:
            Liepin_Excel.file_create('C:\\Users\\Administrator\\ScrapyTest\\ScrapyTest\\Results\\results.xlsx', list0)
            self.crawler.engine.close_spider(self, '爬取完成关闭爬虫')
        else:
            n += 1
            """
            信息结构（信息总集）
            这种形式的xpath是因为页面采用了动态定位
            <script>
            window.tlg = {
                dataInfo: JSON.parse(decodeURIComponent("%7B%22head_id%22%3A%228db86d8395b3dbcae0675cb7bfc92f7b%22%2C%22ck_id%22%3A%22bce3fe552dd2e97096ecb8a7cbad1538%22%2C%22gen_cnt%22%3A0%2C%22total_cnt%22%3A15676%2C%22gen_flag%22%3A0%2C%22gen_posi%22%3A-1%2C%22gen_op%22%3A%5B%5D%2C%22so_cond%22%3A%7B%22keys%22%3A%22%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86%EF%BC%8C%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88%EF%BC%8C%E7%94%A8%E6%88%B7%E7%A0%94%E7%A9%B6%22%2C%22industrys%22%3A%22%22%2C%22dqs%22%3A%22050090%22%2C%22comp_kind%22%3A%22%22%2C%22comp_scale%22%3A%22%22%2C%22pubtime%22%3A%22%22%2C%22job_kind%22%3A%22%22%2C%22company%22%3A%5B%5D%7D%2C%22abtest_flag%22%3A%22job-no_login%22%2C%22abtest_flag_fe%22%3A%22abtest-page-c-0%22%2C%22job_ids%22%3A%5B%222_29604271%22%2C%222_28587613%22%2C%222_30023287%22%2C%222_30023029%22%2C%222_30022447%22%2C%222_30022257%22%2C%222_30019873%22%2C%222_30019575%22%2C%222_30018213%22%2C%222_30018173%22%2C%222_30018159%22%2C%222_30017851%22%2C%222_30017753%22%2C%222_30017695%22%2C%222_30016953%22%2C%222_30016801%22%2C%222_30015561%22%2C%222_30013411%22%2C%222_30013257%22%2C%222_30012831%22%2C%222_30006847%22%2C%222_30006493%22%2C%222_30005149%22%2C%222_30004625%22%2C%222_30003929%22%2C%222_30003893%22%2C%222_30003811%22%2C%222_30003265%22%2C%222_30002743%22%2C%222_30002061%22%2C%222_29997131%22%2C%222_29995389%22%2C%222_29995081%22%2C%222_29992871%22%2C%222_29986497%22%2C%222_29984767%22%2C%222_29983127%22%2C%222_29980715%22%2C%222_29976307%22%2C%222_29974989%22%5D%2C%22cur_page%22%3A0%2C%22page_size%22%3A40%2C%22as_from%22%3A%22search_fp_bar%22%7D")),
                exposure: [{
                    type: 'dynamic',
                    container: {
                        xpath: 'div.container/div/div.job-content/div.sojob-result',
                    },
                    xpath: 'div.container/div/div.job-content/div.sojob-result/ul.sojob-list/li'
                }]
            }
            </script>
            """
            all_content = response.xpath('//*/ul[@class="sojob-list"]/li/div')[0]
            # 获取对应元素
            job_title = all_content.xpath('//div[@class="job-info"]/h3/a/text()').extract()
            job_info_list = all_content.xpath('//div[@class="job-info"]/p[@class="condition clearfix"]/@title').extract()
            company = all_content.xpath('//div[@class="company-info nohover"]/p[@class="company-name"]/a/text()').extract()
            offer_time = all_content.xpath('//div[@class="job-info"]/p[@class="time-info clearfix"]/time/@title').extract()
            info_url = all_content.xpath('//div[@class="job-info"]/h3/a/@href').extract()
            # 创建字典
            for i in range(len(job_title)):
                item = dict()
                job_info = job_info_list[i].split('_')
                salary = job_info[0]
                area = job_info[1]
                education = job_info[2]
                working_seniority = job_info[3]
                item['job_title'] = job_title[i].replace('\r\n', '').replace('\t', '')
                item['salary'] = salary
                item['area'] = area
                item['education'] = education
                item['working_seniority'] = working_seniority
                item['company'] = company[i]
                item['offer_time'] = offer_time[i]
                item['info_url'] = info_url[i]
                print(item)
                item['create_time'] = TimeHelper.TimeHelper.getTime(self=None)
                list0.append(item)


            # 定位"下一个"按钮，在页码栏的倒数第二位
            next_href = response.xpath('//*/div[@class="pager"]/div/a[last()-1]/@href').extract()[0]
            next_url = 'https://www.liepin.com' + next_href
            print("下一页是: " + next_url)
            yield scrapy.Request(next_url, dont_filter=True, meta={'n': n, 'list0': list0}, callback=self.parse2)




