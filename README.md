Play My Piano
=============

A project by [Conrad Appel](http://conradhappeliv.com).

Overview
--------

This goal of this project is to allow a physical player piano to be controlled by a MIDI controller played by anyone, anywhere in the world. A bonus objective is to do so with as little requirements as possible, allowing anyone to jump right in and participate - even with little to no knowledge of code, technology, or even MIDI.

The project was hosted at [playmypiano.xyz](http://playmypiano.xyz) (`.xyz` domains happened to be as cheap as $1 at the time of the project's creation).

Components
----------

* Player piano
* Intel Edison
* Web server. I use Digital Ocean usually because it's so cheap and so simple - also they have sweet community docs. Use my [referral link](https://www.digitalocean.com/?refcode=352c96483c50) and you get $10 free :)
* Google's Hangouts on Air (for live streaming and recording)

How It Works
------------

When you go to the web page, the web server only needs to send a single page to the client browser. Then, there's a call to the [Web MIDI API](http://webaudio.github.io/web-midi-api/), which exposes the MIDI devices that are made available to your browser. As of the time of the project's creation, the only browser that had yet implemented the API was Google Chrome, which is the reason Chrome is the only supported browser. The user is prompted to choose the appropriate MIDI device. KnockoutJS handles data-synchronization and rendering of page components.

On the choice, the browser sets up handlers for MIDI events from the keyboard. Before allowing the user to continue further, they need to play anything to confirm that their piano is working and the browser is receiving the events (in order to prevent wasted time during their "performance"). 

Then, the user can elect to "get in line", where the browser establishes a websocket connection to the web server, which keeps track of everyone in line, broadcasting to all clients when the line changes (someone's turn is up or someone leaves).

Once the user reaches the front of the queue, the web server will start accepting MIDI messages sent from the client, which it then retransmits to the piano's Edison. The Python client on the Edison uses [MIDO](https://mido.readthedocs.org/en/latest/) to parse the bytes and to handle easy transmission through the serial connection (I was very pleasantly surprised by this package - I'd recommend it). The client, the web server, and the Edison all filter out MIDI messages that the piano cannot use, for security (wouldn't want people to break the piano in ways that I haven't thought of). The Edison then sends the MIDI messages to the piano when the time is right.

On the way back, I used Google Hangouts on Air to embed a live stream of the whole event on the website, as well as giving me a recording for Youtube and such. Super easy.

Timing
------

To determine the correct time, the client application also sends over a field representing the number of milliseconds since the last note was played, which the Edison uses to maintain mostly continual playback. To compensate for potential lag anywhere in the chain, the Edison will wait 5 seconds after receiving a message to even consider playing it, and then make sure the notes are still spaced probably according to the client's playback. Here's a timing diagram that may you understand what's happening here:

    Time sent
    |-----o--------o------ooo--------|
    Time received
    |--------o-----o------o---o-o----|
    Time played
    |-------------o--------o------ooo|
    
As you can see, even though the notes are received at a completely different rhythm, this system accounts for the lag and plays the notes at the same rhythm the client played. In the future, I could make the "buffer" dynamic dependent on the current roundtrip time to the piano, as to try to minimize the lag from client to piano.
