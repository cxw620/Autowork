#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'cxw620'
# time: 2022-9-11 21:00
# 使用前: pip install alibabacloud_dcdn20180115==1.0.19

import copy
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dcdn20180115.client import Client as dcdn20180115Client
from alibabacloud_dcdn20180115 import models as dcdn_20180115_models
from datetime import datetime

# 参数
AK = "YOUR AK"
SK = "YOUR SK"
# 这是你的证书保存地址
DOMAIN_SSL = {
    "example.com": {
        "fullchain": "/www/server/panel/vhost/ssl/example.com/fullchain.pem",
        "privkey": "/www/server/panel/vhost/ssl/example.com/privkey.pem",
    },
}
# example.com为Main_Domain, example1.example.com等为在SAN_Domains范围内的待配置SSL的的domain
DOMAIN_DCDN = {
    "example.com": [
        "example1.example.com",
        "example2.example.com",
        "example3.example.com",
    ],
}


CONFIG = open_api_models.Config(access_key_id=AK, access_key_secret=SK)


def set_cert_dcdn(_ssl_domain: str, _domain_list: list):
    def read_cert(_ssl_domain):
        print("Read Certs!")
        with open(DOMAIN_SSL[_ssl_domain]["fullchain"], "r") as _cert:
            _cert_text = _cert.read()
        with open(DOMAIN_SSL[_ssl_domain]["privkey"], "r") as _key:
            _key_text = _key.read()
        return [_cert_text, _key_text]

    _cert_info = read_cert(_ssl_domain)
    dcdn_config = copy.deepcopy(CONFIG)
    dcdn_config.endpoint = f"dcdn.aliyuncs.com"
    dcdn_client = dcdn20180115Client(dcdn_config)
    batch_set_dcdn_domain_certificate_request = (
        dcdn_20180115_models.BatchSetDcdnDomainCertificateRequest(
            domain_name=",".join(_domain_list),
            cert_name=_ssl_domain + f" Updated At {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            cert_type="upload",
            sslprotocol="on",
            sslpub=_cert_info[0],
            sslpri=_cert_info[1],
        )
    )
    dcdn_runtime = util_models.RuntimeOptions()
    try:
        # 复制代码运行请自行打印 API 的返回值
        dcdn_client.batch_set_dcdn_domain_certificate_with_options(
            batch_set_dcdn_domain_certificate_request, dcdn_runtime
        )
        return True
    except Exception as error:
        try:
            print(UtilClient.assert_as_string(error.message))
        except:
            print(error)
        finally:
            print(f"设置属于[{_ssl_domain}]的证书失败")
            return False


if __name__ == "__main__":
    # _ssl_domain_data = upload_ssl()
    for _ssl_domain in DOMAIN_DCDN:
        # _ssl_domain_cas_name = _ssl_domain_data[_ssl_domain]
        _domain_list = DOMAIN_DCDN[_ssl_domain]
        print(f"开始设置属于[{_ssl_domain}]的证书")
        _resp = set_cert_dcdn(_ssl_domain, _domain_list)
        if _resp:
            print(f"设置属于[{_ssl_domain}]的证书成功")
