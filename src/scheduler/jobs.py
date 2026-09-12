from jobs.stocks import StockJob


def register_jobs(scheduler, stock_service):

    stock_job = StockJob(stock_service)

    scheduler.add_interval_job(
        stock_job.run,
        minutes=15,
        job_id="stock_data",
    )

    # scheduler.add_job(
    #    # download_service.cleanup_downloads,
    #     "interval",
    #     hours=6,
    #     kwargs={"max_age_days": 7},
    # )