#!/bin/bash


## works both under bash and sh
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


## add udev rule
AUTOSTART_FILE=~/.local/share/applications/menulibre-littleted.desktop


cat > $AUTOSTART_FILE << EOL
[Desktop Entry]
Version=1.1
Type=Application
Name=Little Ted
Comment=A small descriptive blurb about this application.
Icon=$SCRIPT_DIR/littleted/gui/img/text-editor-black.png
Exec=$SCRIPT_DIR/startlittleted
Path=$SCRIPT_DIR
Actions=
Categories=Games;Office;
StartupNotify=true
Terminal=false

EOL


echo "File created in: $AUTOSTART_FILE"
