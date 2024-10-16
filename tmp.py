from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union

from mmengine.fileio import (BaseStorageBackend, get_file_backend,
                             list_from_file)
from mmengine.logging import MMLogger

from mmcls.registry import DATASETS

def find_folders(
    root: str,
    backend: Optional[BaseStorageBackend] = None
) -> Tuple[List[str], Dict[str, int]]:
    """Find classes by folders under a root.

    Args:
        root (string): root directory of folders
        backend (BaseStorageBackend | None): The file backend of the root.
            If None, auto infer backend from the root path. Defaults to None.

    Returns:
        Tuple[List[str], Dict[str, int]]:

        - folders: The name of sub folders under the root.
        - folder_to_idx: The map from folder name to class idx.
    """
    # Pre-build file backend to prevent verbose file backend inference.
    backend = backend or get_file_backend(root, enable_singleton=True)
    print(backend)
    folders = list(
        backend.list_dir_or_file(
            root,
            list_dir=True,
            list_file=True,
            recursive=True,
        ))
    folders.sort()
    folder_to_idx = {folders[i]: i for i in range(len(folders))}
    return folders, folder_to_idx


if __name__ == '__main__':
    print(find_folders('/mnt/e/data/cat_dataset_coco/images/'))