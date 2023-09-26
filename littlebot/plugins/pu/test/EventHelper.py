import asyncio
import time

from x_mock.m_mock import m_mock


def get_time():
    return m_mock.mock('@time("%H:%M:%S.%f")')


async def case_a():
    print('start', get_time(), 'case_a')
    await asyncio.sleep(2)  # 只阻塞当前函数,所以比case_b 多等 1s,下面这句最后打印
    print('end', get_time(), 'case_a')


async def case_b():
    print('start', get_time(), 'case_b')
    await asyncio.sleep(1)
    print('end', get_time(), 'case_b')


async def main():
    await asyncio.gather(
        case_a(),
        case_b()
    )


if __name__ == '__main__':
    start = time.time()
    # asyncio.run(main())  # 运行方式1

    # 运行方式2
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(time.time() - start)
