# -*- coding: utf-8 -*-

# Scrapy settings for MM project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'MM'

SPIDER_MODULES = ['MM.spiders']
NEWSPIDER_MODULE = 'MM.spiders'

ITEM_PIPELINES = {
	# 'MM.pipelines.MmPipeline':300
	'MM.pipelines.MmPipelineJosn':300
	
}

RANDOMIZE_DOWNLOAD_DELAY  = {
	
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'MM (+http://www.yourdomain.com)'
