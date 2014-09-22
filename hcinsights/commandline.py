# -*- coding: utf-8 -*-

import json
import optparse
import os.path

from . import insights
from importers.db import DBImporter


def main():
    usage = '%prog configfile'
    op = optparse.OptionParser(usage=usage)

    options, args = op.parse_args()

    if not args:
        op.error('Please provide a run config file')

    config = json.load(open(os.path.expanduser(args[0])))

    sfcreds = config['salesforce']
    password = os.environ.get('HCINSIGHTS_SFDC_PASSWORD')
    if not password:
        op.error('Please provide your password via environment varibable: HCINSIGHTS_SFDC_PASSWORD')

    auth_creds = insights.login(sfcreds['username'], password,
                                sfcreds['oauth_clientid'], sfcreds['oauth_secret'],
                                sfcreds['oauth_redirect'])

    connection = insights.SFSoapConnection(sfcreds['username'], password,
            sfcreds['edgemart_alias'], sfcreds['edgemart_container'])
    for table in config['objects']:
        importer = DBImporter(config['db'], table['table'])
        uploader = insights.InsightsUploader(importer, connection)
        uploader.upload()


if __name__ == '__main__':
    main