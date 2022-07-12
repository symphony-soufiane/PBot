#!/usr/bin/env python3
import asyncio
import logging.config
from pathlib import Path

from symphony.bdk.core.activity.command import CommandContext
from symphony.bdk.core.config.loader import BdkConfigLoader
from symphony.bdk.core.symphony_bdk import SymphonyBdk

# Configure logging
current_dir = Path(__file__).parent.parent
logging_conf = Path.joinpath(current_dir, 'resources', 'logging.conf')
logging.config.fileConfig(logging_conf, disable_existing_loggers=False)


async def run():
    config = BdkConfigLoader.load_from_file(Path.joinpath(current_dir, 'resources', 'config.yaml'))

    async with SymphonyBdk(config) as bdk:
        datafeed_loop = bdk.datafeed()
        activities = bdk.activities()

        @activities.slash("/ping")
        async def ping(context: CommandContext):
            response = f"<messageML>pong</messageML>"
            await bdk.messages().send_message(context.stream_id, response)

        # Start the datafeed read loop
        await datafeed_loop.start()


# Start the main asyncio run
try:
    logging.info("Running bot application...")
    asyncio.run(run())
except KeyboardInterrupt:
    logging.info("Ending bot application")
