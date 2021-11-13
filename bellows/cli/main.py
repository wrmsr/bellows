import logging
import time

import click
import click_log

from bellows.config import CONF_DEVICE, CONF_DEVICE_BAUDRATE, CONF_FLOW_CONTROL

from . import opts


###

import sys
import threading
import traceback


log = logging.getLogger(__name__)


def dump_threads():
    frames_by_id = sys._current_frames()
    for thrd in threading.enumerate():
        log.info(str(thrd))
        thrd_frame = frames_by_id.get(thrd.ident)
        if thrd_frame is None:
            log.info('???')
        else:
            log.info(''.join(traceback.format_stack(thrd_frame)))


def thread_dump_proc():
    while True:
        try:
            dump_threads()
        except:
            log.exception('thread_dumper_proc exception')
        time.sleep(5)


###

@click.group()
@click_log.simple_verbosity_option(logging.getLogger(), default="WARNING")
@opts.device
@opts.baudrate
@opts.flow_control
@click.pass_context
def main(ctx, device, baudrate, flow_control):
    thread_dump_thread = threading.Thread(target=thread_dump_proc, daemon=True)
    thread_dump_thread.start()

    ctx.obj = {
        CONF_DEVICE: device,
        CONF_DEVICE_BAUDRATE: baudrate,
        CONF_FLOW_CONTROL: flow_control,
    }
    click_log.basic_config()
    logging.root.setLevel(logging.INFO)

if __name__ == "__main__":
    main()
