from elasticsearch import Elasticsearch


class index_info:
    def __init__(self,host,username,password):
        self.host = host
        self.username = username
        self.password = password
    def get_index(self):
        host = self.host
        username = self.username
        password = self.password
        es = Elasticsearch(host, http_auth=(username,password), verify_certs=False)
        result = es.indices.get(index="*")
        index_list = list(result.keys())
        return result,index_list


# es = Elasticsearch("https://localhost:9200", http_auth=('elastic','bGzOBS9el+QJ+XwoDDLM'), verify_certs=False)
node1 = index_info("https://localhost:9200","elastic","bGzOBS9el+QJ+XwoDDLM")

print(node1.get_index())



