#import debugpy
#debugpy.listen(("0.0.0.0", 5678))
#debugpy.wait_for_client()
from flask import Flask, request, make_response
import time
import datetime
import json
import datetime
import requests
from flask_cors import CORS
import gzip, zlib
import copy

app = Flask(__name__)
CORS(app)

noBidResponse = {}
noBidResponse['uuid'] = 'BID_UUID'
noBidResponse['tag_id'] = 'TAG_ID'
noBidResponse['auction_id'] = '8700173304411798647'
noBidResponse['nobid'] = True
noBidResponse['ad_profile_id'] = 1182765

bidResponse = {}
bidResponse['uuid'] = 'BID_UUID'
bidResponse['tag_id'] = 'TAG_ID'
bidResponse['auction_id'] = '6249467170603590729'
bidResponse['nobid'] = False
bidResponse['no_ad_url'] = ''
bidResponse['timeout_ms'] = 0
bidResponse['ad_profile_id'] = 1182765
bidResponse['rtb_video_fallback'] = False
ads = {}
ads['content_source'] = 'rtb'
ads['ad_type'] = 'banner'
ads['buyer_member_id'] = 9325
ads['advertiser_id'] = 2529885
ads['creative_id'] = 96846035
ads['media_type_id'] = 1
ads['media_subtype_id'] = 1
ads['cpm'] = 0.10
ads['is_bin_price_applied'] = False
ads['publisher_currency_code'] = '$'
ads['brand_category_id'] = 0
ads['client_initiated_ad_counting'] = True
rtb = {}
banner = {}
banner['content'] = "<a href='https://adrelevantis.xyz/' target='_blank'><img src='https://www.adrelevantis.com/img/defaulthb.png' width='300' height='250' alt='' title='' border='0' /></a>"
banner['width'] = 300
banner['height'] = 250
banner728_90 = "<a href='https://adrelevantis.xyz/' target='_blank'><img src='https://www.adrelevantis.com/img/hb728_90.png' width='728' height='90' alt='' title='' border='0' /></a>"
banner970_250 = "<a href='https://adrelevantis.xyz/' target='_blank'><img src='https://www.adrelevantis.com/img/hb970_250.png' width='970' height='250' alt='' title='' border='0' /></a>"
tracker = {}
tracker['impression_urls'] = []
tracker['video_events'] = {}
trackers = [tracker]
rtb['banner'] = banner
rtb['trackers'] = trackers
ads['rtb'] = rtb
bidResponse['ads'] = [ads]

@app.route('/prebid', methods=['POST'])
def prebid():
    try:
        if request.data is not None:
            payload = json.loads(request.data.decode('utf-8'))
            ks =''
            if 'fpd' in payload:
                for k in payload['fpd']['keywords']:
                    ks = ks + '|' + k
            keywords = ks[1:] if len(ks)>1 else ''
            category=payload['fpd']['category'] if 'fpd' in payload else ''
			
            query =''
            for tag in payload['tags']:
                keys = []
                for adtype in tag['ad_types']:
                    for siz in tag['sizes']:
                        key = adtype + '-' + str(siz['width']) + 'x' + str(siz['height'])
                        if not (key in keys):
                            keys.append(key)

                query = query + '|tag' + str(tag['uuid']) + '|cpm-' + str(tag['cpm']) + '|'+  '|'.join(keys)

            query = {'tags' : query[1:], 'category': category, 'keywords': keywords, 'ref': payload['referrer_detection']['rd_ref']}
            bidder = 'https://adserver.adrelevantis.com/'
            res = requests.post(bidder + 'www/delivery/asyncspc.php', data=query).text

            tm = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
            k = (bidder[7:] if bidder.find('https') else bidder[6:]).split(':')[0] + ':' + tm
            query['response'] = res

            bids = json.loads(res)['rtb']['html']
            tags = payload['tags']
            resp_tags = [dict() for x in range(len(tags))]
            for x in range(len(tags)):
                hasBid = False
                for b in range(len(bids)):
                    if bids[b]['tag'] == tags[x]['uuid']:
                        hasBid = True
                        resp_tags[x] = copy.deepcopy(bidResponse)
                        resp_tags[x]['ads'][0]['rtb']['banner']['width'] = bids[b]['width']
                        resp_tags[x]['ads'][0]['rtb']['banner']['height'] = bids[b]['height']
                        resp_tags[x]['ads'][0]['rtb']['banner']['content'] = bids[b]['ad']
                        resp_tags[x]['uuid'] = tags[x]['uuid']
                        resp_tags[x]['tag_id'] = tags[x]['id']
                        if tags[x]['cpm'] is not None:
                            resp_tags[x]['ads'][0]['cpm'] = tags[x]['cpm']
                        break

                if not hasBid:
                    if  tags[x]['id'] == 13144370:
                        for siz in tags[x]['sizes']:
                            if siz['width'] == 300 and siz['height'] == 250:
                                hasBid = True
                                resp_tags[x] = copy.deepcopy(bidResponse)
                            elif siz['width'] == 728 and siz['height'] == 90:
                                hasBid = True
                                resp_tags[x] = copy.deepcopy(bidResponse)
                                resp_tags[x]['ads'][0]['rtb']['banner']['width'] = 728
                                resp_tags[x]['ads'][0]['rtb']['banner']['height'] = 90
                                resp_tags[x]['ads'][0]['rtb']['banner']['content'] = banner728_90
                            elif siz['width'] == 970 and siz['height'] == 250:
                                hasBid = True
                                resp_tags[x] = copy.deepcopy(bidResponse)
                                resp_tags[x]['ads'][0]['rtb']['banner']['width'] = 970
                                resp_tags[x]['ads'][0]['rtb']['banner']['height'] = 250
                                resp_tags[x]['ads'][0]['rtb']['banner']['content'] = banner970_250
                        if tags[x]['cpm'] is not None:
                            resp_tags[x]['ads'][0]['cpm'] = tags[x]['cpm']

                    if not hasBid:
                        resp_tags[x] = copy.deepcopy(noBidResponse)

                    resp_tags[x]['uuid'] = tags[x]['uuid']
                    resp_tags[x]['tag_id'] = tags[x]['id']
                    
        itms = []
        itm = {}
        itm['version'] = '3.0.0'
        itm['tags'] = resp_tags
        itms.append(itm)

        acceptEncoding = request.headers['Accept_Encoding']
        if 'gzip' in acceptEncoding:
            buffer = gzip.compress(json.dumps(itm).encode('utf-8'))
            res = make_response(buffer)
            res.headers['Content-Encoding'] = 'gzip'
        elif 'defalte' in acceptEncoding:
            res = make_response(zlib.compress(json.dumps(itm).encode('utf-8')))
            res.headers['Content-Encoding'] = 'deflate'
        res.headers['Content-Type'] = 'application/json'
        res.headers['Access-Control-Allow-Credentials'] = 'true'
        res.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        return res
    except Exception as e:
        tm = time.strftime('%Y-%m-%d %Hh%Mm%Ss', time.localtime(time.time()))
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
