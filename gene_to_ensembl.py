import requests as request

BASE = 'http://uniprot.org'
TOOL_ENDPOINT = '/uploadlists/'


def map_retrieve(ids2map, source_fmt='ACC+ID', target_fmt='ACC', output_fmt='list'):
    """
    Converts identifiers into other identifiers based on set parameters. Uses Uniprot as data source.
    :param ids2map: Identifiers for mapping.
    :param source_fmt: Format of source.
    :param target_fmt: Format of target.
    :param output_fmt: Output format.
    :return:
    """
    if hasattr(ids2map, 'pop'):
        payload = {'from': source_fmt,
                   'to': target_fmt,
                   'format': output_fmt,
                   'query': ids2map,
                   }
        response = request.get(BASE + TOOL_ENDPOINT, params=payload)
        if response.ok:
            return response.text
        else:
            response.raise_for_status()


def convert_ID(id, type):
    """
    Converts individual identifiers to other identifiers using the map_retrieve function.
    :param id: Source identifier type.
    :param type: Target identifier type.
    :return: Returns identifier.
    """
    if type == "ensembl":
        ensembl = map_retrieve(id.strip().split(), target_fmt='ENSEMBL_ID').split("\n")[0]
    elif type == "gene":
        ensembl = map_retrieve(id.strip().split(), target_fmt='GENENAME').split("\n")[0]
    return ensembl
