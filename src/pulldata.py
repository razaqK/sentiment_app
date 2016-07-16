import json, requests, datetime

class Config:

    CONFIG_FILE = 'data/config/configuration.txt'
    COMPANY_FILE = 'data/listofcompanies.txt'
    SPLITTER = '='

    def __init__(self):
        get_credentials = self.read_config()
        self.id = get_credentials[1]
        self.secret = get_credentials[0]

    def read_data(self, filename):
        with open(filename, 'r') as filecontent:
            data = filecontent.readlines()
        return data

    def read_config(self):
        featurewords = []
        data = self.read_data(self.CONFIG_FILE)
        for word in data:
            tag = word.split(self.SPLITTER)
            featurewords.append(tag[1].strip())
        return featurewords

    def read_company(self):
        return self.read_data(self.COMPANY_FILE)

class PullData:

    GRAPH_URL = 'https://graph.facebook.com/'
    URL_PARAM = "?key=value&access_token="
    POST_DATA_DIR = 'data/postdata/'
    COMMENT_DATA_DIR = 'data/commentdata/comments_'
    JOINER = '|'
    TXT_EXT = '.txt'

    #return post url
    def create_url(self, graph_url, APP_ID, APP_SECRET):
        post_args = "/posts/" + self.URL_PARAM + APP_ID + self.JOINER + APP_SECRET
        post_url = graph_url + post_args
        return post_url

    #convert url page to json
    def render_url_to_json(self, graph_url):
        try:
            json_data = requests.get(graph_url).json()
            return json_data
        except Exception as error:
            return error

    #obtaining data from post url
    def scrape_posts_by_date(self, graph_url, date, post_data, APP_ID, APP_SECRET):
        page_posts = self.render_url_to_json(graph_url)

        if(page_posts is not False):
            next_page = page_posts["paging"]["next"]
            page_posts = page_posts["data"]
            collecting = True
            for post in page_posts:
                try:
                    current_post = [post["id"], post["message"], post["created_time"]]
                except Exception:
                    current_post = [ "error", "error", "error", "error"]

                if current_post[2] != "error":
                    if date <= current_post[2]:
                        post_data.append(current_post)
                    elif date > current_post[2]:
                        print("Done collecting")
                        collecting = False
                        break
            if collecting == True:
                self.scrape_posts_by_date(next_page, date, post_data, APP_ID, APP_SECRET)
            return post_data


    #create Graph API Call
    def create_comments_url(self, graph_url, post_id, APP_ID, APP_SECRET):
        comments_args = post_id + "/comments/" + self.URL_PARAM + APP_ID + self.JOINER + APP_SECRET
        comments_url = graph_url + comments_args
        return comments_url

    #obtaining comment for each post
    def get_comments_data(self, comments_url, comment_data, post_id):
        print(comments_url)
        comments = self.render_url_to_json(comments_url)["data"]
        print(comments)
        if len(comments)>0:

            for comment in comments:
                try:
                    current_comments = [comment["id"], comment["message"],comment["created_time"], post_id]
                    comment_data.append(current_comments)
                except Exception:
                    current_comments = ["error", "error", "error", "error", "error"]

            try:
                next_page = comments["paging"]["next"]
            except Exception:
                next_page = None

            if next_page is not None:
                self.get_comments_data(next_page, comment_data, post_id)
            else:
                return comment_data

    def write_file(self, data_file, data):
        with open(data_file, 'a') as file:
            file.writelines(data)
            file.close()

    def main(self):
        credentials = Config()
        APP_SECRET = credentials.secret
        APP_ID = credentials.id
        input_company_name = input("Enter Company Name").replace(" ", "").lower().split()
        list_companies = input_company_name

        last_crawl = datetime.datetime.now() - datetime.timedelta(days=18)
        last_crawl = last_crawl.isoformat()

        for company in list_companies:
            post_data_file = self.POST_DATA_DIR+company+self.TXT_EXT
            comments_data_file = self.COMMENT_DATA_DIR+company+self.TXT_EXT
            current_page_post = self.GRAPH_URL + company
            post_url = self.create_url(current_page_post, APP_ID, APP_SECRET)
            post_data = []
            post_data = self.scrape_posts_by_date(post_url, last_crawl, post_data, APP_ID, APP_SECRET)
            self.write_file(post_data_file, json.dumps(post_data))
            comment_data = []
            for post in post_data:
                comment_url = self.create_comments_url(self.GRAPH_URL, post[0], APP_ID, APP_SECRET)
                comments = self.get_comments_data(comment_url, comment_data, post[0])
                print(comments)
                self.write_file(comments_data_file, json.dumps(comments))
