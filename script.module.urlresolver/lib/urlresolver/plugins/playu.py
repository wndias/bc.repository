"""
    urlresolver XBMC Addon
    Copyright (C) 2016 Gujal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import re
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError

class PlayUResolver(UrlResolver):
    name = 'playu'
    domains = ['playu.net']
    pattern = '(?://|\.)(playu\.net)/(?:embed-)?([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        link = self.net.http_GET(web_url).content
        if 'was deleted' in link :
            raise ResolverError('File Removed')
            
        r = re.search('file\s*:\s*"([^"]+)', link)
        if r:
            return r.group(1)
        
        raise ResolverError('Unable to find playu.net video')

    def get_url(self, host, media_id):
        return 'http://playu.net/embed-%s.html' % media_id

    def get_host_and_id(self, url):
        r = re.search(self.pattern, url)
        if r:
            return r.groups()
        else:
            return False

    def valid_url(self, url, host):
        return re.search(self.pattern, url) or self.name in host
