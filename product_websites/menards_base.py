from .website_base import WebsiteBase
import json


class Menards(WebsiteBase):

    name = 'Menards'

    def __init__(self, out_path, debug_mode=False):
        super(Menards, self).__init__(out_path + '/menards', debug_mode)
        self.scrape_map = {'Title': {'method': 4},
                           'Model No': {'method': 5},
                           'Price': {'method': 1, 'tag': 'span', 'element': 'id',
                                     'element_value': 'itemFinalPrice'},
                           'Description': {'method': 6},
                           'Image Links': {'method': 7},
                           'Features': {'method': 8}}

    def get_scrape_master(self):
        return self.scrape_methods

    class scrape_methods(WebsiteBase.scrape_methods):
        def __init__(self, driver, logger, name):
            super(Menards.scrape_methods, self).__init__(driver, logger, name)
            new_codes = {4: self.get_title, 5: self.get_modelno, 6: self.get_desc, 7: self.get_imgs,
                         8: self.get_features}
            self.method_map.update(new_codes)

        def get_title(self, soup):
            '''
            Custom scrape method
            '''
            return soup.find_all('div', {'id': 'itemDetailPage'})[0].find_all('div', {'class', 'h3'})[0].text

        def get_modelno(self, soup):
            '''
            Custom scrape method
            '''
            return self.simple_scrape(soup, 'div', 'class', 'modelSKU h4').split(':')[1].strip()

        def get_desc(self, soup):
            '''
            Custom scrape method
            '''
            return soup.find_all('div', {'id': 'descriptDocs'})[0].find_all('p')[0].text

        def get_imgs(self, soup):
            '''
            Custom scrape method
            '''
            ret = []
            for img_ele in \
            soup.find_all('div', {'class': 'alt-slider-image d-flex flex-column align-items-center py-3'})[0] \
                    .find_all('img'):
                ret.append(img_ele['src'])
            return ','.join(ret)

        def get_features(self, soup):
            '''
            Custom scrape method
            '''
            ret = []
            for feature_ele in soup.find_all('div', {'id': 'description'})[0].find_all('li'):
                ret.append(feature_ele.text)
            return ','.join(ret)
