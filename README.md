# cerebro
![jenkins status](https://travis-ci.org/fanequinha/cerebro.svg?branch=master)

![A Industriosa](https://i.imgur.com/DZ3NuFg.png)

This mono-repo contains the python related areas of `fanequiña`, that is an [A Industriosa](https://intranet.aindustriosa.org/) project about creating an autonomous boat.

Each folder in this mono-repo is a development area for `fanequiña`, currently we are working on the following areas:

## Mastermind 
A Machine Learning model & engine created to make `fanequiña` aware of it's surroundings while navigating.

## Commander
[dronekit](http://python.dronekit.io/)'s project created to work together with `Mastermaind` to command `fanequiña` using [pixhawk](https://pixhawk.org/).

* Requirements

    - Python 2.7
    - Pipenv (https://docs.pipenv.org/)


* Installation and environment activation

    ```
        >cd commander/
        >pipenv install
        >pipenv shell
    ```

* Configure connection environment

    You must check what port you have to connect depending your OS ((http://python.dronekit.io/guide/connecting_vehicle.html#get-started-connecting))

    You can configure your own environment with your custom file `.env`:

    ```
        >copy env.sample .env
        >vim .env
    ```

    Activate the environment:

    ```
        >export `cat .env`
    ```


* First connection

    ```
        >cd commander/
        >./main.py
    ```

* Listen location, attitude, velocity and gps

    ```
        >cd commander/
        >./main.py -l
    ```

## Pixhawk configuration

* Initial configuration
First of all you must install some Ground Station Software (GCS):
    - http://ardupilot.org/rover/docs/common-install-gcs.html

Secondly upgrade the Pixhawk firmware to the latest "Ardupilot Rover" Firmware

    - http://ardupilot.org/rover/docs/common-loading-firmware-onto-pixhawk.html

* Mandatory Hardware Configuration
  - http://ardupilot.org/rover/docs/rover-code-configuration.html

* Conecting the receiver
  - http://ardupilot.org/rover/docs/common-pixhawk-and-px4-compatible-rc-transmitter-and-receiver-systems.html

* Configure Firmware as Boat (“Frame class”)

  >To specify that the vehicle is a boat the FRAME_CLASS parameter should be set to 2 (Boat).

  - http://ardupilot.org/rover/docs/boat-configuration.html#boat-configuration
  - http://ardupilot.org/rover/docs/balance_bot-configure.html?highlight=frame_class#parameter-configuration


http://ardupilot.org/rover/docs/rover-motor-and-servo-connections.html?highlight=servo

http://ardupilot.org/rover/docs/common-pixhawk-and-px4-compatible-rc-transmitter-and-receiver-systems.html#common-pixhawk-and-px4-compatible-rc-transmitter-and-receiver-systems


