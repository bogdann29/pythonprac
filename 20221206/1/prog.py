import asyncio

event = asyncio.Event()


async def writer(queue, delay):
    i = 0
    while True:
        await queue.put(f"{i}_{delay}")
        await asyncio.sleep(delay)
        if event.is_set():
            break
        i += 1


async def stacker(queue, stack):
    while True:
        t = await queue.get()
        await stack.put(t)
        if event.is_set():
            break


async def reader(stack, num, delay):
    for i in range(num):
        res = await stack.get()
        print(res)
        await asyncio.sleep(delay)
    event.set()


async def main():
    d1, d2, d3, n = eval(input())
    queue = asyncio.Queue()
    stack = asyncio.LifoQueue()
    tsk1 = asyncio.create_task(
        writer(queue, d1)
    )
    tsk2 = asyncio.create_task(
        writer(queue, d2)
    )
    tsk3 = asyncio.create_task(
        stacker(queue, stack)
    )
    tsk4 = asyncio.create_task(
        reader(stack, n, d3)
    )
    await tsk1
    await tsk2
    await tsk3
    await tsk4


asyncio.run(main())