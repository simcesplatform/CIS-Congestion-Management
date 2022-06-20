# -*- coding: utf-8 -*-
# Copyright 2021 Tampere University and VTT Technical Research Centre of Finland
# This software was developed as a part of the ProCemPlus project: https://www.senecc.fi/projects/procemplus
# This software was developed as a part of EU project INTERRFACE: http://www.interrface.eu/.
#  This source code is licensed under the MIT license. See LICENSE in the repository root directory.
# Author(s): Mehdi Attar <mehdi.attar@tuni.fi>
#            Ville Heikkilä <ville.heikkila@tuni.fi>


import asyncio
import json
# from multiprocessing import _BoundedSemaphoreType
#from typing import Any, cast, Set, Union, Dict, List

from tools.components import AbstractSimulationComponent
from tools.exceptions.messages import MessageError
# from tools.messages import BaseMessage
from tools.tools import FullLogger, load_environmental_variables

from Fetcher import JsonFileCIS

# import all the required messages from installed libraries
from CIS.CISCustomerMessage import CISCustomerMessage

# initialize logging object for the module
LOGGER = FullLogger(__name__)

# topics
CIS_DATA_TOPIC = "CIS_DATA_TOPIC"

# time interval in seconds on how often to check whether the component is still running
TIMEOUT = 2.0

# input file name
CIS_JSON_FILE = "CIS_JSON_FILE"


class CIS(AbstractSimulationComponent): # the NIS class inherits from AbstractSimulationComponent class
    """
    The CIS component is initialized in the beginning of the simulation by the platform manager.
    CIS gets its input data (CIS data) from the json file containing the customer data.
    the JSON structure for customer data is available:
    https://simcesplatform.github.io/energy_msg-init-cis-customerinfo/
    """

    # Constructor
    def __init__(
            self,
            customer_data: dict):
        """
        The CIS component is initiated in the beginning of the simulation by the simulation manager
        and in epoch 1, it publishes the CIS data. The CIS data is fetched using a class called Fetcher.
        """

        super().__init__()
        self._customer_data = customer_data

        # Load environmental variables for those parameters that were not given to the constructor.
        environment = load_environmental_variables(
            (CIS_DATA_TOPIC, str, "Init.CIS.CustomerInfo")
        )
        self.CustomerDataTopic=environment[CIS_DATA_TOPIC]
        # The easiest way to ensure that the component will listen to all necessary topics

    def clear_epoch_variables(self) -> None:
        """Clears all the variables that are used to store information about the received input within the
           current epoch. This method is called automatically after receiving an epoch message for a new epoch.

           NOTE: this method should be overwritten in any child class that uses epoch specific variables
        """
        pass

    async def process_epoch(self) -> bool:
        """
        Process the epoch and do all the required calculations.
        Returns False, if processing the current epoch was not yet possible.
        Otherwise, returns True, which indicates that the epoch processing was fully completed.
        This also indicated that the component is ready to send a Status Ready message to the Simulation Manager.
        """
        # create and send CISCustomerMessage
        if self._latest_epoch==1:      # CISCustomerMessage is only needed to be published in the first epoch
            try:
                customer_message = self._message_generator.get_message(
                    CISCustomerMessage,
                    EpochNumber=self._latest_epoch,
                    TriggeringMessageIds=self._triggering_message_ids,
                    ResourceId=self._customer_data["ResourceId"],
                    CustomerId=self._customer_data["CustomerId"],
                    BusName=self._customer_data["BusName"]
                )

            except (ValueError, TypeError, MessageError) as message_error:
                # When there is an exception while creating the message, it is in most cases a serious error.
                LOGGER.error(f"{type(message_error).__name__}: {message_error}")
                await self.send_error_message("Internal error when creating customer message.")
                return False

            await self._send_message(customer_message, self.CustomerDataTopic)

        # return True to indicate that the component is finished with the current epoch
        return True

    async def _send_message(self, MessageContent, Topic):
        await self._rabbitmq_client.send_message(
            topic_name=Topic,
            message_bytes=MessageContent.bytes())


def create_component() -> CIS:         # Factory function. making instance of the class
    """
    Creates and returns a NIS Component based on the environment variables.
    """
    env_variables = load_environmental_variables(
        (CIS_JSON_FILE, str, None )
    )
    LOGGER.warning("before opening the file")

    json_file = JsonFileCIS(env_variables[CIS_JSON_FILE]) # creating an object of JsonFileCIS class 
    LOGGER.warning("after opening the file")
    customer_data_content = json_file.get_data()
    return CIS(customer_data_content)    # the birth of the NIS object


async def start_component():
    """
    Creates and starts a SimpleComponent component.
    """

    simple_component = create_component()

    # The component will only start listening to the message bus once the start() method has been called.
    await simple_component.start()

    # Wait in the loop until the component has stopped itself.
    while not simple_component.is_stopped:
        await asyncio.sleep(TIMEOUT)


if __name__ == "__main__":
    asyncio.run(start_component())
