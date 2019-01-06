#!/bin/bash
#
# Simple helper script -
#  lists all groupnames used in given inventory file.
#  Default inventory - hosts_example
#
#
INVENTORYFILE=${1:-hosts_example}
gawk '
/inv_groupnames/ {
     I=1 ;
     while( I<NF ) { 
       if($I ~ /inv_groupnames=/) { break } ;
       I++
     } ;
     gsub("inv_groupnames=|\\]|\\[|\"|.$","",$I) ;
     gsub("^.","",$I) ;
     split($I,GROUP,",") ;
     for( KEY in GROUP) {
       GROUPS[GROUP[KEY]]=GROUP[KEY]
     }
}
END {
  for( KEY in GROUPS ) {
    print GROUPS[KEY] 
  }
}' $INVENTORYFILE | sort -u
