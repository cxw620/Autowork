#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb, cxw620'
# time: 2022-09-11 22:00
# 使用前: pip install tencentcloud-sdk-python

import json
from datetime import datetime
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.ssl.v20191205 import ssl_client
from tencentcloud.ssl.v20191205 import models as models_ssl
from tencentcloud.ecdn.v20191012 import ecdn_client
from tencentcloud.ecdn.v20191012 import models as models_ecdn
from tencentcloud.cdn.v20180606 import cdn_client
from tencentcloud.cdn.v20180606 import models as models_cdn

# ---------------Static--------------------------
SECRETID = "SECRET ID"
SECRETKEY = "SECRET KEY"
DOMAIN_PACK = {
    "example.com": [
        "example1.example.com",
    ],
}
LOC = "/root/.acme.sh/"
# 控制功能开关
# 是否开启HTTP2
ENABLE_HTTP2 = True
# 是否开启HSTS
ENABLE_HSTS = True
# 为HSTS设定最长过期时间（以秒为单位）
HSTS_TIMEOUT_AGE = 3153600
# HSTS包含子域名（仅对泛域名有效）
HSTS_INCLUDE_SUBDOMAIN = True
# 是否开启OCSP
ENABLE_OCSP = True
# 是否开启HTTP->HTTPS强制跳转
FORCE_REDIRECT = True
# TLS Version设置, 默认除了TLS1.0("TLSv1")全开
TLS_VERSION = ["TLSv1.1", "TLSv1.2", "TLSv1.3"]
# ---------------Static--------------------------


def read_cert(_domain):
    """读取证书内容"""
    with open(LOC + _domain + "/" + "fullchain" + ".cer", "r") as _cer:
        _cer_text = _cer.read()
    with open(LOC + _domain + "/" + _domain + ".key", "r") as _key:
        _key_text = _key.read()
    timestr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _cert_full = {
        "CertificatePublicKey": _cer_text,
        "CertificatePrivateKey": _key_text,
        "Alias": "Auto Upload at {}".format(timestr),
    }
    return _cert_full


def upload_cert(_domain):
    try:
        cred = credential.Credential(SECRETID, SECRETKEY)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ssl_client.SslClient(cred, "", clientProfile)

        req = models_ssl.UploadCertificateRequest()
        params = read_cert(_domain)
        req.from_json_string(json.dumps(params))

        resp = client.UploadCertificate(req)
        print(resp.to_json_string())
        return str(resp.CertificateId)

    except TencentCloudSDKException as err:
        print(err)
        return ""


def update_cdn_ssl(_ssl_domain: str, _domain_list: list):
    """该函数实现为CDN更新ssl证书的功能"""
    _id = upload_cert(_ssl_domain)

    def get_cdn_detail_info(_domain):
        try:
            cred = credential.Credential(SECRETID, SECRETKEY)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cdn.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = cdn_client.CdnClient(cred, "", clientProfile)

            req = models_cdn.DescribeDomainsConfigRequest()
            params = {"Filters": [{"Name": "domain", "Value": [_domain[0]]}]}
            req.from_json_string(json.dumps(params))

            resp = client.DescribeDomainsConfig(req)
            return resp.Domains
        except TencentCloudSDKException as err:
            print(err)
            return []

    for _domain in _domain_list:
        cdns = get_cdn_detail_info(_domain)
        https = None
        for _cdn in cdns:
            if _cdn.Domain == _domain:
                https = _cdn.Https
                break
        print(https)
        # generate_https(https)
        try:
            cred = credential.Credential(SECRETID, SECRETKEY)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "cdn.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = cdn_client.CdnClient(cred, "", clientProfile)
            req = models_cdn.UpdateDomainConfigRequest()
            # 必选参数
            # Domain: String, 域名
            # 部分可选参数
            # Https: Https, Https 加速配置
            # 该类型详见 https://cloud.tencent.com/document/api/228/30987#Https
            timestr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            params = {
                "Domain": _domain,
                "ForceRedirect": {
                    "Switch": "off",
                    "RedirectType": "https",
                    "RedirectStatusCode": 301,
                    "CarryHeaders": "on",
                },
                "Https": {
                    "Switch": "on",
                    "CertInfo": {
                        "CertId": _id,
                        "Message": "Auto Update at {}".format(timestr),
                    },
                },
            }
            if ENABLE_HTTP2:
                params["Https"]["Http2"] = "on"

            if ENABLE_HSTS:
                params["Https"]["Hsts"] = {
                    "Switch": "off",
                    "MaxAge": 0,
                    "IncludeSubDomains": "off",
                }
                params["Https"]["Hsts"]["Switch"] = "on"
                params["Https"]["TlsVersion"] = TLS_VERSION
                params["Https"]["Hsts"]["MaxAge"] = HSTS_TIMEOUT_AGE
                if HSTS_INCLUDE_SUBDOMAIN:
                    params["Https"]["Hsts"]["IncludeSubDomains"] = "on"

            if ENABLE_OCSP:
                params["Https"]["OcspStapling"] = "on"
            if FORCE_REDIRECT:
                params["ForceRedirect"]["Switch"] = "on"
            req.from_json_string(json.dumps(params))

            resp = client.UpdateDomainConfig(req)
            print(resp.to_json_string())
            print("成功更新域名为{0}的CDN的ssl证书为{1}".format(_domain, _id))

        except TencentCloudSDKException as err:
            print(err)
            exit("为CDN设置SSL证书{}出错".format(_id))


if __name__ == "__main__":
    for _ssl_domain in DOMAIN_PACK:
        _domain_list = DOMAIN_PACK[_ssl_domain]
        update_cdn_ssl(_ssl_domain, _domain_list)
