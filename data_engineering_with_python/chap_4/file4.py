from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()

# doc={'query':{'match_all':{}}}

# res=es.search(index='users',body=doc,size=10)

# for item in res.items():
#     print(item, sep='\t')

# for item in res['hits'].items():
#     print(item,sep='\t')
# print(res['hits']['hits'],sep='\n')

# for doc in res['hits']['hits']: 
#     print(doc['_source'])


res=es.search(index='users',
                doc_type='doc',
                scroll='2000m',
                size=500,
                body={'query':{'match_all':{}}}
              )

sid=res['_scroll_id']
size=res['hits']['total']['value']
while size>0:
    res=es.scroll(scroll_id=sid,scroll='2000m')
    sid=res['_scroll_id']
    size=len(res['hits']['hits'])
    
    for doc in res['hits']['hits']:
        print(doc['_source'])