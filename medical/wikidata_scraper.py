# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """#A network of Drug-disease interactions on infectious diseases (Source: Disease Ontology, NDF-RT and ChEMBL)
SELECT DISTINCT ?item ?itemLabel ?drug ?drugLabel ?disease ?diseaseLabel ?link
WHERE
{
  VALUES ?toggle { true false }
  ?disease wdt:P699 ?doid;
           wdt:P279+ wd:Q18123741;
           wdt:P2176 ?drug.
  ?drug rdfs:label ?drugLabel.
    FILTER(LANG(?drugLabel) = "en").
  ?disease rdfs:label ?diseaseLabel.
    FILTER(LANG(?diseaseLabel) = "en").
  BIND(IF(?toggle,?disease,?drug) AS ?item).
  BIND(IF(?toggle,?diseaseLabel,?drugLabel) AS ?itemLabel).
  BIND(IF(?toggle,"",?disease) AS ?link).
}"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result)

