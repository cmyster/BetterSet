from os import cpu_count
import settings as S


def core_count():
    """
    param: Returns adjusted CPU count for the ThreadPoolExecutor by taking into account the free threads we want to preserve.
    type: None
    return: int
    """
    CPU_COUNT = cpu_count()

    if CPU_COUNT > S.FREE_THREADS:
        CPU_COUNT -= S.FREE_THREADS
    else:
        CPU_COUNT = 1

    return CPU_COUNT
