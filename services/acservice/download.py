from services.acservice.constants import DOWNLOAD_COMPONENT


class ACDownloadMixin(object):
    """
    Mixin that defines methods to allow downloading (retrieval) of Audio Commons content.
    To download content, the Audio Commons API must be able to provide the client with a url
    where content can be downloaded without the need of any authentication. In this way the
    client can download from the service without transferring data through the mediator and
    without knowing anything about the third party service.
    Services are expected to override methods to adapt them to their own APIs.
    """

    def conf_download(self, conf):
        self.implemented_components.append(DOWNLOAD_COMPONENT)

    def get_download_url(self, acid, *args, **kwargs):
        """
        Given an Audio Commons unique resource identifier (acid), this function returns a url
        where the resource can be downloaded by the client without the need of extra authentication.
        If the 3rd party service can't provide a link to download that resource or some other errors
        occur during the collection of the url, an ACDownloadException should be raised.
        Individual services can extend this method with extra parameters to make it more suitable to their
        needs (e.g., to call the method given an already retrieved resource and avoid in this way an
        extra request).
        :return: url to download the input resource (string)
        """
        raise NotImplementedError("Service must implement method ACLicensingMixin.get_download_url")

    def download(self, acid, *args, **kwargs):
        """
        This endpoint returns a download url and raises warnings that might contain relevant
        information for the application. To get the URL, it uses 'get_download_url' method, therefore
        'get_download_url' is the main method that should be overwritten by third party services.
        Raise warnings using the BaseACService.add_response_warning method.
        :param acid: Audio Commons unique resource identifier
        :return: url where to download the resource
        """
        return self.get_download_url(acid, *args, **kwargs)
