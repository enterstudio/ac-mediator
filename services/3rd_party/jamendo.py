from ac_mediator.exceptions import ACLicesningException
from services.acservice.constants import *
from services.acservice.utils import *
from services.acservice.base import BaseACService
from services.acservice.auth import ACServiceAuthMixin
from services.acservice.search import ACServiceTextSearch, translates_field
from services.acservice.licensing import ACLicensingMixin


class JamendoService(BaseACService, ACServiceAuthMixin, ACServiceTextSearch, ACLicensingMixin):

    # General
    NAME = 'Jamendo'
    URL = 'http://www.jamendo.com'
    API_BASE_URL = 'https://api.jamendo.com/v3.0/'

    # Auth
    SUPPORTED_AUTH_METHODS = [APIKEY_AUTH_METHOD, ENDUSER_AUTH_METHOD]
    BASE_AUTHORIZE_URL = API_BASE_URL + 'oauth/authorize/?client_id={0}'
    ACCESS_TOKEN_URL = API_BASE_URL + 'oauth/grant/'
    REFRESH_TOKEN_URL = API_BASE_URL + 'oauth/grant/'

    def access_token_request_data(self, authorization_code):
        # Jamendo needs to include 'redirect_uri' in the access token request
        data = super(JamendoService, self).access_token_request_data(authorization_code)
        data.update({'redirect_uri': self.get_redirect_uri()})
        return data

    def get_auth_info_for_request(self, auth_method, account=None):
        if auth_method == ENDUSER_AUTH_METHOD:
            return {'params': {'access_token': self.get_enduser_token(account)}}
        else:
            return {'params': {'client_id': self.service_client_id}}

    # Search
    TEXT_SEARCH_ENDPOINT_URL = API_BASE_URL + 'tracks/'

    @property
    def direct_fields_mapping(self):
        return {
            FIELD_URL: 'shareurl',
            FIELD_NAME: 'name',
            FIELD_AUTHOR_NAME: 'artist_name',
            FIELD_STATIC_RETRIEVE: 'audiodownload',
        }

    @translates_field(FIELD_TAGS)
    def translate_field_tags(self, result):
        try:
            tags = result['musicinfo']['tags']['genres'] + result['musicinfo']['tags']['instruments'] + result['musicinfo']['tags']['vartags']
        except KeyError:
            tags = []
        return tags

    @translates_field(FIELD_LICENSE)
    def translate_field_license(self, result):
        return translate_cc_license_url(result['license_ccurl'])

    def format_search_response(self, response):
        results = list()
        for result in response['results']:
            results.append(self.translate_single_result(result))
        return {
            NUM_RESULTS_PROP: None,  # TODO: work out this param
            NEXT_PAGE_PROP: None,  # TODO: work out this param
            PREV_PAGE_PROP: None,  # TODO: work out this param
            RESULTS_LIST: results,
        }

    def text_search(self, query):
        # TODO: add minimum response fields?
        response = self.send_request(
            self.TEXT_SEARCH_ENDPOINT_URL,
            params={'search': query, 'include': 'musicinfo+licenses'},
        )
        return self.format_search_response(response)

    # Licensing
    def get_licensing_url(self, acid=None, resource_dict=None):
        if acid is None and resource_dict is None:
            raise ACLicesningException(
                'Either \'acid\' or \'resoruce_dict\' should be provided to \'get_licensing_url\'', 400)
        if resource_dict is None:
            # Translate ac resource id to Jamendo resource id
            if not acid.startswith(self.id_prefix):
                raise ACLicesningException('Invalid resource id \'{0}\''.format(acid), 400)
            resource_id = acid[len(self.id_prefix):]
            # If no resource dict is provided, make a request to Jamendo to retrieve resource data
            response = self.send_request(
                self.TEXT_SEARCH_ENDPOINT_URL,
                params={'id': resource_id, 'include': 'licenses'},
            )
            if response['headers']['results_count'] != 1:
                raise ACLicesningException('Response does not contain expected results.', 500)
            resource_dict = response['results'][0]
        return resource_dict.get('prourl', None)
