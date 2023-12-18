# CIS

## Introduction

CIS components to be used in SimCES.

The component publishes the [customer](https://simcesplatform.github.io/energy_msg-init-cis-customerinfo/) information system data.

## Requirements

- python
- pip for installing requirements

Install requirements:

```bash
# optional create a virtual environment:
python3 -m venv .env
# activate it
. .env/bin/activate # *nix
.env\scripts\activate # windows.
# install required packages
pip install -r requirements.txt
```

## **Workflow of CIS**

1. CIS publishes the [customer ](https://simcesplatform.github.io/energy_msg-init-cis-customerinfo/)relared data.

## **Epoch workflow**

In beginning of the simulation the CIS component will wait for [SimState](https://simcesplatform.github.io/core_msg-simstate/)(running) message, when the message is received component will initialize and send [Status](https://simcesplatform.github.io/core_msg-status/)(Ready) message with epoch number 0. If SimState(stopped) is received component will close down. Other message are ignored at this stage.

After startup component will begin to listen for [epoch](https://simcesplatform.github.io/core_msg-epoch/) messages. In the current implementation, it only publishes the customer information data in the epoch 1. For other epoches other than 1, it only sends ready message when epoch starts.

If at any stage of the execution Status (Error) message is received component will immediately close down

## **Implementation details**

* Language and platform

| Programming language | Python 3.11.4                                              |
| -------------------- | ---------------------------------------------------------- |
| Operating system     | Docker version 20.10.21 running on windows 10 version 22H2 |

## **External packages**

The following packages are needed.

| Package          | Version   | Why needed                                                                                | URL                                                                                                   |
| ---------------- | --------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Simulation Tools | (Unknown) | "Tools for working with simulation messages and with the RabbitMQ message bus in Python." | [https://github.com/simcesplatform/simulation-tools](https://github.com/simcesplatform/simulation-tools) |

## Usage

The component is based on the AbstractSimulationCompoment class from the [simulation-tools](https://github.com/simcesplatform/simulation-tools)
 repository. It is configured via environment variables which include common variables for all AbstractSimulationComponent subclasses such as rabbitmq connection and component name. Environment variables specific to this component are listed below:

- CIS_JSON_FILE (required): Location of the json file which contains the electricty grid's customer data. Relative file paths are in relation to the current working directory.

When using a json file as input data. the file must contain the following keys: ResourceId, CustomerId, BusName.

The component can be started with:

    python -m CIS.component

It can be also used with docker via the included dockerfile.

<!--
Follow the instruction steps from [https://wiki.eduuni.fi/display/tuniSimCES/Running+a+simulation#Runningasimulation-Preparationsforanewsimulation](https://wiki.eduuni.fi/display/tuniSimCES/Running+a+simulation#Runningasimulation-Preparationsforanewsimulation).

1. Install the simple component code

    ```bash
    git -c http.sslVerify=false clone --recursive https://git.ain.rd.tut.fi/procemplus/simple-component.git
    ```

2. Add the simple component to the `docker-compose-domain-build.yml` file in the `platform-manager/build/domain` folder. The context path is given here as a relative path from the `platform_manager/build/domain` folder.

    ```yaml
    simple-component:
        image: simple-component:0.1
        build:
            context: ../../../simple-component
            dockerfile: Dockerfile
    ```

3. Build the Docker images for the domain components including the newly added simple component by using the following command from the `platform-manager` folder.

    ```bash
    source platform_domain_setup.sh
    ```

4. Add `SimpleComponent` section to the `supported_components_domain.json`file in the `platform-manager`folder.

    ```json
    "SimpleComponent":
    {
        "Type": "dynamic",
        "Description": "Simple component",
        "DockerImage": "simple-component:0.1",
        "Attributes":
        {
            "SimpleValue":
            {
                "Environment": "SIMPLE_VALUE",
                "Optional": false
            },
            "InputComponents":
            {
                "Environment": "INPUT_COMPONENTS",
                "Optional": true,
                "Default": ""
            },
            "OutputDelay":
            {
                "Environment": "OUTPUT_DELAY",
                "Optional": true,
                "Default": 0.0
            }
        }
    }
    ```

5. Update Platform manager Docker image to include the new component type  by using the following command from the `platform-manager` folder.

    ```bash
    source platform_core_setup.sh
    ```

6. Copy the simulation configuration file to the `platform-component` folder by using the following command from the `platform-manager` folder.

    ```bash
    cp ../simple-component/simple_simulation.yml .
    ```

7. Run the test simulation by using the following commands from the `platform-manager` folder.

    ```bash
    source start_simulation.sh simple_simulation.yml
    ```
-->
