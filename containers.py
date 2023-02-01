from dependency_injector import containers, providers
from temporalio.client import Client


class Container(containers.DeclarativeContainer):
    client = providers.Factory(Client.connect, "localhost:7233")

    temporal_client = providers.Singleton(
        client,
    )
