# -*- coding: utf-8 -*-
from flask import Flask, g, make_response, request, Response
from datetime import datetime, date

app = Flask(__name__)
app.debug = True
# app.config["SERVER_NAME"] = 'local.com:5000'


@app.route("/wc")
#localhost:5000/wc?key=token&val=abc
def wc() :
    key = request.args.get("key")
    val = request.args.get("val")
    res = Response("Set Cookie")
    res.set_cookie(key, val)
    return make_response(res)

@app.route("/rc")
#localhost:5000/rc?key=token
def rg () :
    key = request.args.get("key")
    val = request.cookies.get(key)
    return "Cookie:[{}]:[{}]".format(key, val)

@app.route("/reqenv")
def reqenv() :
    ss = "<table border='1'>"
    for x in request.environ :
        ss += "<tr><td>{}</td><td>{}</td></tr>".format(x, request.environ[x])
    ss += "</table>"

    return make_response(ss)
    # return [x for x in request.environ ]
    # return ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
    #     'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
    #     'PATH_INFO: %(PATH_INFO) s <br>'
    #     'QUERY_STRING: %(QUERY_STRING) s <br>'
    #     'SERVER_NAME: %(SERVER_NAME) s <br>'
    #     'SERVER_PORT: %(SERVER_PORT) s <br>'
    #     'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
    #     'wsgi.version: %(wsgi.version) s <br>'
    #     'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
    #     'wsgi.input: %(wsgi.input) s <br>'
    #     'wsgi.errors: %(wsgi.errors) s <br>'
    #     'wsgi.multithread: %(wsgi.multithread) s <br>'
    #     'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
    #     'wsgi.run_once: %(wsgi.run_once) s') % request.environ



# request 처리 용 함수
def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans


@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)

# @app.route("/sub")
# # local.com:5000/sub
# def main_domain() :
#     return "Main Domain"

# @app.route("/sub",subdomain="g")
# # g.local.com:5000/sub
# # subdomain Testing <= /etc/hosts edit....
# def sub_domain() :
#     return "Sub Domain"

@app.route("/req1")
# local.com:5000/req1?q=123&q=abc
def req1() :
    q = request.args.get("q") #q='122'
    q = request.args.getlist("q") # q=[u'122', u'abc', u'\ud55c\uae00']
    return "q=%s" % str(q)


# WSGI(WebServer Gateway Interface)
@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [ ('Content-Type', 'text/plain'), 
                    ('Content-Length', str(len(body))) ]
        start_response('200 OK', headers)
        return [body]

    return make_response(application)



@app.route("/res1")
def res1() :
    # res = Response("custom Response", 200, {"test":"tttt"})
    res = Response("Test")
    res.headers.add('Program-Name', 'Test Response')
    res.set_data("This is Test Program.")
    res.set_cookie("UserToken", "A12Bc9")
    return make_response(res)

# @app.before_request
# def before_request() :
#     print ("before_request~!")
#     g.str = "한글"


# @app.route("/gg")
# def helloworld2():
#     return "Hello World!" + getattr(g, 'str', 'default val')


@app.route("/")
def helloworld() :
    return "Hello Flask World"

if __name__ == '__main__' :
    app.run()
