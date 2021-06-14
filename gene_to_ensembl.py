import requests as request

BASE = 'http://uniprot.org'
TOOL_ENDPOINT = '/uploadlists/'


def map_retrieve(ids2map, source_fmt='ACC+ID', target_fmt='ACC', output_fmt='list'):
    """

    :param ids2map:
    :param source_fmt:
    :param target_fmt:
    :param output_fmt:
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

    :param id:
    :param type:
    :return:
    """
    if type == "ensembl":
        ensembl = map_retrieve(id.strip().split(), target_fmt='ENSEMBL_ID').split("\n")[0]
    elif type == "gene":
        ensembl = map_retrieve(id.strip().split(), target_fmt='GENENAME').split("\n")[0]
    return ensembl
