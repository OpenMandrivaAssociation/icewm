#!/bin/sh
#---------------------------------------------------------------
# Project         : Mageia
# Module          : bin
# File            : xeditor
# Author          : David Walser
# Created On      : Thu Apr 3 16:26:54 2012
# Updated On      : Mon Mar 6 20:05:25 2017
# Purpose         : launch a text editor
#---------------------------------------------------------------

strip_texteditor_var() {
    if [[ -n "$TEXTEDITOR" ]]; then
	if [[ `basename "$TEXTEDITOR"` == "xeditor" ]]; then
	    unset TEXTEDITOR
	elif ! which $TEXTEDITOR > /dev/null 2>&1; then
	    unset TEXTEDITOR
	fi
    fi
}

strip_texteditor_var
if [[ -z "$TEXTEDITOR" ]]; then

    # using GNOME
    if [[ -n "$GNOME_DESKTOP_SESSION_ID" ]]; then
	TEXTEDITOR="gedit"
    fi

    #using KDE
    if [[ -n "$KDE_FULL_SESSION" ]]; then
	TEXTEDITOR="kwrite"
    fi

    #using Xfce
    if [[ $XDG_CURRENT_DESKTOP == XFCE ]]; then
        TEXTEDITOR="mousepad"
    fi

    strip_texteditor_var

    [[ -z "$TEXTEDITOR" ]] && TEXTEDITOR=`which kwrite 2> /dev/null`
    [[ -z "$TEXTEDITOR" ]] && TEXTEDITOR=`which gedit 2> /dev/null`
    [[ -z "$TEXTEDITOR" ]] && TEXTEDITOR=`which mousepad 2> /dev/null`

    [[ -z "$TEXTEDITOR" ]] && which vim > /dev/null 2>&1 && TEXTEDITOR="xvt -e vim"
    [[ -z "$TEXTEDITOR" ]] && which efte > /dev/null 2>&1 && TEXTEDITOR="xvt -e efte"
    [[ -z "$TEXTEDITOR" ]] && which nano > /dev/null 2>&1 && TEXTEDITOR="xvt -e nano"
    if [[ -z "$TEXTEDITOR" ]]; then
	EMACS=`readlink /etc/alternatives/emacs`
	if [[ -n "$EMACS" ]]; then
	    if [[ `basename "$EMACS"` = "emacs-nox" ]]; then
		TEXTEDITOR="xvt -e emacs"
	    else
		TEXTEDITOR="emacs"
	    fi
	fi
    fi
fi

if [[ -n "$TEXTEDITOR" ]]; then
    exec $TEXTEDITOR "$@"
else
    echo "no text editor detected"
fi

# xeditor ends here
