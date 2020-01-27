# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import scrapy
import json
import pprint

# create spider to scrape the business web app
class TaskSpider(scrapy.Spider):
    name       = 'task'
    start_urls = ['https://firststop.sos.nd.gov/search/business']

    # create the data file with column headers
    # use jsonRequest method query data from webservice
    def parse(self, response):
        open('data.tsv','w').close()
        with open('data.tsv', 'w') as dataFile:
            dataFile.write('Title\tOwner\tRegistered_Agent\t' +
                'Commercial_Registered_Agent\n')
        return scrapy.http.JsonRequest(
            url  = 'https://firststop.sos.nd.gov/api/Records/businesssearch',
            data = {"SEARCH_VALUE":"x", 
                    "STARTS_WITH_YN":"true", 
                    "ACTIVE_ONLY_YN":"true"},
            callback = self.parse_details
        )

    # collect response from query call
    # for each business, make another request to get additional data
    def parse_details(self, response):
        data = json.loads(response.text)
        for key, value in data['rows'].items():
            title   = value['TITLE'][0]
            yield scrapy.http.Request(
                url = 'https://firststop.sos.nd.gov/' +
                    'api/FilingDetail/business/{}/false'.format(key),
                callback  = self.parse_xml,
                cb_kwargs = dict(title=title)
            )

    # extract owner and agent information and write into file
    def parse_xml(self, response, title):
        d = {'title':title}
        d['ra'], d['owner'], d['cra'] = 'NA', 'NA', 'NA'
        root = ET.fromstring(response.text)
        for drawer in root[0]:
            if drawer[0].text == 'Registered Agent':
                d['ra'] = drawer[1].text.split('\n')[0]
            if drawer[0].text == 'Commercial Registered Agent':
                d['cra'] = drawer[1].text.split('\n')[0]
            if drawer[0].text == 'Owner Name':
                d['owner'] = drawer[1].text.split('\n')[0]
        with open('data.tsv', 'a') as myFile:
            myFile.write('{}\t{}\t{}\t{}\n' \
                .format(d['title'],
                        d['owner'],
                        d['ra'],
                        d['cra']))
