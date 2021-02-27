# from opulence.config import engine_config
# from opulence.common.database.es import create_client, INDEXES


# # Create ES instance
# es_client = create_client(engine_config.elasticsearch)

# # Create kibana defaut index patterns
# for index in INDEXES:
#     kibana_endpoint = f"{engine_config.kibana.url}/api/saved_objects/index-pattern/{index.index_name}"
#     headers = {"kbn-xsrf": "yes", "Content-Type": "application/json"}
#     data = {
#         "attributes": {
#         "title": f"{index.index_name}*"
#         }
#     }
#     r = httpx.post(kibana_endpoint, json=data, headers=headers)
#     logger.info(f"Kibana create index pattern ({index}): {r.status_code}")

# print("done")
