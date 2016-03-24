# -*- coding: utf-8 -*-


import tornado.ioloop
import tornado.web
import pdb

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("session")

class MainHandler(BaseHandler):
    @tornado.web.authenticated # 如果没有登陆，就自动跳转到登陆页面
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name+'</br>'
                    '<span><a href="http://127.0.0.1:5000">127.0.0.1:5000</a></span>')

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    def post(self):
        # 这里补充一个，获取用户输入
        # self.get_argument("name")
        self.set_cookie('test', self.get_argument('name'),domain='cinghoo.com')
        #secure_cookie不能跨二级域名传递
        # self.set_secure_cookie("session", self.get_argument("name"),path='.cinghoo.com')
        # pdb.set_trace()
        self.redirect("/")

settings = {
    "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=", # 安全cookie所需的
    "login_url": "/login", # 默认的登陆页面，必须有
    'debug':True
}
# handlers.append(site.handlers)
handlers = [
            # "^[a-zA-Z_\-0-9]*\.cinghoo.com$",
                # [
                    (r"/", MainHandler),
                    (r"/login", LoginHandler),
                # ]
            ]

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
