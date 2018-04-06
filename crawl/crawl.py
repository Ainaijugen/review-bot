import os
import platform
import re
import utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from task import tasks

if platform.platform().lower().find("linux") != -1:
    from pyvirtualdisplay import Display

    display = Display(visible=0, size=(800, 800))
    display.start()
print(platform.platform())

params = {"confident_rate": 0.8, "page_size": 20, "attr_number": 8, "counts_per_attr": 2048, "item_per_page": 44}


def getsource(url, times):
    print(url)
    if times == 3:
        return ""
    # browser = webdriver.PhantomJS(executable_path="./phantomjs/bin/phantomjs")
    chrome_options = Options()
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    if platform.platform().lower().find("linux") != -1:
        browser = webdriver.Chrome(executable_path="chromedriver")
    else:
        browser = webdriver.Chrome(executable_path="./chromedriver")
    browser.set_page_load_timeout(10)
    try:
        browser.get(url)
        ans = str(browser.page_source)
        browser.close()
    except:
        browser.close()
        return getsource(url, times + 1)
    return ans


class Crawl:
    def __init__(self, tier1, tier2, i, j):
        self.attr2feature = dict()
        self.attr2feedback = dict()
        self.tiers = [tier1, tier2]
        self.attr_finished = []
        self.token = utils.GetToken()
        self.counts = 0
        self.tiers_id = [i, j]

    def crawl_id(self, item_id):
        feed_url = "https://rate.taobao.com/feedRateList.htm?auctionNumId=%s&currentPageNum=%d&pageSize=20&rateType=&orderType=sort_weight&attribute=%s&sku=&hasSku=false&folded=0&callback=jsonp_tbcrate_reviews_list"
        map_url = ("https://rate.taobao.com/detailCommon.htm?auctionNumId=%s&callback=json_tbc_rate_summary" % item_id)
        content = getsource(map_url, 0)
        item = re.search("count\":", content)
        attr_list = []
        attr_count = dict()
        while item:
            content = content[item.end():]
            try:
                count = int(content[:re.search(",", content).start()])
            except:
                break

            item = re.search("attribute\":\"", content)
            content = content[item.end():]
            attr = content[:re.search("\"", content).start()]

            item = re.search("title\":\"", content)
            content = content[item.end():]
            title = content[:re.search("\"", content).start()]

            item = re.search("value\":", content)
            content = content[item.end():]
            value = int(content[:re.search("\}", content).start()])

            if value > 0:
                self.attr2feature[attr] = title
                attr_list.append(attr)
                attr_count[attr] = int(count * params["confident_rate"])

            item = re.search("count\":", content)
        print(attr_list)
        for attr in attr_list:
            if attr not in self.attr2feedback:
                self.attr2feedback[attr] = []
            attr_count[attr] = min(attr_count[attr], params["counts_per_attr"] - len(self.attr2feedback[attr]))
            if attr_count[attr] == 0:
                continue
            i = 1
            while attr_count[attr]:
                content = getsource(feed_url % (item_id, i, attr), 0)
                item = re.search("content\":\"", content)
                if item is None:
                    break
                while item:
                    content = content[item.end():]
                    try:
                        feedback = content[:re.search("\",\"", content).start()]
                    except:
                        break
                    content = content[re.search("\",\"", content).end():]
                    if content[:6] == "rateId":
                        feedback = self.token.tokenlize(utils.clean_string(feedback))
                        # print(feedback)
                        self.attr2feedback[attr].append(feedback)
                        attr_count[attr] -= 1
                        self.counts += 1
                        if attr_count[attr] == 0:
                            break
                    item = re.search("content\":\"", content)
                i += 1
            if len(self.attr2feedback[attr]) == params["counts_per_attr"]:
                self.attr_finished.append(attr)
                print("finished: ", self.attr2feature[attr])
        print("collected: %d\n" % self.counts)
        for x in self.attr2feedback:
            print(self.attr2feature[x] + ": ", len(self.attr2feedback[x]))

    def crawl(self, i=0):
        i *= params["item_per_page"]
        while len(self.attr_finished) < params["attr_number"] and i < params["item_per_page"] * 5:
            search_url = "https://s.taobao.com/search?q=%s+%s&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&sort=sale-desc&initiative_id=staobaoz_20180406&s=%d" % (
                self.tiers[0], self.tiers[1], i)
            content = getsource(search_url, 0)
            for _ in range(params["item_per_page"]):
                # print(content)
                content = content[re.search("nid\":\"", content).end():]
                item_id = content[:re.search("\"", content).start()]
                content = content[re.search("\"isTmall\":", content).end():]
                if content[0] == "f":
                    print(item_id)
                    self.crawl_id(item_id)
                    if len(self.attr_finished) >= params["attr_number"]:
                        break
            i += params["item_per_page"]
            self.save()
            f = open("./data/%d_%d/is_finish.txt" % (self.tiers_id[0], self.tiers_id[1]), "w")
            f.write("%d" % (i / params["item_per_page"]))
            f.close()
        while len(self.attr_finished) < params["attr_number"]:
            Max = 0
            add = None
            for x in self.attr2feedback:
                if x not in self.attr_finished:
                    if Max < len(self.attr2feedback[x]):
                        Max = len(self.attr2feedback[x])
                        add = x
            assert add is not None
            self.attr_finished.append(add)
        print("finished! ", self.attr_finished)

    def save(self, is_remove=False):
        # Token里面的大字典， 包含x个attr的两个大字典（一个是to feature，一个是to feedback）
        utils.save(self.token.word2id_dict, "%d_%d" % (self.tiers_id[0], self.tiers_id[1]), "word2id", True)
        # print(self.token.word2id_dict)
        if is_remove:
            self.attr_finished = self.attr_finished[:params["attr_number"]]
            remove = []
            for x in self.attr2feature:
                if x not in self.attr_finished:
                    remove.append(x)
            for x in remove:
                self.attr2feature.pop(x, None)
                self.attr2feedback.pop(x, None)
        utils.save(self.attr2feedback, "%d_%d" % (self.tiers_id[0], self.tiers_id[1]), "attr2feedback", True)
        utils.save(self.attr2feature, "%d_%d" % (self.tiers_id[0], self.tiers_id[1]), "attr2feature", True)
        if is_remove:
            f = open("./data/%d_%d/is_finish.txt" % (self.tiers_id[0], self.tiers_id[1]), "w")
            f.write("%d" % -1)
            f.close()

    def load(self):
        self.token.word2id_dict = utils.load("%d_%d" % (self.tiers_id[0], self.tiers_id[1]), "word2id")
        self.attr2feedback = utils.load("%d_%d" % (self.tiers_id[0], self.tiers_id[1]), "attr2feedback")
        self.attr2feature = utils.load("%d_%d" % (self.tiers_id[0], self.tiers_id[1]), "attr2feature")
        print(self.token.word2id_dict)
        print(self.attr2feedback)
        print(self.attr2feature)

    def resume(self, i):
        self.load()
        for x in self.attr2feedback:
            if len(self.attr2feedback[x]) == params["counts_per_attr"]:
                self.attr_finished.append(x)
        self.token.resume()
        self.crawl(i)


for i in range(len(tasks)):
    for j in range(len(tasks[i][1])):
        crawl = Crawl(tasks[i][0], tasks[i][1][j], i, j)
        if not os.path.exists("./data/%d_%d" % (i, j)):
            crawl.crawl()
            crawl.save(True)
        else:
            try:
                f = open("./data/%d_%d/is_finish.txt" % (i, j), "r")
                checkpoint = int(f.readline().strip())
                if checkpoint > 0:
                    crawl.crawl(checkpoint)
                    crawl.save(True)
            except:
                crawl.crawl()
                crawl.save(True)
        crawl.load()

'''
    https://rate.taobao.com/feedRateList.htm?auctionNumId=39595400262&currentPageNum=1
    https://rate.taobao.com/feedRateList.htm?auctionNumId=560911808609&currentPageNum=1&pageSize=20&rateType=&orderType=sort_weight&attribute=620-11&sku=&hasSku=false&folded=0&callback=jsonp_tbcrate_reviews_list
    https://rate.taobao.com/detailCommon.htm?auctionNumId=536738885088&callback=json_tbc_rate_summary
    https://s.taobao.com/search?q=%s+%s&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&sort=renqi-desc
    
    
'''
