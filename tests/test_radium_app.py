import shutil

import pytest

from main import *

DIRECTORY = os.path.join(os.getcwd(), "temp/")
LINK = ('https://gitea.radium.group/radium/project-configuration', 'https://github.com/', 'https://leetcode.com/')


@pytest.mark.parametrize('num_of_req, link, directory, result', [(5, LINK[0], DIRECTORY, 5),
                                                                 (10, LINK[1], DIRECTORY, 10),
                                                                 (15, LINK[2], DIRECTORY, 15),
                                                                 ])
def test_run_async_positive(num_of_req, link, directory, result):
    os.mkdir(f'{directory}')
    asyncio.run(run_async(num_of_req, link, directory))
    assert len(os.listdir(f'{directory}')) == result
    shutil.rmtree(f"{directory}")


def test_make_hash_positive():
    os.mkdir(f'{DIRECTORY}')
    asyncio.run(run_async(5, LINK[0], DIRECTORY))
    hash_list = make_hash(DIRECTORY)
    assert hash_list[0] != hash_list[1]
    assert hash_list[0] != hash_list[-1]
    hash_list2 = make_hash(DIRECTORY)
    assert hash_list == hash_list2
    shutil.rmtree(f"{DIRECTORY}")
