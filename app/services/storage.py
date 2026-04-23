import uuid
import logging
from datetime import datetime
from typing import Optional
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

from app.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    def __init__(self):
        self.blob_service_client: Optional[BlobServiceClient] = None
        self.container_client: Optional[ContainerClient] = None

    def connect(self) -> None:
        connection_string = (
            f"DefaultEndpointsProtocol=http;"
            f"AccountName={settings.azurite_account_name};"
            f"AccountKey={settings.azurite_account_key};"
            f"BlobEndpoint={settings.azurite_blob_endpoint};"
        )

        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self._create_container()
        logger.info(f"Connected to Azurite at {settings.azurite_blob_endpoint}")

    def _create_container(self) -> None:
        try:
            self.container_client = self.blob_service_client.create_container(
                settings.azurite_container_name, public_access="blob"
            )
            logger.info(f"Container '{settings.azurite_container_name}' created")
        except ResourceExistsError:
            self.container_client = self.blob_service_client.get_container_client(
                settings.azurite_container_name
            )
            logger.info(f"Container '{settings.azurite_container_name}' already exists")

    def store(self, contenido: str) -> str:
        evidence_id = str(uuid.uuid4())
        blob_name = f"{evidence_id}.json"

        metadata = {
            "created_at": datetime.utcnow().isoformat(),
            "content_type": "text/plain",
        }

        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(contenido, overwrite=True, metadata=metadata)

        logger.info(f"Evidence {evidence_id} stored successfully")
        return evidence_id

    def retrieve(self, evidence_id: str) -> Optional[dict]:
        blob_name = f"{evidence_id}.json"
        blob_client = self.container_client.get_blob_client(blob_name)

        try:
            blob_data = blob_client.download_blob()
            contenido = blob_data.readall()

            metadata = blob_client.get_blob_properties().metadata

            return {
                "id": evidence_id,
                "contenido": contenido.decode("utf-8"),
                "created_at": metadata.get("created_at", datetime.utcnow().isoformat()),
                "content_type": metadata.get("content_type", "text/plain"),
            }
        except ResourceNotFoundError:
            logger.warning(f"Evidence {evidence_id} not found")
            return None

    def delete(self, evidence_id: str) -> bool:
        blob_name = f"{evidence_id}.json"
        blob_client = self.container_client.get_blob_client(blob_name)

        try:
            blob_client.delete_blob()
            logger.info(f"Evidence {evidence_id} deleted")
            return True
        except ResourceNotFoundError:
            logger.warning(f"Evidence {evidence_id} not found for deletion")
            return False


storage_service = StorageService()
