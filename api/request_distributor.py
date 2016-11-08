from ac_mediator.exceptions import ACException
from services.management import get_available_services
from api.response_aggregator import get_response_aggregator


response_aggregator = get_response_aggregator()


class RequestDistributor(object):

    @staticmethod
    def process_request(request):
        """
        Process incoming request, and propagate it to corresponding services.
        TODO: properly design and implement this. Current test implementation is synchronous and blocking...
        :param request: incoming request
        :return:
        """

        services = get_available_services(component=request['component'])
        # Create object to store response contents
        response_id = response_aggregator.create_response(n_expected_responses=len(services))
        response_aggregator.set_response_to_processing(response_id)

        for service in services:
            # Query each service and aggregate results from each service
            try:
                service_response = getattr(service, request['method'])(**request['kwargs'])
            except ACException as e:
                # Aggregate error response in response aggregator and continue with next service
                response_aggregator.aggregate_response(response_id, service.name, e)
                continue
            response_aggregator.aggregate_response(response_id, service.name, service_response)
            """
            NOTE: current implementation is synchronous and blocking, it calls every service
            sequentially and adds the results to the created response object. Once all
            have finished it sets the response status to finished and returns the contents of the
            response.
            The idea is that this process should be asynchronous and non-blocking. Different 3rd party
            services would be queried in parallel and responses aggregated bit by bit in the aggregator.
            Here we would return just the response id and then the client (or some other piece in our
            software) would be in charge of iteratively checking if all desired results have been aggregated
            and then return them once all have finished (or return them partially upon request).
            """
        return response_id


request_distributor = RequestDistributor()


def get_request_distributor():
    return request_distributor
