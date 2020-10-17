# MCore - Maic's Core Utils

Collection of Python code I always copy into new projects.
Supportive code for logging, testing, network, and arcade game development.

## Installation

```
pip install git+https://github.com/eruvanos/mcore.git
```

## Overview

### General

* `mcore.log.configure()` - configures loggers (stdout: info|debug; stderr: warn|error) 
* `mcore.serialize.EnhancedJSONEncoder` - json support for dataclass 
* `mcore.enum.AutoNameEnum` - the missing AutoNameEnum 
* `mcore.dispatcher.Dispatcher` - Dispatcher for objects, register listener by type  
* `mcore.dispatcher.AsyncDispatcher` - Like `Dispatcher` with async interface  


### Networking

> `mcore.net.SecureNetwork` requires `mcore[secnet]`

* `mcore.net.Packet` - Dict like wrapper with access to items via attributes 
* `mcore.net.Network` - Handles data transfer via socket
* `mcore.net.SecureNetwork` - Like `Network` with end-to-end encryption
* `mcore.net.AIONetwork` - Like `Network` with async interface

### Test

* `mcore.test.local_dynamodb` - Manage local dynamodb within test setups
* `mcore.test.mock_server` - Mock json API with Flask in test setups


### Game development
> requires `mcore[game]`

* `mcore.game.fps.FPSDisplay` - Pyglets FPSDisplay with fix for arcade
* `mcore.game.frozen` - Utils for frozen environments (PyInstaller) 
* `mcore.game.sound.SoundPlayer` - Sound controls (music, sound effects, adjust volume)
* `mcore.game.animation.Animation` - Time based animations within arcade
* `mcore.game.transition.Effect` - Time based change of values
* `mcore.game.esper_ext.World` - improved version of `esper.World`
* `mcore.game.predict.PredictedValue` - Helper to smooth network latency
* `mcore.game.camera` - different camera implementations
    * `MarginCamera` - Camera keeps margin between borders and tracked sprite
    * `ZoomCamera` - Supports zoom
    * `FreeCamera` - Moveable with mouse interaction






