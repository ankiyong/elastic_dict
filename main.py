from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse,FileResponse
from elasticsearch import Elasticsearch
import uvicorn

app = FastAPI()

# es = Elasticsearch([{"host": "localhost", "port": 9200}])
es = Elasticsearch("http://localhost:9200", http_auth=('elastic','bGzOBS9el+QJ+XwoDDLM'), verify_certs=False)

@app.get("/")
def read_root():
    return FileResponse('root.html')

@app.get("/search")
async def search(q: str = Query(None)):
    if not q:
        return {"message": "Please provide a search term"}
    
    results = es.search(index="blogs", body={"query": {"match": {"content": q}}})
    analyzers = ["syno_stan","nori","ngram"]
    results = []
    for analyzer in analyzers:
        body = {
        "analyzer": analyzer,
        "text": q
        }
        results.append([es.indices.analyze(index="test_dic", body=body)])
    
    result_html = "<div style='display: inline-flex'>"
    # for result in results["hits"]["hits"]:
    #     result_html += f"<p>{result['_source']['url']}</p>"
    # for i, result in enumerate(results['analyzer']):
        # result_html += f"<p>{result['token']}</p>"
    for result in results:
        for i in result:
            result_html += "<ul class='list-group'>"
            for r in i['tokens']:
                result_html += f"<li class='list-group-item'>{r['token']}</li>"
            result_html += "</ul>"
    result_html += "</div>"
    html = f'''
    <html>
        <head>
        <!-- CSS only -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
            <title>Search Results for "{q}"</title>
        </head>
        <body>
            <h1>Search Results for "{q}"</h1>
            {result_html}
            
        </body>
        <!-- JavaScript Bundle with Popper -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
    </html>
    '''
    return HTMLResponse(content=html)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)