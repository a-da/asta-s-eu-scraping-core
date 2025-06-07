from pathlib import Path
from shutil import rmtree

from asta_s_eu.scraping.core.prospect_database.local_file_system import \
    LocalFileSystem


def test_crud_local_file_system():
    """
    GIVEN prospect database object
    WHEN capture a new prospect
    AND capture the same prospect again
    THEN it has to not be added into database since it already there
    """
    path = Path(__file__).parent / 'tmp_test_prospect_database.db'
    if path.exists():
        rmtree(path)

    banana_prospect = {
        'product_id': 'banana-id',
        'key': 'value'
    }
    db = LocalFileSystem(path)
    assert db.capture([banana_prospect]) == [banana_prospect]

    assert not db.capture([banana_prospect])

    rmtree(path)
