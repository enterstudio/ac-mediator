# Some of these concept definitions should be linked with the ontology (or be loaded from it)

# Authentication
APIKEY_AUTH_METHOD = 'apikey_auth'
ENDUSER_AUTH_METHOD = 'enduser_auth'

# Resource fields (just using fake names here)
FIELD_ID = 'id'
FIELD_URL = 'url'
FIELD_NAME = 'name'
FIELD_LICENSE = 'license'
FIELD_AUTHOR_NAME = 'author_name'
FIELD_TAGS = 'tags'
FIELD_STATIC_RETRIEVE = 'static_retrieve'

MINIMUM_RESOURCE_DESCRIPTION_FIELDS = [
    FIELD_ID,
    FIELD_URL,
    FIELD_NAME,
    FIELD_AUTHOR_NAME,
    FIELD_TAGS,
    FIELD_LICENSE,
    FIELD_STATIC_RETRIEVE
]

# Search results parameters
NEXT_PAGE_PROP = 'next'
PREV_PAGE_PROP = 'prev'
NUM_RESULTS_PROP = 'num_results'
RESULTS_LIST = 'results'

# Licenses
LICENSE_UNKNOWN = 'Unknown'
LICENSE_CC0 = 'CC0'
LICENSE_CC_BY = 'BY'
LICENSE_CC_BY_SA = 'BY-SA'
LICENSE_CC_BY_NC = 'BY-NC'
LICENSE_CC_BY_ND = 'BY-ND'
LICENSE_CC_BY_NC_SA = 'BY-NC-SA'
LICENSE_CC_BY_NC_ND = 'BY-NC-ND'
LICENSE_CC_SAMPLING_PLUS = 'Sampling+'
