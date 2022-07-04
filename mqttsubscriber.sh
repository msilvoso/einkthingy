#!/bin/bash
readonly RRDDATABASE="/var/lib/ems-esp/temperatures.rrd"
readonly GRAPH="/var/lib/ems-esp/graph.png"
readonly LASTVALUES="/var/lib/ems-esp/lastvalues"
[[ ! -f "$RRDDATABASE" ]] && /usr/bin/rrdtool create "$RRDDATABASE" DS:wt:GAUGE:600:0:100 DS:ft:GAUGE:600:0:100 DS:ot:GAUGE:600:-30:60 RRA:AVERAGE:0.5:1:2016 RRA:AVERAGE:0.5:4:2016 RRA:AVERAGE:0.5:12:9600 RRA:MAX:0.5:288:400 RRA:MIN:0.5:288:400
while true
do
        values=$(mosquitto_sub -h localhost --pretty -u XXX -P YYY -C 2 -t "ems-esp/boiler_data" -t "ems-esp/boiler_data_ww")
        water_temp=$(echo $values | jq '.wwcurtemp' | grep -v null)
        outdoor_temp=$(echo $values | jq '.outdoortemp' | grep -v null)
        curflow_temp=$(echo $values | jq '.curflowtemp' | grep -v null)
        /usr/bin/rrdtool update "$RRDDATABASE" "N:$water_temp:$curflow_temp:$outdoor_temp"
        /usr/bin/rrdtool graph "$GRAPH" -Z -G mono --width=145 --height=80 --start now-86400s --end now -c "CANVAS#FFFFFF" -c "BACK#FFFFFF" -c "SHADEA#FFFFFF" -c "SHADEB#FFFFFF" -c "MGRID#000000" DEF:ota=$RRDDATABASE:ot:AVERAGE DEF:wta=$RRDDATABASE:wt:AVERAGE LINE1:wta#000000 LINE1:ota#000000::dashes
        /usr/bin/rrdtool lastupdate "$RRDDATABASE" | grep ':' | awk '{ print $2"\n"$3"\n"$4 }' >"$LASTVALUES"
done
