import json, pymysql,requests, datetime

class PullData:

    #return post url
    def create_url(self, graph_url, APP_ID, APP_SECRET):
        post_args = "/posts/?key=value&access_token=" + APP_ID + "|" + APP_SECRET
        post_url = graph_url + post_args
        return post_url

    #convert url page to json
    def render_url_to_json(self,graph_url):
        json_data = requests.get(graph_url).json()
        return json_data

    #obtaining data from post url
    def scrape_posts_by_date(self,graph_url, date, post_data, APP_ID, APP_SECRET):
        page_posts = self.render_url_to_json(graph_url)
        next_page = page_posts["paging"]["next"]
        page_posts = page_posts["data"]
        collecting = True

        for post in page_posts:
            try:
                current_post = [post["id"], post["message"],
                                 post["created_time"]]
            except Exception:
                current_post = [ "error", "error", "error", "error"]

            if current_post[2] != "error":
                print(date)
                print(current_post[2])
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
        comments_args = post_id + "/comments/?key=value&access_token=" + APP_ID + "|" + APP_SECRET
        comments_url = graph_url + comments_args
        return comments_url

    #obtaining comment for each post
    def get_comments_data(self,comments_url, comment_data, post_id):
        comments = self.render_url_to_json(comments_url)["data"]

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

    def main(self):
        APP_SECRET = ""
        APP_ID = ""

        list_companies = ["walmart"]
        graph_url = "https://graph.facebook.com/"

        last_crawl = datetime.datetime.now() - datetime.timedelta(days=3)
        last_crawl = last_crawl.isoformat()

        for company in list_companies:
            current_page_post = graph_url + company
            post_url = self.create_url(current_page_post, APP_ID, APP_SECRET)
            post_data = []
            post_data = self.scrape_posts_by_date(post_url, last_crawl, post_data, APP_ID, APP_SECRET)
            #print(post_data)

            comment_data = []
            for post in post_data:
                comment_url = self.create_comments_url(graph_url, post[0], APP_ID, APP_SECRET)
                comments = self.get_comments_data(comment_url, comment_data, post[0])
                #print(comments)

if __name__ == "__main__":
    pulldata = PullData()
    pulldata.main()6
