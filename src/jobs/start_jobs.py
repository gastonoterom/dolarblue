from asyncio import sleep, get_running_loop
import schedule  # type: ignore
from src.jobs.scheduled_jobs import send_dolarblue_update_request


def start_all_jobs():
    """This function starts all the scheduled jobs asyncronously.

    Every minute it checks if there are any scheduled jobs pending and it runs them"""
    async def start_all_jobs_async():
        # The waiting is async, but each routine is run, of course, sync, so be carefull with
        # its execution time
        schedule.every().hour.do(send_dolarblue_update_request)

        while True:
            schedule.run_pending()
            await sleep(60)

    loop = get_running_loop()
    loop.create_task(start_all_jobs_async())
