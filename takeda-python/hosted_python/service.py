from tempfile import TemporaryDirectory
from logging import getLogger, Logger, basicConfig, INFO

from aiohttp import ClientSession, ClientResponse
import os

from output_data.main import get_report_values_files

basicConfig(level=INFO)

logger: Logger = getLogger(__name__)

_AUTHORIZATION_SCHEME = "Bearer"


def transform(access_token: str):
    working_directory = TemporaryDirectory(delete=False)
    docugami_client: ClientSession = ClientSession(
        headers={"Authorization": _AUTHORIZATION_SCHEME + " " + access_token}
    )
    return working_directory, docugami_client


def create_path_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        logger.info("Path already exists")
    return


async def download_output_file(output_directory, response, file_name):
    # check if the output directory exists
    create_path_if_not_exists(output_directory)

    file_path = os.path.join(output_directory, file_name)
    with open(file_path, 'wb') as f:
        f.write(await response.content.read())
    return file_path


async def download_and_get_output_file(docugami_request):
    working_directory, docugami_client = transform(docugami_request.accessToken)
    try:
        artifact_url: str = docugami_request.artifact.url
        file_name: str = docugami_request.artifact.name
        download_url: str = artifact_url + "/content"
        download_stream: ClientResponse = await docugami_client.get(download_url)
        if download_stream.status == 200:
            logger.info("download started")
            download_path = await download_output_file(working_directory.name, download_stream, file_name)
            logger.info("download completed : {}".format(download_path))

        # get the output file for the downloaded file
        output_file_path = await get_report_values_files(working_directory.name, file_name)
        logger.info("output file saved: {}".format(output_file_path))

    finally:
        await docugami_client.close()
        # rmtree(working_directory.name, ignore_errors=True)
