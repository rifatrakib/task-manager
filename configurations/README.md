### Configurations

This directory contains a sample file that is public which shows what variables are to be defined for configuring the application. There can be as many `.env.<mode_name>` files as needed each being used by a distinct mode for the app to operate in. For example, for *development* mode, there should be a `.env.development`, for *staging* mode, there should be a `.env.staging`, for *production* mode, there should be a `.env.production`, and so on.

Look at the `server.config.environment` module, it contains a `base.py` module which contains configuration classes that are inherited by classes abstracting each distinct app mode defined in different modules.
