import inspect
import pkgutil
import configparser
import os
from django.conf import settings
from services.acservice.base import BaseACService
from ac_mediator.exceptions import ImproperlyConfiguredACService, ACException, ACServiceDoesNotExist

SERVICES_CONFIGURATION_FILE = os.path.join(settings.BASE_DIR, 'services/services_conf.cfg')
SERVICES_SCAN_FOLDER = os.path.join(settings.BASE_DIR, 'services/3rd_party/')


def _load_services():
    """
    We walk through the modules in services ac-mediator package and instantiate objects
    for those classes which are subclass of BaseACService.
    :return: list of BaseACService instances
    """
    loaded_services = []
    for importer, modname, ispkg in pkgutil.walk_packages([SERVICES_SCAN_FOLDER], 'services.3rd_party.'):
        if not ispkg:
            module = __import__(modname, fromlist="dummy")
            for name, ftype in inspect.getmembers(module, inspect.isclass):
                if issubclass(ftype, BaseACService) and name != 'BaseACService':
                    loaded_services.append(ftype())
    return loaded_services


def _configure_services(loaded_services):
    """
    Configure loaded services and return a list of those that were successfully configured.
    :param loaded_services: list of BaseACService instances
    :return: list of successfully configures BaseACService instances
    """
    config = configparser.ConfigParser()
    if not os.path.exists(SERVICES_CONFIGURATION_FILE):
        print('No services configuration file has been found, no services will be loaded...')
        return []
    config.read(SERVICES_CONFIGURATION_FILE)
    configured_services = []
    for service in loaded_services:
        try:
            try:
                configuration = config[service.name]
                enabled = configuration['enabled']
                if enabled == 'no':
                    continue
            except KeyError:
                raise ImproperlyConfiguredACService('No configuration section found')
            service.configure(configuration)
            if service.id in [srv.id for srv in configured_services]:
                raise ACException('Each service should have a unique id')
            configured_services.append(service)
        except ImproperlyConfiguredACService as e:
            print('Service {0} could not be configured: {1}'.format(service.name, e))
            continue
    print('Loaded {0} services: {1}'.format(len(configured_services), [service.name for service in configured_services]))
    return configured_services


def _load_and_configure_services():
    loaded_services = _load_services()
    return _configure_services(loaded_services)


available_services = _load_and_configure_services()


def get_available_services(component=None, exclude=None, include=None):
    """
    Get all available services which implement a particular component (or all services if
    'component' is None). Allows excluding particular services and restricting those from which to filter.
    :param component: component (mixin) that should be implemented by returned services
    :param exclude: exclude services passed through this parameter (should be a list of service names)
    :param include: consider only services passed through this parameter (should be a list of service names)
    :return: list of matching services (can be empty)
    """
    out_services = list()
    for service in available_services:
        if component is not None:
            if component not in service.implemented_components:
                continue
        if exclude is not None:
            if service.name in exclude:
                continue
        if include is not None:
            if service.name not in include:
                continue
        out_services.append(service)
    return out_services


def get_service_by_id(service_id):
    for service in available_services:
        if service.id == service_id:
            return service
    raise ACServiceDoesNotExist('Service with id {0} does not exist'.format(service_id))


def get_service_by_name(service_name):
    for service in available_services:
        if service.name == service_name:
            return service
    raise ACServiceDoesNotExist('Service with name {0} does not exist'.format(service_name))
