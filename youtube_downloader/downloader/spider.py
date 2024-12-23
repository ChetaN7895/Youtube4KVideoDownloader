# -*- coding: utf-8 -*-
from http.cookiejar import LWPCookieJar
import socket
from urllib import request, parse, error
from ..utils.tail_call import tail_call_optimized

__author__ = 'rabbi'

USER_AGENT = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0')


class Spider(object):
    __headers = [USER_AGENT,
                 ('Connection', 'keep-alive'),
                 # ('Accept-Encoding', 'gzip, deflate'),
                 ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                 ('Accept-Language', 'en-us,en;q=0.5')]

    def __init__(self):
        self.__opener = None

    # @tail_call_optimized
    def fetch_data(self, url, parameters=None, headers=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, retry=0,
                   max_retry=3):
        try:
            if not headers:
                headers = self.__headers

            if self.__opener is None:
                self.__opener = self.__create_opener(headers=headers, handler=self.__create_cookie_jar_handler())
            if not parameters:
                response = self.__opener.open(url, timeout=timeout)
                print(response.info())
            else:
                print('ok..1' + url)
                response = self.__opener.open(url, data=parse.urlencode(parameters).encode('utf-8'), timeout=timeout)

            if response:
                print(response.info())
                return response.read().decode('utf-8')
        except error.HTTPError as e:
            print(e.code)
        except error.ContentTooShortError as e:
            print(e.reason)
        except error.URLError as e:
            print(e.reason)
        except Exception as ex:
            print(ex)
            if retry < max_retry:
                return self.fetch_data(url, parameters=parameters, retry=retry + 1)
        return None

    @staticmethod
    def __create_opener(headers=None, handler=None):
        """
        Create opener for fetching data.
        headers = [] Ex. User-agent etc like, [('User-Agent', HEADERS), ....]
        handler = object Ex. Handler like cookie_jar, auth handler etc.
        return opener
        """
        try:
            opener = request.build_opener(request.HTTPRedirectHandler(),
                                          request.HTTPHandler(debuglevel=0),
                                          request.HTTPSHandler(debuglevel=0))
            if headers is not None:
                opener.addheaders.extend(headers)
            if handler is not None:
                opener.add_handler(handler)

            request.install_opener(opener)
            return opener
        except Exception as x:
            raise x

    @staticmethod
    def __create_cookie_jar_handler():
        """
        Create cookie jar handler. used when keep cookie at login.
        """
        cookie_jar = LWPCookieJar()
        return request.HTTPCookieProcessor(cookie_jar)