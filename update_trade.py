from elasticsearch import Elasticsearch
import requests
from time import time
from datetime import datetime
from elasticsearch_dsl import Search
es = Elasticsearch()



def update_trade(pair,option):
    r = requests.get('https://api1.binance.com/api/v3/ticker/price?symbol='+pair)
    data1=r.json()
    price=data1['price']
    # rdate = datetime.datetime.now()
    if option=="put":
        data={
                "script": {   "source":"ctx._source.final_price="f"{float(price)}"";if(ctx._source.final_price<ctx._source.price){ctx._source.result='win';ctx._source.update_trade=1}else{ctx._source.result='loss';ctx._source.update_trade=1}",
                "lang": "painless"
                },
                "query": {
                    "bool": {
                    "must": [
                        {
                        "match": {
                            "option": option
                        }
                        },
                        {
                        "match": {
                            "pair": pair
                        }
                        },
                        {
                        "match": {
                            "update_trade": 0
                        }
                        }
                    ]
                    }
                }
            }
        try:
            upadte_t=es.update_by_query(body=data, doc_type='trades', index='trades')
        except:
            upadte_t="es error"
    elif option=="call":
        data={
                "script": {   "source":"ctx._source.final_price="f"{float(price)}"";if(ctx._source.final_price>ctx._source.price){ctx._source.result='win';ctx._source.update_trade=1}else{ctx._source.result='loss';ctx._source.update_trade=1}",
                "lang": "painless"
                },
                "query": {
                    "bool": {
                    "must": [
                        {
                        "match": {
                            "option": option
                        }
                        },
                        {
                        "match": {
                            "pair": pair
                        }
                        },
                        {
                        "match": {
                            "update_trade": 0
                        }
                        }
                    ]
                    }
                }
            }
        try:
            upadte_t=es.update_by_query(query=data, doc_type='trades', index='trades')
        except:
            upadte_t="es error"
    return upadte_t

#main balance check
def main_balance(id):
    body={
            "query": {
                "match": {
                "zid":id 
                }
            }
            }
    check_bal=es.search(index='user_accounts',doc_type='accounts',body=body)
    hits=check_bal['hits']
    max_score = hits['max_score']
    if max_score is None:
        u_accounts={
            "zid":id,
            "main_balance":"0",
            "tournament_balance":"0"
        }
        es.index(index="user_accounts", doc_type="accounts",body=u_accounts)
        return {"main_balnce":"0","status":"account created sucessfully"}
    else:
        source=check_bal['hits']['hits'][0]['_source']
        main_balance=source['main_balance']
        id=check_bal['hits']['hits'][0]['_id']
        return {"main_balance":float(main_balance),"id":id}
        
# update main balance for 
def update_main_balance(new_bal,id):
    update_bal={
            "doc": {
                "main_balance": new_bal
            }
        }
    res=es.update(index='user_accounts',doc_type='accounts',id=id,body=update_bal)
    if res['result']=="updated":
        return {"update_id":res['_id']}
    else:
        return {"status":"something went wrong","res":res}
def upated_trade_amt():
    data={
        "_source": ["zid","traded_amt"],
        "query": {
            "bool": {
            "must": [
                {
                "match": {
                    "option": "put"
                }
                },
                {
                "match": {
                    "pair": "BTCUSDT"
                }
                },
                {
                "match": {
                    "result": "win"
                }
                },
                {
                "match": {
                    "update_trade": 1
                }
                }
            ]
            }
        }
        }
    update_amt=es.search(index='trades',doc_type='trades',body=data)
    lst=update_amt['hits']['hits']
    a=list()
    for index,item in enumerate(lst):
        zid=lst[int(index)]["_source"]["zid"]
        amt=lst[int(index)]["_source"]["traded_amt"]
        m_bal=main_balance(zid)
        bal=m_bal["main_balance"]
        id=m_bal["id"]
        new_bal=float(amt*0.75)+bal
        res=update_main_balance(new_bal,id)
        a.append(res)
        print(index,item)
    return a
        
reasult=update_trade("BTCUSDT","put")
result=update_trade("BTCUSDT","call")
r1=upated_trade_amt()
# print(reasult,result)
print(r1)