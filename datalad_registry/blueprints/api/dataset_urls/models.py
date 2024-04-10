from datetime import datetime
from enum import auto
from pathlib import Path
from typing import Optional, Union
from uuid import UUID

from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
    FileUrl,
    NonNegativeInt,
    PositiveInt,
    StrictInt,
    StrictStr,
    validator,
)

from datalad_registry.utils import StrEnum

from ..url_metadata.models import URLMetadataModel, URLMetadataRef

DEFAULT_PAGE = 1  # Default page query param value
DEFAULT_PER_PAGE = 20  # Default per_page query param value


def path_url_must_be_absolute(url):
    """
    Validator for the path URL field that ensures that the URL is absolute
    """
    if isinstance(url, Path) and not url.is_absolute():
        raise ValueError("Path URLs must be absolute")
    return url


class OrderDir(StrEnum):
    """
    Enum for representing the order directions
    """

    asc = auto()
    desc = auto()


class OrderKey(StrEnum):
    """
    Enum for representing the ordering keys
    """

    url = auto()
    annex_key_count = auto()
    annexed_files_in_wt_count = auto()
    annexed_files_in_wt_size = auto()
    last_update_dt = auto()
    git_objects_kb = auto()


class MetadataReturnOption(StrEnum):
    """
    Enum for representing the metadata return options
    """

    reference = auto()
    content = auto()


class PathParams(BaseModel):
    """
    Pydantic model for representing the path parameters for API endpoints related to
    dataset URLs.
    """

    id: int = Field(..., description="The ID of the dataset URL")


class QueryParams(BaseModel):
    """
    Pydantic model for representing the query parameters to query
    the dataset_urls endpoint
    """

    search: Optional[str] = Field(
        None,
        description="A search string used to perform a search identical to the one "
        "offered by the Web UI. Please consult the Web UI for the expected "
        "syntax of this search string by clicking on "
        'the "Show Search Query Syntax" button.',
        regex=r".*\S.*",
    )

    url: Optional[Union[FileUrl, AnyUrl, Path]] = Field(None, description="The URL")

    ds_id: Optional[UUID] = Field(None, description="The ID, a UUID, of the dataset")

    min_annex_key_count: Optional[int] = Field(
        None, description="The minimum number of annex keys "
    )
    max_annex_key_count: Optional[int] = Field(
        None, description="The maximum number of annex keys "
    )

    min_annexed_files_in_wt_count: Optional[int] = Field(
        None, description="The minimum number of annexed files in the working tree"
    )
    max_annexed_files_in_wt_count: Optional[int] = Field(
        None, description="The maximum number of annexed files in the working tree"
    )

    min_annexed_files_in_wt_size: Optional[int] = Field(
        None,
        description="The minimum size of annexed files in the working tree in bytes",
    )
    max_annexed_files_in_wt_size: Optional[int] = Field(
        None,
        description="The maximum size of annexed files in the working tree in bytes",
    )

    earliest_last_update: Optional[datetime] = Field(
        None,
        description="The earliest last update time",
    )
    latest_last_update: Optional[datetime] = Field(
        None,
        description="The latest last update time",
    )

    min_git_objects_kb: Optional[int] = Field(
        None, description="The minimum size of the `.git/objects` in KiB"
    )
    max_git_objects_kb: Optional[int] = Field(
        None, description="The maximum size of the `.git/objects` in KiB"
    )

    processed: Optional[bool] = Field(
        None,
        description="Whether an initial processing has been completed "
        "on the dataset URL",
    )

    cache_path: Optional[Path] = Field(
        None,
        description="The path, relative or full, of the cached clone of the dataset at "
        "the URL in the local file system, the file system of the "
        "Celery worker. If the path is relative, it is relative to the base cache path."
        " If the path is full, only the last three components of the path are used "
        "in the query.",
    )

    return_metadata: Optional[MetadataReturnOption] = Field(
        None,
        description="Whether and how to return metadata of the datasets at the URLs. "
        "If this query parameter is not provided, "
        "each returned dataset URL object will not contain a `metadata` field. "
        'If this query parameter is "reference", '
        "the `metadata` field of each returned dataset URL object will be a list of "
        "objects each presenting a reference link to a piece of metadata "
        "of the dataset at the URL. "
        'If this query parameter is "content", the `metadata` field '
        "of each returned dataset URL object will be a list of objects "
        "each presenting a piece of metadata of the dataset at the URL.",
    )

    # Pagination parameters
    page: PositiveInt = Field(
        DEFAULT_PAGE,
        description="The current page (used to calculate the offset "
        f"of the pagination). Defaults to {DEFAULT_PAGE}.",
    )
    per_page: PositiveInt = Field(
        DEFAULT_PER_PAGE,
        description="The maximum number of items on a page "
        "(used to calculate the offset and limit of the pagination). "
        f"Defaults to {DEFAULT_PER_PAGE}.",
    )

    # Ordering parameters
    order_by: OrderKey = Field(
        OrderKey.last_update_dt,
        description="The key to use to order the items in the query",
    )
    order_dir: OrderDir = Field(
        OrderDir.desc, description="The direction to order the items in the query"
    )

    # Validator
    _path_url_must_be_absolute = validator("url", allow_reuse=True)(
        path_url_must_be_absolute
    )


class DatasetURLSubmitModel(BaseModel):
    """
    Model for representing the database model RepoUrl for submission communication
    """

    url: Union[FileUrl, AnyUrl, Path] = Field(..., description="The URL")

    # Validator
    _path_url_must_be_absolute = validator("url", allow_reuse=True)(
        path_url_must_be_absolute
    )


class DatasetURLRespBaseModel(DatasetURLSubmitModel):
    """
    Base model for `DatasetURLRespModel`

    All fields defined in this model are intended to be populated
    from an orm model object directly.
    """

    id: int = Field(..., description="The ID of the dataset URL")
    ds_id: Optional[UUID] = Field(None, description="The ID, a UUID, of the dataset")
    head_describe: Optional[str] = Field(
        None,
        description="The output of `git describe --tags --always` on the dataset",
    )
    annex_key_count: Optional[int] = Field(None, description="The number of annex keys")
    annexed_files_in_wt_count: Optional[int] = Field(
        None, description="The number of annexed files in the working tree"
    )
    annexed_files_in_wt_size: Optional[int] = Field(
        None, description="The size of annexed files in the working tree in bytes"
    )
    last_update_dt: Optional[datetime] = Field(
        None,
        description="The last time the local copy of the dataset was updated",
    )
    git_objects_kb: Optional[int] = Field(
        None, description="The size of the `.git/objects` in KiB"
    )
    processed: bool = Field(
        description="Whether an initial processing has been completed "
        "on the dataset URL"
    )
    last_chk_dt: Optional[datetime] = Field(
        None, description="The datetime the last check for update was performed"
    )

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class DatasetURLRespModel(DatasetURLRespBaseModel):
    """
    Model for representing the database model RepoUrl in response communication
    """

    metadata: Optional[Union[list[URLMetadataModel], list[URLMetadataRef]]] = Field(
        None, alias="metadata_", description="The metadata of the dataset at the URL"
    )

    class Config:
        # Ensure the JSON schema of the model uses the field name
        # instead of the alias to name a field
        by_alias = False


class AnnexDsCollectionStats(BaseModel):
    """
    Model with the base components of annex dataset collection statistics
    """

    ds_count: NonNegativeInt = Field(description="The number of datasets")
    size_of_annexed_files: NonNegativeInt = Field(
        description="The size of annexed files"
    )
    annexed_file_count: NonNegativeInt = Field(
        description="The number of annexed files"
    )


class DataladDsCollectionStats(BaseModel):
    """
    Model for DataLad dataset collection statistics
    """

    unique_ds_stats: AnnexDsCollectionStats = Field(
        description="Statistics for unique datasets"
    )
    stats: AnnexDsCollectionStats = Field(
        description="Statistics for all datasets, as individual repos, "
        "without any deduplication"
    )


class NonAnnexDsCollectionStats(BaseModel):
    """
    Model for non-annex dataset collection statistics
    """

    ds_count: NonNegativeInt = Field(
        description="The number of datasets, as individual repos, "
        "without any deduplication"
    )


class StatsSummary(BaseModel):
    unique_ds_count: NonNegativeInt = Field(description="The number of unique datasets")
    ds_count: NonNegativeInt = Field(
        description="The number of datasets, as individual repos, "
        "without any deduplication"
    )


class CollectionStats(BaseModel):
    datalad_ds_stats: DataladDsCollectionStats = Field(
        description="Statistics for DataLad datasets"
    )
    pure_annex_ds_stats: AnnexDsCollectionStats = Field(
        description="Statistics for pure annex datasets, as individual repos, "
        "without any deduplication"
    )
    non_annex_ds_stats: NonAnnexDsCollectionStats = Field(
        description="Statistics for non-annex datasets"
    )

    summary: StatsSummary = Field(description="Summary statistics")


class DatasetURLPage(BaseModel):
    """
    Model for representing a page of dataset URLs in response communication
    """

    total: StrictInt = Field(
        description="The total number of dataset URLs across all pages"
    )
    cur_pg_num: StrictInt = Field(description="The number of the current page")
    prev_pg: Optional[StrictStr] = Field(
        None, description="The link to the previous page"
    )
    next_pg: Optional[StrictStr] = Field(None, description="The link to the next page")
    first_pg: StrictStr = Field(description="The link to the first page")
    last_pg: StrictStr = Field(description="The link to the last page")

    dataset_urls: list[DatasetURLRespModel] = Field(
        description="The list of dataset URLs in the current page"
    )
    collection_stats: CollectionStats = Field(
        description="Statistics about the collection of dataset URLs, "
        "not just the URLs in the current page but the entire collection "
        "returned"
    )
