# -*- coding:utf8 -*-
import execjs
import random
import requests
import json
import time

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
]
headers = {
           'User-Agent': random.choice(USER_AGENTS),
           'Accept - Encoding': 'gzip, deflate',
           'Accept - Language': 'zh - CN, zh;q = 0.9',
           'Connection': 'keep-alive'
           }
def login_data():
    data ={
        'login_id': '13026358696',
        'password': '02a05c6e278d3e19afaca4f3f7cf47d9',
        'login_type': 1,
        'auto_login': 0
    }

    keyEncry =r'''
    function  keyEncry(e) {
            var t = function(e, t) {
                return e << t | e >>> 32 - t
            };
            var n = function(e, t) {
                var n, r, i, s, o;
                i = e & 2147483648;
                s = t & 2147483648;
                n = e & 1073741824;
                r = t & 1073741824;
                o = (e & 1073741823) + (t & 1073741823);
                if (n & r)
                    return o ^ 2147483648 ^ i ^ s;
                if (n | r) {
                    if (o & 1073741824)
                        return o ^ 3221225472 ^ i ^ s;
                    else
                        return o ^ 1073741824 ^ i ^ s
                } else {
                    return o ^ i ^ s
                }
            };
            var r = function(e, t, n) {
                return e & t | ~e & n
            };
            var i = function(e, t, n) {
                return e & n | t & ~n
            };
            var s = function(e, t, n) {
                return e ^ t ^ n
            };
            var o = function(e, t, n) {
                return t ^ (e | ~n)
            };
            var u = function(e, i, s, o, u, a, f) {
                e = n(e, n(n(r(i, s, o), u), f));
                return n(t(e, a), i)
            };
            var a = function(e, r, s, o, u, a, f) {
                e = n(e, n(n(i(r, s, o), u), f));
                return n(t(e, a), r)
            };
            var f = function(e, r, i, o, u, a, f) {
                e = n(e, n(n(s(r, i, o), u), f));
                return n(t(e, a), r)
            };
            var l = function(e, r, i, s, u, a, f) {
                e = n(e, n(n(o(r, i, s), u), f));
                return n(t(e, a), r)
            };
            var c = function(e) {
                var t;
                var n = e.length;
                var r = n + 8;
                var i = (r - r % 64) / 64;
                var s = (i + 1) * 16;
                var o = Array(s - 1);
                var u = 0;
                var a = 0;
                while (a < n) {
                    t = (a - a % 4) / 4;
                    u = a % 4 * 8;
                    o[t] = o[t] | e.charCodeAt(a) << u;
                    a++
                }
                t = (a - a % 4) / 4;
                u = a % 4 * 8;
                o[t] = o[t] | 128 << u;
                o[s - 2] = n << 3;
                o[s - 1] = n >>> 29;
                return o
            };
            var h = function(e) {
                var t = "", n = "", r, i;
                for (i = 0; i <= 3; i++) {
                    r = e >>> i * 8 & 255;
                    n = "0" + r.toString(16);
                    t = t + n.substr(n.length - 2, 2)
                }
                return t
            };
            var p = function(e) {
                e = e.replace(/\x0d\x0a/g, "\n");
                var t = "";
                for (var n = 0; n < e.length; n++) {
                    var r = e.charCodeAt(n);
                    if (r < 128) {
                        t += String.fromCharCode(r)
                    } else if (r > 127 && r < 2048) {
                        t += String.fromCharCode(r >> 6 | 192);
                        t += String.fromCharCode(r & 63 | 128)
                    } else {
                        t += String.fromCharCode(r >> 12 | 224);
                        t += String.fromCharCode(r >> 6 & 63 | 128);
                        t += String.fromCharCode(r & 63 | 128)
                    }
                }
                return t
            };
            var d = Array();
            var v, m, g, y, b, w, E, S, x;
            var T = 7
              , N = 12
              , C = 17
              , k = 22;
            var L = 5
              , A = 9
              , O = 14
              , M = 20;
            var _ = 4
              , D = 11
              , P = 16
              , H = 23;
            var B = 6
              , j = 10
              , F = 15
              , I = 21;
            e = p(e);
            d = c(e);
            w = 1732584193;
            E = 4023233417;
            S = 2562383102;
            x = 271733878;
            for (v = 0; v < d.length; v += 16) {
                m = w;
                g = E;
                y = S;
                b = x;
                w = u(w, E, S, x, d[v + 0], T, 3614090360);
                x = u(x, w, E, S, d[v + 1], N, 3905402710);
                S = u(S, x, w, E, d[v + 2], C, 606105819);
                E = u(E, S, x, w, d[v + 3], k, 3250441966);
                w = u(w, E, S, x, d[v + 4], T, 4118548399);
                x = u(x, w, E, S, d[v + 5], N, 1200080426);
                S = u(S, x, w, E, d[v + 6], C, 2821735955);
                E = u(E, S, x, w, d[v + 7], k, 4249261313);
                w = u(w, E, S, x, d[v + 8], T, 1770035416);
                x = u(x, w, E, S, d[v + 9], N, 2336552879);
                S = u(S, x, w, E, d[v + 10], C, 4294925233);
                E = u(E, S, x, w, d[v + 11], k, 2304563134);
                w = u(w, E, S, x, d[v + 12], T, 1804603682);
                x = u(x, w, E, S, d[v + 13], N, 4254626195);
                S = u(S, x, w, E, d[v + 14], C, 2792965006);
                E = u(E, S, x, w, d[v + 15], k, 1236535329);
                w = a(w, E, S, x, d[v + 1], L, 4129170786);
                x = a(x, w, E, S, d[v + 6], A, 3225465664);
                S = a(S, x, w, E, d[v + 11], O, 643717713);
                E = a(E, S, x, w, d[v + 0], M, 3921069994);
                w = a(w, E, S, x, d[v + 5], L, 3593408605);
                x = a(x, w, E, S, d[v + 10], A, 38016083);
                S = a(S, x, w, E, d[v + 15], O, 3634488961);
                E = a(E, S, x, w, d[v + 4], M, 3889429448);
                w = a(w, E, S, x, d[v + 9], L, 568446438);
                x = a(x, w, E, S, d[v + 14], A, 3275163606);
                S = a(S, x, w, E, d[v + 3], O, 4107603335);
                E = a(E, S, x, w, d[v + 8], M, 1163531501);
                w = a(w, E, S, x, d[v + 13], L, 2850285829);
                x = a(x, w, E, S, d[v + 2], A, 4243563512);
                S = a(S, x, w, E, d[v + 7], O, 1735328473);
                E = a(E, S, x, w, d[v + 12], M, 2368359562);
                w = f(w, E, S, x, d[v + 5], _, 4294588738);
                x = f(x, w, E, S, d[v + 8], D, 2272392833);
                S = f(S, x, w, E, d[v + 11], P, 1839030562);
                E = f(E, S, x, w, d[v + 14], H, 4259657740);
                w = f(w, E, S, x, d[v + 1], _, 2763975236);
                x = f(x, w, E, S, d[v + 4], D, 1272893353);
                S = f(S, x, w, E, d[v + 7], P, 4139469664);
                E = f(E, S, x, w, d[v + 10], H, 3200236656);
                w = f(w, E, S, x, d[v + 13], _, 681279174);
                x = f(x, w, E, S, d[v + 0], D, 3936430074);
                S = f(S, x, w, E, d[v + 3], P, 3572445317);
                E = f(E, S, x, w, d[v + 6], H, 76029189);
                w = f(w, E, S, x, d[v + 9], _, 3654602809);
                x = f(x, w, E, S, d[v + 12], D, 3873151461);
                S = f(S, x, w, E, d[v + 15], P, 530742520);
                E = f(E, S, x, w, d[v + 2], H, 3299628645);
                w = l(w, E, S, x, d[v + 0], B, 4096336452);
                x = l(x, w, E, S, d[v + 7], j, 1126891415);
                S = l(S, x, w, E, d[v + 14], F, 2878612391);
                E = l(E, S, x, w, d[v + 5], I, 4237533241);
                w = l(w, E, S, x, d[v + 12], B, 1700485571);
                x = l(x, w, E, S, d[v + 3], j, 2399980690);
                S = l(S, x, w, E, d[v + 10], F, 4293915773);
                E = l(E, S, x, w, d[v + 1], I, 2240044497);
                w = l(w, E, S, x, d[v + 8], B, 1873313359);
                x = l(x, w, E, S, d[v + 15], j, 4264355552);
                S = l(S, x, w, E, d[v + 6], F, 2734768916);
                E = l(E, S, x, w, d[v + 13], I, 1309151649);
                w = l(w, E, S, x, d[v + 4], B, 4149444226);
                x = l(x, w, E, S, d[v + 11], j, 3174756917);
                S = l(S, x, w, E, d[v + 2], F, 718787259);
                E = l(E, S, x, w, d[v + 9], I, 3951481745);
                w = n(w, m);
                E = n(E, g);
                S = n(S, y);
                x = n(x, b)
            }
            var q = h(w) + h(E) + h(S) + h(x);
            return q.toLowerCase()
        }    
    '''

    js = execjs.compile(keyEncry)
    password = js.call('keyEncry', "1qaz2wsx")
    data['password'] = password

    # data='login_id=13026358696&password={}&login_type=1&auto_login=0'.format(password)
    return data

def login():
    session = requests.session()

    try:
        # url = "http://music.taihe.com/"
        url = "http://passport.taihe.com/v2/web/popLogin.html?tpl=baidu_music&target=pop&u=http%3A%2F%2Fmusic.taihe.com%2F&staticPage=%2F%2Fmusic.taihe.com%2Fstatic%2Fhtml%2Ftpassjump.html&callback=tpass15866147400291"
        headers['Referer'] = 'http://music.taihe.com/'
        response = session.get(url, headers=headers)

        if response and response.status_code==200:
            print(response.headers)
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            print(cookies)
            with open('cookie_new.txt', 'w') as f:
                f.write(json.dumps(cookies))
            # print(response.text)
            pass
        else:
            print(response)
            return False

        # cookies = {}
        # with open('cookie.txt', 'r') as f:
        #     for line in f.read().split(';'):
        #         print(line)
        #         name,value = line.strip().split('=',1)
        #         cookies[name] = value

        # url = 'http://passport.taihe.com/v2/api/login'
        # headers['Referer'] = 'http://passport.taihe.com/v2/web/popLogin.html?tpl=baidu_music&target=pop&u=http%3A%2F%2Fmusic.taihe.com%2F&staticPage=%2F%2Fmusic.taihe.com%2Fstatic%2Fhtml%2Ftpassjump.html&callback=tpass15866106110821'
        # # headers['Referer'] = url
        # data = login_data()
        # print(data)
        # response = session.post(url, headers=headers, data=data)

        print(response.text)

    except Exception as e:
        print(e)
        pass



if __name__ == '__main__':

    # login()
    print(time.time())