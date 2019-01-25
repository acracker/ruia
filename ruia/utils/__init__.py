#!/usr/bin/env python

from .log import get_logger


def default_pop(dictionary, key, default=None):
    try:
        return dictionary.pop(key)
    except KeyError:
        return default


def make_headers(string):
    """
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9
    Cache-Control: max-age=0
    Connection: keep-alive
    Cookie: authLoginSwitch=false; authTag=13608228554; JRECORD_UID=c128882a29cbde99b0d744bcdd6873d5; JRECORD_FTIME=1534148336; _smt_uid=5b713ef0.1587aa61; gr_user_id=260c312d-c6f8-4245-8715-21eebe9473d2; MEIQIA_EXTRA_TRACK_ID=8584c244428711e780ee02fa39e25136; JRECORD_LTIME=1541585306; JRECORD_SRC=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DrV-4Cp4G9kZWeh3wpmlcK7aUrKx3BRyL3BKbAcVa4cm%26wd%3D%26eqid%3Db990c08600066227000000055c3ee952; Hm_lvt_9cfdc8c0bb3c0ab683956289eef9f34a=1547626841; MEIQIA_VISIT_ID=1FqBeZFRVix119lMZvU29xy4ZlU; compare_index=0%26%261%26%262%26%263; PHPSESSID=v0676p8stfqo5cco4qrtbe9bc6; jfzWebUser=11183f9c01015af8ca15ca99bbcd9f3a83fb8d3ea%3A4%3A%7Bi%3A0%3Bs%3A10%3A%224720875108%22%3Bi%3A1%3Bs%3A11%3A%2213608228554%22%3Bi%3A2%3Bi%3A86400%3Bi%3A3%3Ba%3A0%3A%7B%7D%7D; jfz_login_id=4720875108; accessToken=3e993ec9bd688828a0b677aec126a42c; jfz_user_type=0; JRECORD_LANDPAGE=https%3A%2F%2Fwww.jfz.com%2Fsimu%2Fcompany_p1.html; gr_cs1_b747f2ce-9af2-45a2-893b-d9e6abcc9b7b=user_id%3A4720875108; JRECORD_CTIME=1547630027; Hm_lpvt_9cfdc8c0bb3c0ab683956289eef9f34a=1547630027
    Host: www.jfz.com
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36

    :param string:
    :return:
    """
    result = {}
    for header in string.split('\n'):
        header = header.strip()
        if header:
            items = header.split(':')
            k = items[0]
            v = ":".join(items[1:])
            k = k.strip()
            v = v.strip()
            result[k] = v
    return result



if __name__ == '__main__':

    s = """
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
        Accept-Encoding: gzip, deflate, br
        Accept-Language: zh-CN,zh;q=0.9
        Cache-Control: max-age=0
        Connection: keep-alive
        Cookie: authLoginSwitch=false; authTag=13608228554; JRECORD_UID=c128882a29cbde99b0d744bcdd6873d5; JRECORD_FTIME=1534148336; _smt_uid=5b713ef0.1587aa61; gr_user_id=260c312d-c6f8-4245-8715-21eebe9473d2; MEIQIA_EXTRA_TRACK_ID=8584c244428711e780ee02fa39e25136; JRECORD_LTIME=1541585306; JRECORD_SRC=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DrV-4Cp4G9kZWeh3wpmlcK7aUrKx3BRyL3BKbAcVa4cm%26wd%3D%26eqid%3Db990c08600066227000000055c3ee952; Hm_lvt_9cfdc8c0bb3c0ab683956289eef9f34a=1547626841; MEIQIA_VISIT_ID=1FqBeZFRVix119lMZvU29xy4ZlU; compare_index=0%26%261%26%262%26%263; PHPSESSID=v0676p8stfqo5cco4qrtbe9bc6; jfzWebUser=11183f9c01015af8ca15ca99bbcd9f3a83fb8d3ea%3A4%3A%7Bi%3A0%3Bs%3A10%3A%224720875108%22%3Bi%3A1%3Bs%3A11%3A%2213608228554%22%3Bi%3A2%3Bi%3A86400%3Bi%3A3%3Ba%3A0%3A%7B%7D%7D; jfz_login_id=4720875108; accessToken=3e993ec9bd688828a0b677aec126a42c; jfz_user_type=0; JRECORD_LANDPAGE=https%3A%2F%2Fwww.jfz.com%2Fsimu%2Fcompany_p1.html; gr_cs1_b747f2ce-9af2-45a2-893b-d9e6abcc9b7b=user_id%3A4720875108; JRECORD_CTIME=1547630027; Hm_lpvt_9cfdc8c0bb3c0ab683956289eef9f34a=1547630027
        Host: www.jfz.com
        Upgrade-Insecure-Requests: 1
        User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36
    """
    print(make_headers(s))
