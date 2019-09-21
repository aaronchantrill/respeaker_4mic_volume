# -*- coding: utf-8 -*-
from gpiozero import LED
from gpiozero.exc import GPIODeviceClosed
import spidev
from naomi import plugin


class RespeakerVisualizationsPlugin(plugin.VisualizationsPlugin):
    red = [255, 0, 0, 128]  # brightness, blue, green, red
    green = [255, 0, 128, 0]
    blue = [255, 192, 0, 0]
    lt_blue = [255, 4, 0, 0]
    yellow = [255,4,4,0]
    settings = OrderedDict(
        [
            (
                ("visualizations","respeaker"), {
                    title: "Do you want to use the respeaker visualizations?",
                    description: "This will display microphone levels on the SeeedStudio Respeaker 4mic Raspberry Pi hat"
                }
            )
        ]
    )

    def __init__(self, *args, **kwargs):
        super(RespeakerVisualizationsPlugin, self).__init__(*args, **kwargs)

        num_leds = 12
        self.displaywidth = num_leds
        
        self.spi = spidev.SpiDev()
        bus = 0
        device = 1
        self.spi.open(bus, device)  # open the SPI device
        self.spi.max_speed_hz = 8000000  # I have no idea what this does
        self.power = LED(5)
        self.power.on()  # send power to the LED display

    def mic_volume(self, *args, **kwargs):
        try:
            recording = kwargs['recording']
            snr = kwargs['snr']
            minsnr = kwargs['minsnr']
            maxsnr = kwargs['maxsnr']
            mean = kwargs['mean']
            threshold = kwargs['threshold']
        except KeyError:
            return
        snrrange = maxsnr - minsnr
        # without the list on the next line, feedback gets set to point to
        # the self.red or self.green variables, so entending it extends the
        # class variable.
        feedback = self.red.copy() if recording else self.green.copy()
        feedback.extend(
            self.blue * int(self.displaywidth * ((snr-minsnr) / snrrange))
        )
        feedback.extend(
            self.lt_blue * int(self.displaywidth * ((maxsnr-snr) / snrrange))
        )
        if minsnr < threshold < maxsnr:
            threshold_led = int(self.displaywidth * ((threshold - minsnr) / snrrange))
            feedback[threshold_led * 4:threshold_led * 4 + 4] = self.yellow
        self.spi.xfer2([0] * 4)
        self.spi.xfer2(feedback[:48])
        self.spi.xfer2([0x00])
