#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'cxw620'
# time: 2022-07-01 20:00
# 使用前安装 pip install huaweicloudsdkcore
# 使用前安装 pip install huaweicloudsdkcdn
from huaweicloudsdkcore.auth.credentials import GlobalCredentials
from huaweicloudsdkcdn.v1.region.cdn_region import CdnRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcdn.v1 import *
from datetime import datetime

AK = "AK"
SK = "SK"
DOMAIN_CDN = [
    {
        # domain
        "domain": "example.com",
        # where stored pem cert
        "fullchain": "/www/server/panel/vhost/ssl/example.com/fullchain.pem",
        # where stored pem key
        "privkey": "/www/server/panel/vhost/ssl/example.com/privkey.pem"
    },
]
def read_cert(_domainInfo):
        print("Read Certs!")
        with open(_domainInfo["fullchain"], 'r') as _cert:
            _cert_text = _cert.read()
        with open(_domainInfo["privkey"], 'r') as _key:
            _key_text = _key.read()
        return [_cert_text, _key_text]


if __name__ == "__main__":
    # 实际上是可以同时多域名的, 懒得改了
    for _domain in DOMAIN_CDN:
        _cert_info = read_cert(_domain)

        credentials = GlobalCredentials(AK, SK) \

        client = CdnClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(CdnRegion.value_of("cn-north-1")) \
            .build()
        try:
            request = UpdateDomainMultiCertificatesRequest()
            forceRedirectConfigForceRedirect = ForceRedirect(
                switch=1,
                redirect_type="https"
            )
            httpsUpdateDomainMultiCertificatesRequestBodyContent = UpdateDomainMultiCertificatesRequestBodyContent(
                domain_name=_domain['domain'],
                https_switch=1,
                access_origin_way=3,
                force_redirect_https=1,
                force_redirect_config=forceRedirectConfigForceRedirect,
                http2=1,
                cert_name="cert " + _domain['domain'] + " Add Time " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                certificate=_cert_info[0],
                private_key=_cert_info[1]
            )
            request.body = UpdateDomainMultiCertificatesRequestBody(
                https=httpsUpdateDomainMultiCertificatesRequestBodyContent
            )
            response = client.update_domain_multi_certificates(request)
            print(response)
        except exceptions.ClientRequestException as e:
            print(e.status_code)
            print(e.request_id)
            print(e.error_code)
            print(e.error_msg)
